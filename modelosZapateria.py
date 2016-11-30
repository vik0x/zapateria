import webapp2
from google.appengine.ext import ndb

class marca(ndb.Model):
	nombre = ndb.StringProperty()
	def all(self):
		return marca.query().fetch()

class tipo_calzado(ndb.Model):
	nombre = ndb.StringProperty()
	def all(self):
		return tipo_calzado.query().fetch()

class material_calzado(ndb.Model):
	nombre = ndb.StringProperty(choices = ['Piel', 'Sintetico'])
	def all(self):
		return material_calzado.query().fetch()

class temporada(ndb.Model):
	nombre = ndb.StringProperty(choices = ['Verano', 'Invierno', 'Otono', 'Primavera'])
	def all(self):
		return temporada.query().fetch()

class genero(ndb.Model):
	nombre = ndb.StringProperty()
	def all(self):
		return genero.query().fetch()

class zapato(ndb.Model):
	marca = ndb.StringProperty()
	tipo = ndb.StringProperty()
	temporada = ndb.StringProperty()
	material= ndb.StringProperty()
	genero = ndb.StringProperty()
	numero = ndb.IntegerProperty()
	costo = ndb.FloatProperty()
	existencia = ndb.IntegerProperty()
	def all(self):
		return zapato.query().fetch()

class almacen(ndb.Model):
	zapatos = ndb.StructuredProperty(zapato)
	cantidad = ndb.IntegerProperty()
	fecha = ndb.DateTimeProperty()
	tipo = ndb.BooleanProperty()
	def all(self):
		return almacen.query().fetch()

class pedido(ndb.Model):
	mail = ndb.IntegerProperty()
	fecha = ndb.DateTimeProperty()
	estatus = ndb.IntegerProperty()
	def all(self):
		return pedido.query().fetch()

class detalle_pedido(ndb.Model):
	pedido = ndb.StructuredProperty(pedido)
	zapato = ndb.StructuredProperty(zapato)
	cantidad = ndb.IntegerProperty()
	def all(self):
		return detalle_pedido.query().fetch()

class tareas(ndb.Model):
	nombre = ndb.StringProperty()
	def all(self):
		return tareas.query().fetch()
