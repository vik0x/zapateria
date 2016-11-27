import webapp2
from google.appengine.ext import ndb

class marca(ndb.Model):
	nombre = ndb.StringProperty()

class tipo_calzado(ndb.Model):
	nombre = ndb.StringProperty()

class material_calzado(ndb.Model):
	nombre = ndb.StringProperty()

class temporada(ndb.Model):
	nombre = ndb.StringProperty()

class genero(ndb.Model):
	nombre = ndb.StringProperty()

class zapato(ndb.Model):
	marca = ndb.StringProperty()
	tipo = ndb.StringProperty()
	temporada = ndb.StructuredProperty(temporada)
	material= ndb.StructuredProperty(material_calzado, repeated = True)
	genero = ndb.StructuredProperty(genero)
	numero = ndb.IntegerProperty()
	costo = ndb.FloatProperty()
	existencia = ndb.IntegerProperty()

class almacen(ndb.Model):
	zapatos = ndb.StructuredProperty(zapato)
	cantidad = ndb.IntegerProperty()
	fecha = ndb.DateTimeProperty()
	tipo = ndb.BooleanProperty()

class pedido(ndb.Model):
	mail = ndb.IntegerProperty()
	fecha = ndb.DateTimeProperty()
	estatus = ndb.IntegerProperty()

class detalle_pedido(ndb.Model):
	pedido = ndb.StructuredProperty(pedido)
	zapato = ndb.StructuredProperty(zapato)
	cantidad = ndb.IntegerProperty()
