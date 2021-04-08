Class Profesor():
	def _init_(self, DNI, nombre, tipoUsuario): #constructor
		self.nombre = nombre
		self.DNI = DNI
		self.tipoUsuario =  tipoUsuario


	#observadores
	def getNombre(self):
		return self.nombre

	def getDNI(self):
		return self.DNI

	def getTipoUsuario(self):
		return self.tipoUsuario


	#modificadores
	def setNombre(self, nombre):
		self.nombre=nombre

	def setDNI(self, DNI):
		self.DNI=DNI

	def setTipoUsuario(self, tipoUsuario):
		self.tipoUsuario=tipoUsuario


	#funciones de la clase
	def altaProfesorComision(self, ):
		pass