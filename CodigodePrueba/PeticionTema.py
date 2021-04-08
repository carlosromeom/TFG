Class PeticionTema():
	def _init_(self, tituloTrabajo, solicitaAdelanto, motivosAdelanto, cumplimientoRequisitoTFM, director1, director2, sugerencias, aceptaSugerencias): #constructor
		self.tituloTrabajo=tituloTrabajo
		self.solicitaAdelanto=solicitaAdelanto
		self.motivosAdelanto=motivosAdelanto
		self.cumplimientoRequisitoTFM=cumplimientoRequisitoTFM
		self.director1=director1
		self.director2=director2
		self.sugerencias=sugerencias
		self.aceptaSugerencias=aceptaSugerencias

	#observadores
	def getTituloTrabajo(self):
		return self.tituloTrabajo

	def getSolicitaAdelanto(self):
		return self.solicitaAdelanto

	def getMotivosAdelanto(self):
		return self.motivosAdelanto

	def getCumplimientoRequisitoTFM(self):
		return self.cumplimientoRequisitoTFM

	def getDirector1(self):
		return self.director1

	def getDirector2(self):
		return self.director2

	def getSugerencias(self):
		return self.sugerencias

	def getAceptaSugerencias(self):
		return self.aceptaSugerencias


	#modificadores
	def setTituloTrabajo(self, a):
		self.tituloTrabajo=a

	def setSolicitaAdelanto(self, a):
		self.solicitaAdelanto=a

	def setMotivosAdelanto(self, a):
		self.motivosAdelanto=a

	def setCumplimientoRequisitoTFM(self, a):
		self.cumplimientoRequisitoTFM = a

	def setDirector1(self, a):
		self.director1=a

	def setDirector2(self, a):
		self.director2=a

	def setSugerencias(self, a):
		self.sugerencias=a

	def setAceptaSugerencias(self, a):
		self.aceptaSugerencias=a


	#funciones de la clase
	def presentarPeticionTema(self, titulo, adelanto, motivosAdelanto, cumplimientoRequisitoTFM, director1, director2):
		peticionTema=PeticionTema(titulo, adelanto, motivosAdelanto, cumplimientoRequisitoTFM, director2, director2)
		
