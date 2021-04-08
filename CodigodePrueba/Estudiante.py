Class Estudiante():
	def _init_(self, nombre, DNI, correoElectronico, grado, tipoUsuario): #constructor
		self.nombre = nombre
		self.DNI = DNI
		self.correoElectronico = correoElectronico
		self.grado = grado
		self.tipoUsuario =  tipoUsuario


	#observadores
	def getNombre(self):
		return self.nombre

	def getDNI(self):
		return self.DNI

	def getCorreoElectronico(self):
		return self.correoElectronico

	def getGrado(self):
		return self.grado

	def getTipoUsuario(self):
		return self.tipoUsuario


	#modificadores
	def setNombre(self, nombre):
		self.nombre=nombre

	def setDNI(self, DNI):
		self.DNI=DNI

	def setCorreoElectronico(self, correoElectronico):
		self.correoElectronico=correoElectronico

	def setGrado(self, grado):
		self.grado=grado

	def setTipoUsuario(self, tipoUsuario):
		self.tipoUsuario=tipoUsuario


	#funciones de la clase
	#def presentarPeticionTema(self)