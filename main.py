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
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext import ndb
from webapp2_extras import sessions
from datetime import date
from webob import Request

mail_message= mail.EmailMessage()
app_mail = "pedidos@v-gutierrez.appspotmail.com"

num = random.randint(1,100)
nom = ""

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
        self.render(template_name)

class addHandler(Handler):
    def extract_template_name_from_request(self):
        logging.info('ruta = ' +str(self.request.path_info[8:-5]))
        return self.request.path_info[8:-5]

    def get(self):
        template_name = self.extract_template_name_from_request() + '/create.html'
        logging.info('template name ='+str(template_name))
        self.render(template_name)

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
								('/index.html', MainPage),
								('/agregar/.*.html',addHandler),
								('.*.html',PageHandler),
								#('/contacto',Contacto),
                                (MailHandler.mapping())
                              ],
                              debug=True, config=config)
