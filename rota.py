import Instancia

class Rota:
	
	def __init__(self):
		
		self.rotaEq={}  # dicionario que possui cada equipe relacionada com as atividades que irão realizar (ordenada)
						#chave = equipes
		self.atividades={} #atividades que devem ser concluidas em cada talhao, em ordem de precedencia
		self.tempoAtividade=[] #matriz numAtividades x 2 que armazena atividades com seu tempo de inicio e fim
		self.dia = 1
		self.ordena =[]
		self.armazena=[]
		
	
	def CalcularTempo(self,iinstancia,arquivo):
		
		for i in range (1, iinstancia.equipes+1):
			self.rotaEq[i] = [] 	 
	
		for i in range (1, iinstancia.talhoes+1):
			self.atividades[i] = []
		
		for i in range (0, iinstancia.numAtividades):
			linha=[]
			for j in range(2):
				 linha.append(0)
			self.tempoAtividade.append(linha)
	
		for i in range (1,iinstancia.equipes+1):
			linha = arquivo.readline()
			espaco = linha.split()
			cont = int(espaco[1])
			ite = 2
			while cont != -1:
				self.rotaEq[i].append(cont)
				cont = int(espaco[ite])
				ite= ite+1
			
		linha = arquivo.readline()
	
		for i in range (1,iinstancia.talhoes+1):
			linha = arquivo.readline()
			espaco = linha.split()
			cont = int(espaco[1])
			ite = 2
			while cont != -1:
				self.atividades[i].append(cont)
				cont = int(espaco[ite])
				ite = ite+1
			
		linha = arquivo.readline()
		
		linha= arquivo.readline()
		espaco = linha.split()
		
		for i in range(0, iinstancia.numAtividades):
			cont = int(espaco[i])
			self.ordena.append(cont) 
			 
		
		linha = arquivo.readline()
	
		for i in range (0,iinstancia.equipes):
			linha= arquivo.readline()
			espaco = linha.split()
			tmp =[]
			for j in range (0,iinstancia.numAtividades):
				elemento = float(espaco[j])
				tmp.append(elemento)
			iinstancia.tempoTarefa.append(tmp[:])
			
				
		linha = arquivo.readline()
		
		
		for i in range (0, iinstancia.numAtividades+1):
			linha = arquivo.readline()
			espaco =  linha.split()
			tmp = []
			for j in range (0,iinstancia.numAtividades+1):
				elemento = float(espaco[j])
				tmp.append(elemento)
			iinstancia.tempoDeslocamento.append(tmp[:])
		

		repetir = 1		
		original=self.ordena
		
		
		for xis in range(0, len(self.ordena)):
				ativ = self.ordena[xis]
				
				equipe = 1			
					
				for chave,valor in self.rotaEq.items():
					for ajuda in range (0, len(valor)):
						if self.rotaEq[chave][ajuda] == ativ:
							equipe=chave  
					
				maior = 0
				
				for chave, valor in self.atividades.items():
					if len(valor) > maior:
						maior = len(valor)
						
		
				auxiliar= -1
				talhao = -1
				
				for cont in range(1,iinstancia.talhoes+1):
					for i in range (0, maior-1):
						if self.atividades[cont][i] == ativ:
							auxiliar=i
							talhao=cont
						
				if auxiliar == 0:
							
					if self.rotaEq[equipe][0] == ativ:
						
						self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ] 	
						
						if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): 
							self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) - 
								(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
							self.dia= self.dia + 1
								
						else:
							self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]
									
					else:
						aux = []
						for valor in self.rotaEq[equipe]: 
							aux.append(valor)
						
						anterior = -1
						indiceAntUm = -1
						i= xis-1
						
						while (i>=0):
							for j in aux:
								if self.ordena[i] == j and anterior == -1:
									anterior = self.ordena[i]
									indiceAntUm= i
							i=i-1
									
						if self.tempoAtividade[anterior-1][1]+ iinstancia.tempoDeslocamento[ativ][anterior] > iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]:	
							self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ]
							self.dia= self.dia+1
									
						else:
							self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1]+ iinstancia.tempoDeslocamento[ativ][anterior]
								
						if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):
							self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) - (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]))
							self.dia= self.dia + 1
							
						else:
							self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]
								
				else:
					
					listaRota = []
					for chave,valor in self.rotaEq.items():
						for ajuda in range (0, len(valor)):
							if self.rotaEq[chave][ajuda] == ativ:
								for x in self.rotaEq[chave]:
									listaRota.append(x)
					
					listaTalhao = []
					for chave,valor in self.atividades.items():
						for ajuda in range (0, len(valor)):
							if self.atividades[chave][ajuda] == ativ:
								for x in self.atividades[chave]:
									listaTalhao.append(x)
					
					anterior = -1
					indiceAntUm = -1
					i= xis-1
						
					while (i>=0):
						for j in listaRota:
							if self.ordena[i] == j and anterior == -1:
								anterior = self.ordena[i]
								indiceAntUm= i
						i=i-1
					
					anterior2 = -1
					indiceAntDois = -1
					i = xis-1
					
					while (i>=0):
						for j in listaTalhao:
							if self.ordena[i] == j and indiceAntDois == -1:
								anterior2 = self.ordena[i]
								indiceAntDois= i
						i=i-1
							
					if anterior == anterior2:
								
						self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1] 
						
						if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): 
					
							self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0]+iinstancia.tempoTarefa[equipe-1][ativ-1]) - 
								(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
							self.dia= self.dia + 1
									
						else:
							self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] 
										
					else: 
								
						if anterior != -1:
							
							if self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] > self.tempoAtividade[anterior2-1][1]:
										
								if self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] >(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):
									
									self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ]   
									self.dia = self.dia + 1
								else:
									self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] 
											
								if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): 
									
									self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -
									(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
									self.dia= self.dia + 1
											
								else:
									self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][i-1]
												
							elif self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior-1][ativ] < self.tempoAtividade[anterior2-1][1]:
										
								self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior2-1][1]
										
								if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] >(iinstancia.turno- iinstancia.tempoDeslocamento[0][ativ]):
									self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + tempoTarefa[equipe-1][ativ-1]) -
									(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]))
									self.dia= self.dia + 1
										
										
						else:
							
							self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior2-1][1]
									
							if self.tempoAtividade[ativ-1][0]+ iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): 
								self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -
								(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
								self.dia= self.dia + 1
										
							else:
								self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][i-1]
				
				
		menor = self.dia		
		controle = False
			
		for c,v in self.rotaEq.items():
			for tam in range (0, len(v)):
				ativ1 = self.rotaEq[c][tam]
				for aux in range (tam+1, len(v)):
					ativ2 = self. rotaEq[c][aux]
					
						
					for chave,valor in self.atividades.items():
						for ajuda in range (0, len(valor)):
							
							if ativ1 == self.atividades[chave][ajuda]:
								controle = False
								for auxi in range (ajuda+1, len(valor)):
									if ativ2 == self.atividades[chave][auxi]:
										controle = True
											
								if controle == False:
									
									self.ordena=[]
							
									for a in original:
										self.ordena.append(a)
										
									indice1=0
									indice2=0
										
									for per in range(0, len(self.ordena)):
										 
										if self.ordena[per]==ativ1:
											indice1 = per
										elif self.ordena[per] == ativ2:
											indice2 = per
									
												
									self.ordena[indice1] = ativ2
									self.ordena[indice2] = ativ1
												
												
									for auxil in range (0, len(valor)):
												
										if auxil > ajuda:
											for per in range(0, len(self.ordena)): 
										
												if self.ordena[per] == self.atividades[chave][auxil]:
													if per < indice2:
														self.ordena[indice2] = self.ordena[per] 
		
														self.ordena[per]=ativ1
																
						
													
										elif auxil < ajuda:
		
										
											for per in range(0, len(self.ordena)): 
												if self.ordena[per] == self.atividades[chave][auxil]:
													if per > indice2:
														self.ordena[indice2] = self.ordena[per] 
														self.ordena[per]=ativ1
										
										
										
									for chav,val in self.atividades.items():
										for a in range (0, len(val)):
											if self.atividades[chav][a]== ativ2:
												for b in range (0,len(val)):
													if b > a:
		
														for per in range(0, len(self.ordena)):
															if self.ordena[per] == self.atividades[chav][b]:
																	
																if per < indice1:
																	self.ordena[indice1] = self.ordena[per] 
																	self.ordena[per]=ativ2
																	
													elif b < a:
													
														for per in range(0, len(self.ordena)): 
															if self.ordena[per] == self.atividades[chav][b]:
																if per > indice1:
																	self.ordena[indice1] = self.ordena[per] 
																	self.ordena[per]=ativ2
																
											
									self.armazena.append(self.ordena[:])							
								
								
		for a in self.armazena:
			self.dia = 1
			for xis in range(0, len(a)):
				ativ = a[xis]
				
				equipe = 1			
					
				for chave,valor in self.rotaEq.items():
					for ajuda in range (0, len(valor)):
						if self.rotaEq[chave][ajuda] == ativ:
							equipe=chave  
					
				maior = 0
				
				for chave, valor in self.atividades.items():
					if len(valor) > maior:
						maior = len(valor)
						

				auxiliar= -1
				talhao = -1
				
				for cont in range(1,iinstancia.talhoes+1):
					for i in range (0, maior-1):
						if self.atividades[cont][i] == ativ:
							auxiliar=i
							talhao=cont
						
				if auxiliar == 0:
							
					if self.rotaEq[equipe][0] == ativ:
						
						self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ] 	
						
						if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): 
							self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) - 
								(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
							self.dia= self.dia + 1
								
						else:
							self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]
									
					else:
						aux = []
						for valor in self.rotaEq[equipe]: 
							aux.append(valor)
						
						anterior = -1
						indiceAntUm = -1
						i= xis-1
						
						while (i>=0):
							for j in aux:
								if a[i] == j and anterior == -1:
									anterior = a[i]
									indiceAntUm= i
							i=i-1
									
						if self.tempoAtividade[anterior-1][1]+ iinstancia.tempoDeslocamento[ativ][anterior] > iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]:	
							self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ]
							self.dia= self.dia+1
									
						else:
							self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1]+ iinstancia.tempoDeslocamento[ativ][anterior]
								
						if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):
							self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) - (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]))
							self.dia= self.dia + 1
							
						else:
							self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]
								
				else:
					
					listaRota = []
					for chave,valor in self.rotaEq.items():
						for ajuda in range (0, len(valor)):
							if self.rotaEq[chave][ajuda] == ativ:
								for x in self.rotaEq[chave]:
									listaRota.append(x)
					
					listaTalhao = []
					for chave,valor in self.atividades.items():
						for ajuda in range (0, len(valor)):
							if self.atividades[chave][ajuda] == ativ:
								for x in self.atividades[chave]:
									listaTalhao.append(x)
					
					anterior = -1
					indiceAntUm = -1
					i= xis-1
						
					while (i>=0):
						for j in listaRota:
							if a[i] == j and anterior == -1:
								anterior = a[i]
								indiceAntUm= i
						i=i-1
					
					anterior2 = -1
					indiceAntDois = -1
					i = xis-1
					
					while (i>=0):
						for j in listaTalhao:
							if a[i] == j and indiceAntDois == -1:
								anterior2 = a[i]
								indiceAntDois= i
						i=i-1
							
					if anterior == anterior2:
								
						self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1] 
						
						if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): 
					
							self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0]+iinstancia.tempoTarefa[equipe-1][ativ-1]) - 
								(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
							self.dia= self.dia + 1
									
						else:
							self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] 
										
					else:	
						if anterior != -1:
							
							if self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] > self.tempoAtividade[anterior2-1][1]:
								
										
								if self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] >(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):
									
									self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ]   
									self.dia = self.dia + 1
								else:
									self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] 
											
								if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]):
									self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -
									(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
									self.dia= self.dia + 1
											
								else:
									self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][i-1]
												
							elif self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior-1][ativ] < self.tempoAtividade[anterior2-1][1]:
										
								self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior2-1][1]
										
								if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] >(iinstancia.turno- iinstancia.tempoDeslocamento[0][ativ]):
									self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + tempoTarefa[equipe-1][ativ-1]) -
									(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]))	
									self.dia= self.dia + 1
										
										
						else:
							
							self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior2-1][1]
									
							if self.tempoAtividade[ativ-1][0]+ iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]):
								self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -
								(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
								self.dia= self.dia + 1
										
							else:
								self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][i-1]
			
	
			if self.dia < menor:
				menor = self.dia	
										
		return int(menor)
