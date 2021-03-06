# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

from datetime import *

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

Telefone = db.define_table('telefone',

Field('numeroTelefone', 'string', label='Telefone'),

)

Fornecedor = db.define_table('fornecedor',

Field('razao_social', 'string', label='Nome da empresa'),
Field('cnpj', 'string', label='CNPJ da empresa'),

)

Fornecedor.razao_social.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Fornecedor.cnpj.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')

Cliente = db.define_table('clientes',

Field('nome', 'string', label='Nome'),
Field('data_nasc', 'date', label='Data de nascimento'),
Field('cpf', 'string', label='CPF', default='000.000.000-00'),
Field('email', 'string', label='E-mail', default='seuemail@email.com'),

)

Cliente.nome.requires = IS_NOT_EMPTY(error_message='Digite aqui seu nome')
Cliente.data_nasc.requires = IS_NOT_EMPTY(error_message='Digite aqui a data de nascimento')
Cliente.data_nasc.requires = IS_DATE(format='%d-%m-%Y', error_message='A data deve estar no formato DD-MM-AAAA')
Cliente.cpf.requires = IS_NOT_EMPTY(error_message='Verifique as informações inseridas')
Cliente.email.requires = IS_EMAIL(error_message='Digite um e-mail válido')

Pedido = db.define_table('pedido',

Field('dataPedido', 'date', label='Data do pedido'),
Field('horaPedido', 'time', label='Horário', default='00:00'),
Field('dataEntrega', 'date', label='Data de entrega do pedido (previsto)'),
Field('horaEntrega', 'time', label='Horário de entrega (previsto)', default='00:00'),

)

Pedido.dataPedido.requires = IS_DATE(format='%d-%m-%Y', error_message='A data deve estar no formato DD/MM/AAAA')
Pedido.dataEntrega.requires = IS_DATE(format='%d-%m-%Y', error_message='A data deve estar no formato DD/MM/AAAA')

Endereco = db.define_table('endereco',

Field('rua', 'string', label='Nome da rua'),
Field('numero', 'integer', label='Número'),
Field('complemento', 'string', label='Complemento', default='Não informado'),
Field('tipoEndereco', 'string', label='Tipo do endereço'),
Field('bairro', 'string', label='Bairro'),
Field('cidade', 'string', label='Cidade'),

)

Endereco.rua.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Endereco.numero.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Endereco.complemento.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Endereco.tipoEndereco.requires = requires=IS_IN_SET(['Residencial', 'Comercial', 'Não informado'])
Endereco.bairro.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Endereco.cidade.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')

Orcamento = db.define_table('orcamento',

Field('codCliente', 'integer', 'references clientes'),
Field('codPedido', 'integer', 'references pedido'),
Field('dataOrcamento', 'date', label='Data de emissão do orçamento'),
Field('valorTotal', 'float', label='Valor total dos preços'),
Field('desconto', 'float', label='Descontos'),
Field('precoFinal', 'float', label='Preço final de venda'),

)

Orcamento.dataOrcamento.requires = IS_DATE(format='%d-%m-%Y', error_message='A data deve estar no formato DD/MM/AAAA')
Orcamento.dataOrcamento.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Orcamento.valorTotal.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Orcamento.desconto.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Orcamento.precoFinal.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')

Item = db.define_table('item',

Field('nome', 'string', label='Nome do ingrediente'),
Field('descricao', 'string', label='Descrição'),
Field('precoUnitario', 'float', label='Preço por unidade'),
Field('quantidade', 'integer', label='Quantidade'),
Field('unidade', 'string', label='Unidade de medida'),
Field('precoTotal', 'float', label='Preço total', default=0),

)

Item.nome.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Item.descricao.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Item.precoUnitario.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Item.quantidade.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Item.unidade.requires = IS_IN_SET(['quilogramas (kg)', 'gramas (g)', 'unidades'])

Produto = db.define_table('produto',

Field('nome', 'float', label='Nome do produto'),
Field('descricao', 'string', label='Descrição'),
Field('custoIngredientes', 'float', label='Custo dos ingredientes'),
Field('custoFabricacao', 'float', label='Custo da fabricação'),
Field('lucros', 'float', label='Lucro da venda'),
Field('custoFinalProd', 'float', label='Custo total do produto', default=0),

)

Produto.nome.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Produto.descricao.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Produto.custoIngredientes.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Produto.custoFabricacao.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
Produto.lucros.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')
#~ Produto.custoFinalProd.requires = IS_NOT_EMPTY(error_message='Preencha os campos corretamente')

Fornecedor_Item = db.define_table('fornecedor_item',

Field('cod_Item', 'integer', 'references item'),
Field('codFornecedor', 'integer', 'references fornecedor'),

)

Produto_Item = db.define_table('produto_item',

Field('cod_Item', 'integer', 'references item'),
Field('codProduto', 'integer', 'references produto'),

)

Orcamento_Produto = db.define_table('orcamento_produto',

Field('codOrcamento', 'integer', 'references orcamento'),
Field('codProduto', 'integer', 'references produto'),

)

Telefone_Cliente = db.define_table('telefone_cliente',

Field('codTelefone', 'integer', 'references telefone'),
Field('codCliente', 'integer', 'references clientes'),

)

Telefone_Fornecedor = db.define_table('telefone_fornecedor',

Field('codTelefone', 'integer', 'references telefone'),
Field('codFornecedor', 'integer', 'references fornecedor'),

)

Endereco_Pedido = db.define_table('endereco_pedido',

Field('codEndereco', 'integer', 'references endereco'),
Field('codPedido', 'integer', 'references pedido'),

)

Endereco_Cliente = db.define_table('endereco_cliente',

Field('codEndereco', 'integer', 'references endereco'),
Field('codCliente', 'integer', 'references clientes'),

)

Endereco_Fornecedor = db.define_table('endereco_fornecedor',

Field('codEndereco', 'integer', 'references endereco'),
Field('codFornecedor', 'integer', 'references fornecedor'),

)
