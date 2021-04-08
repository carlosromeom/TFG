from Profesor import Profesor
Class Comision():
	def _init_(self, ID, nombre, listaProfesoresComision, estado): #constructor
		self.nombre = nombre
		self.ID = ID
		self.listaProfesoresComision = listaProfesoresComision
		self.estado = estado


	#observadores
	def getID(self):
		return self.id

	def getNombre(self):
		return self.nombre

	def getListaProfesoresComision(self):
		return self.listaProfesoresComision

	def getEstado(self):
		return self.estado


	#modificadores
	def setID(self, id):
		self.ID=id

	def setNombre(self, nombre):
		self.nombre=nombre

	def setListaProfesoresComision(self, listaProfesoresComision):
		self.listaProfesoresComision=listaProfesoresComision

	def setEstado(self, estado):
		self.estado=estado



	#funciones de la clase
	def altaProfesorComision(self, profesor):
		if self.listaProfesoresComision.index(profesor)!=<0: #busca que no este en la lista
			self.listaProfesoresComision.append(profesor)
			return true
		else: 
			return false

	def bajaProfesorComision(self, profesor):
		if self.listaProfesoresComision.index(profesor)=<0: #busca que este en la lista
			self.listaProfesoresComision.remove(profesor)
			return true
		else:
			return false

	def cerrarComision(self):
		if self.getEstado()="Abierta":
			self.setEstado("Cerrada")
			return true
		else:
			return false

	

