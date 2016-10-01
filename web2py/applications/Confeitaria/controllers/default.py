# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def BuscarCliente():
	form = SQLFORM.factory(
		Field('nome', 'string', requires=IS_NOT_EMPTY(error_message='Digite seu nome')),
		Field('dataNasc', 'date', label='Data de nascimento', requires=IS_DATE(error_message='Insira uma data válida')),
		submit_button='Buscar',
	)
	form.add_button('Continuar', URL('CadastrarCliente'))
	query = Cliente.id < 0
	if form.process().accepted:
		nomeCliente = form.vars.nome
		dtNascCliente = form.vars.dataNasc
		if nomeCliente != None and dtNascCliente != None:
			query = Cliente.id > 0
			query &= Cliente.nome.like('%' + nomeCliente + '%')
			query &= Cliente.data_nasc == dtNascCliente
	elif form.errors:
		response.flash = 'Verifique as informações inseridas!'
	count = db(query).count()
	resultados = db(query).select()
	msg = response.flash = T('%s registros encontrados' %count)
	return dict(form=form, resultados=resultados)

def CadastrarCliente():
	form = SQLFORM.factory(Cliente, Telefone, Endereco, submit_button='Salvar')
	if form.process(keepvalues=True).accepted:
		id = Cliente.insert(**db.clientes._filter_fields(form.vars))
		form.vars.codCliente = id
		idCliente = id
		id = Endereco.insert(**db.endereco._filter_fields(form.vars))
		idEndereco = id
		id = Telefone.insert(**db.telefone._filter_fields(form.vars))
		idTelefone = id
		id = Endereco_Cliente.insert(codEndereco = int(idEndereco), codCliente = int(idCliente))
		id = Telefone_Cliente.insert(codTelefone = int(idTelefone), codCliente = int(idCliente))
		db.commit()
		response.flash = 'Cliente cadastrado com sucesso!'
	elif form.errors:
		response.flash = 'Verifique as informações inseridas!'
	return dict(form=form)

def CadastrarFornecedor():
	form = SQLFORM.factory(Fornecedor, Telefone, Endereco, submit_button='Salvar')
	if form.process(keepvalues=True).accepted:
		id = Fornecedor.insert(**db.fornecedor._filter_fields(form.vars))
		form.vars.codFornecedor = id
		idFornecedor = id
		id = Endereco.insert(**db.endereco._filter_fields(form.vars))
		idEndereco = id
		id = Telefone.insert(**db.telefone._filter_fields(form.vars))
		idTelefone = id
		id = Endereco_Fornecedor.insert(codEndereco = int(idEndereco), codFornecedor = int(idFornecedor))
		id = Telefone_Fornecedor.insert(codTelefone = int(idTelefone), codFornecedor = int(idFornecedor))
		db.commit()
		response.flash = 'Cliente cadastrado com sucesso!'
	elif form.errors:
		response.flash = 'Verifique as informações inseridas!'
	return dict(form=form)

def CadastrarItem():

	form = SQLFORM.factory(Item,
		submit_button='Adicionar ingrediente',
		keepvalues=True,
	)
	form.add_button('Continuar', URL('CadastrarPedido'))
	if form.process(keepvalues=True).accepted:
		p_unit = float(form.vars.precoUnitario)
		quant = int(form.vars.quantidade)
		precoTotal = float(p_unit * quant)
		if p_unit != None and quant != None:
			form.vars.precoTotal = precoTotal
		id = Item.insert(**db.item._filter_fields(form.vars))
		db.commit()
		response.flash = 'Ingrediente cadastrado com sucesso! Total %.2f' %precoTotal
	elif form.errors:
		response.flash = 'Verifique as informações inseridas!'

	return dict(form=form)

def CadastrarProduto():
	form = SQLFORM.factory(Produto,
		submit_button='Adicionar produto',
	)
	form.add_button('Continuar', URL('CadastrarPedido'))
	if form.process(keepvalues=True).accepted:
		custo_ingr = float(form.vars.custoIngredientes)
		custo_fabr = float(form.vars.custoFabricacao)
		lucro_venda = float(form.vars.lucros)
		total_prod = float(custo_ingr + custo_fabr + lucro_venda)
		form1.vars.custoFinalProd = total_prod
		id = Produto.insert(**db.produto._filter_fields(form.vars))
		db.commit()
		response.flash = 'Produto cadastrado com sucesso!\Total %.2f' % total_prod
	elif form.errors:
		response.flash = 'Verifique as informações inseridas!'
	return dict(form=form)

def CadastrarPedido():
	form = SQLFORM.factory(Pedido, submit_button='Salvar')
	if form.process().accepted:
		response.flash = 'Pedido cadastrado com sucesso!'
		redirect(URL('CadastrarOrcamento'))
	elif form.errors:
		response.flash = 'Verifique as informações inseridas!'
	return dict(form=form)

def CadastrarOrcamento():
	form = SQLFORM(Orcamento, submit_button='Salvar')
	if form.process().accepted:
		response.flash = 'Pedido cadastrado com sucesso!'
	elif form.errors:
		response.flash = 'Verifique as informações inseridas!'
	return dict(form=form)


