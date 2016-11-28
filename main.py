#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
import os #jinja para leer sistema de archivos
import jinja2
import random
import logging
import urllib #manipulación de urls
import urlparse
from google.appengine.api import mail
from google.appengine.ext import ndb
from webapp2_extras import sessions
from datetime import date
from webob import Request
from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from modelosZapateria import marca
from modelosZapateria import tipo_calzado
from modelosZapateria import material_calzado
from modelosZapateria import temporada
from modelosZapateria import genero
from modelosZapateria import zapato
from modelosZapateria import almacen
from modelosZapateria import pedido
from modelosZapateria import detalle_pedido
# from models import marca_model

mail_message= mail.EmailMessage()
app_mail = "pedidos@v-gutierrez.appspotmail.com"

num = random.randint(1,100)
nom = ""

#************ oauth2Decorator
decorator = OAuth2Decorator(
	client_id='796891516114-8c0uee79a6c0aagb7ltrqf6vhi6lob30.apps.googleusercontent.com',
	client_secret='SB9JML0U4krnurkK1Tw2ICNx',
	scope='https://www.googleapis.com/auth/tasks')
service = build('tasks','v1')

class Correos(ndb.Model):
    message_body = ndb.StringProperty()

class user(ndb.Model):
	usr = ndb.StringProperty()
	psw = ndb.StringProperty()
	mail = ndb.StringProperty()

class record(ndb.Model):
	usr = ndb.StringProperty()
	intentos = ndb.StringProperty()
	resultado = ndb.StringProperty()

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'views')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def render_str(template, **params):
	t = JINJA_ENVIRONMENT.get_template(template)
	return t.render(params)

class Handler(webapp2.RequestHandler):
	def render(self,template, **kw):
		self.response.out.write(render_str(template, **kw))

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def dispatch(self):
		self.session_store = sessions.get_store(request = self.request)
		try:
			webapp2.RequestHandler.dispatch(self)
		finally:
			self.session_store.save_sessions(self.response)
	@webapp2.cached_property
	def session(self):
		return self.session_store.get_session()

class MailHandler(InboundMailHandler):
    def receive(self, mail_message):
        for content_type, pl in mail_message.bodies('text/plain'):
            mensaje = Correos(message_body=pl.payload.decode('utf-8'))
            mensaje.put()

class MainPage(Handler):
	def get(self):
		self.render('index.html')
		# self.response.out.writ1e("index.html")
	# def get(self):
	# 	diccionario = {}
	# 	diccionario["nombre"] = "El nombre"
	# 	diccionario["apellido"] = "El buen apellido"
	# 	self.render("index.html",
	# 		message="Una variable",
	# 		dic = diccionario
	# 		)

class dashBoard(Handler):
	def get(self):
		self.render('index.html');

class PageHandler(Handler):
    def extract_template_name_from_request(self):
        logging.info('ruta = ' +str(self.request.path_info[1:-5]))
        return self.request.path_info[1:-5]

    def get(self):
        template_name = self.extract_template_name_from_request() + '/index.html'
        logging.info('template name ='+str(template_name))
        model_n = self.extract_template_name_from_request()
        if( model_n == 'pedido/pendiente' or model_n == 'pedido/terminado' ):
        	model_n = 'pedido'
        # self.response.out.write(model_n)
        q_model = eval(model_n+'()')
        d= q_model
        m= d.all()
        self.render(template_name,obj=m)

class addHandler(Handler):
    def extract_template_name_from_request(self):
		global add_ruta
		logging.info('ruta = ' +str(self.request.path_info[8:-5]))
		add_ruta = str(self.request.path_info[9:-5])
		return self.request.path_info[8:-5]

    def get(self):
		global add_ruta
		ruta = self.extract_template_name_from_request()
		# self.response.out.write(ruta)
		data = {}
		if( ruta == '/almacen' ):
			z = zapato()
			t = tipo_calzado()
			data = {'zapato':z.all(),'tipo':t.all()}
		if( ruta == '/zapato' ):
			m = marca()
			t = tipo_calzado()
			te = temporada()
			ma = material_calzado()
			data = {
				'marca':m.all(),
				'tipo':t.all(),
				'temporada':te.all(),
				'material':ma.all()
			}
		template_name = self.extract_template_name_from_request() + '/create.html'
		logging.info('template name ='+str(template_name))
		self.render(template_name,data = data)

    def post(self):
		global campo
		global add_ruta
		obj = eval(add_ruta + '()')
		if(add_ruta=='marca' or add_ruta=='tipo_calzado'):
			obj.nombre = self.request.get('nombre')
		elif(add_ruta=='zapato'):
			#Guardado de llave
			#marca_key= marca.query(marca.nombre==self.request.get('marca')).get()
			obj.marca = self.request.get('marca')
			obj.tipo= self.request.get('tipo')
			obj.temporada= self.request.get('temporada')
			obj.material= self.request.get('material')
			obj.genero= self.request.get('genero')
			obj.numero= int(self.request.get('numero'))
			obj.costo= float(self.request.get('costo'))
			obj.existencia= int(self.request.get('existencia'))
		elif(add_ruta=='almacen'):
			#obj.zapatos= zapato() Definir que se va mostrar del zapato -> para desplegar
			obj.zapatos= self.request.get('zapatos')
			obj.cantidad= int(self.request.get('cantidad'))
			obj.fecha= self.request.get('fecha')
			obj.tipo= self.request.get('tipo')
		elif(add_ruta=='detalle_pedido'):
			obj.pedido = self.request.get('pedido')
			obj.zapato = self.request.get('zapato')
			obj.cantidad= int(self.request.get('cantidad'))
		obj.put()
		self.redirect("/"+add_ruta+".html")

class tasks(Handler):
	@decorator.oauth_required
	def get(self):
		tasks=service.tasks().list(tasklist='@default').execute(http=decorator.http())
		items = tasks.get('items', [])
		response = '\n'.join([task.get('title','') for task in items])
		self.render("tareas/index.html", response=items)

# class Contacto(Handler):
#     def get(self):
#         self.render("views/pedido/pendientes/index.html")
#     def post(self):
#         global mail_message
#         sender_email = self.request.get("email")
#         logging.info("sender_email: " + sender_email)
#         message = self.request.get("message")
#         logging.info("message: " + message)
#         mail_message.sender = sender_email
#         mail_message.to = app_mail
#         mail_message.subject = "Prueba"
#         mail_message.body = message
#         mail_message.send()
#         logging.info("Entra post")



config={}
config['webapp2_extras.sessions'] = {
	   'secret_key':'some-secret-key',
	}
app = webapp2.WSGIApplication([('/', MainPage),
	('/tareas.html', tasks),
	('/index.html', MainPage),
	('/agregar/.*.html',addHandler),
	('.*.html',PageHandler),
	#('/contacto',Contacto),
    (MailHandler.mapping()),
    (decorator.callback_path, decorator.callback_handler())
  ],
  debug=True, config=config)
