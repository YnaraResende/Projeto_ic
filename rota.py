import Instancia

class Rota:
	
	def __init__(self):
		
		self.rotaEq={}  # dicionario que possui cada equipe relacionada com as atividades que irão realizar (ordenada)
						#chave = equipes
		self.atividades={} #atividades que devem ser concluidas em cada talhao, em ordem de precedencia
		self.tempoAtividade=[] #matriz numAtividades x 2 que armazena atividades com seu tempo de inicio e fim
		self.dia = 1
		self.equipeAtual= None
	
	def CalcularTempo(self,iinstancia,arquivo):
		
		for i in range (1, iinstancia.equipes+1):
			self.rotaEq[i] = [] 	 
	
		for i in range (1, iinstancia.talhoes+1):
			self.atividades[i] = []
		
		for i in range (0, iinstancia.numAtividades-1):
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
		
		maior = 0
		chave_maior = None
		
		for chave, valor in self.atividades.items():
			if len(valor) > maior:
				maior = len(valor)
	
		for auxiliar in range (0, maior-1):
			for cont in range(1,iinstancia.talhoes+1):
				aux =[]
				ativ= self.atividades[cont][auxiliar]
				
				if ativ > 0:
					equipe = 1
					for chave,valor in self.rotaEq.items():
						for ajuda in range (0, len(valor)-1):
							if self.rotaEq[chave][ajuda] == ativ:
								equipe=chave  
					
					if auxiliar == 0:
						
						if self.rotaEq[equipe][0] == ativ:
							self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ] #matriz tempoAtividade recebe na primeira coluna(que armazena tempo de 
							#inicio de cada atividade) tempo de deslocamento da origem para cada atividade	
						
							if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): #se tempo de termino da 
							#atividade for maior que o permitido 
								self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) - 
								(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
								self.dia= self.dia + 1
							
							else:
								self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] #matriz tempoAtividade recebe na segunda 
								#coluna(que armazena tempo final de cada atividade) tempo do inicio da atividade + tempo em que a tarefa foi 
								#executada pela equipe
								
						else:

							for valor in self.rotaEq[equipe]: 
								aux.append(valor)
							
							anterior = 1
							indiceAntUm = 1
							for c in range (0, len(aux)): 
								if aux[c] == ativ: #encontrar atividade na lista aux
									anterior = aux[c-1] #armazenar atividade realizada anteriormente pela equipe
									indiceAntUm = c-1
									
							if self.tempoAtividade[anterior-1][1]+ iinstancia.tempoDeslocamento[ativ][anterior] > iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]:
								self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ]
								self.dia= self.dia+1
								
							else:
								self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1]+ iinstancia.tempoDeslocamento[ativ][anterior]
							
							if self.tempoAtividade[ativ-1][0] + tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):
								self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -
										(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) #tempo final recebe tempo de deslocamento da origem + o tempo restante 
										#para concluir a atividade
								self.dia= self.dia + 1
							else:
								self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + tempoTarefa[equipe-1][ativ-1]
							
					else:

						for chave,valor in self.rotaEq.items():
							for ajuda in range (0, len(valor)-1):
								if self.rotaEq[chave][ajuda] == ativ:
									for ajuda in self.rotaEq[chave]:
										aux.append(valor)
						
						anterior = -1
						indiceAntUm = -1
						
						for c in range (0, len(aux)-1): 
							if aux[c] == ativ: #encontrar atividade na lista aux
								anterior = aux[c-1] #armazenar atividade realizada anteriormente pela equipe
								indiceAntUm = c-1	#e seu indice
									
						anterior2= self.atividades[cont][auxiliar-1]
					
						if anterior == anterior2:
							
							tempoAtividade[ativ-1][0] = tempoAtividade[anterior-1][1] #tempo de inicio da atividade recebe tempo final da anterior
							
							if tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]):#se tempo de 
								#termino for maior que o permitido
								tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((tempoAtividade[ativ-1][0]+iinstancia.tempoTarefa[equipe-1][ativ-1]) - 
									(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) #tempo final recebe tempo de deslocamento da origem + o tempo 
									#restante para concluir a atividade
								self.dia= self.dia + 1
								
							else:
								tempoAtividade[ativ-1][1] = tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] #tempo final recebe tempo de
								# inicio da atividade + tempo que a equipe demora para realizar a atividade
						
								
						else: #se não é do mesmo talhão
							
							if anterior != -1:
								if self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] > self.tempoAtividade[anterior2-1][1]:#se tempo
									#da equipe iniciar a atividade for maior que tempo de termino da atividade anterior do talhao
									
									if self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] >(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):
										#se o tempo final da atividade realizada anteriormente pela equipe + tempo de deslocamento for maior que o permitido
										self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ]   
										self.dia = self.dia + 1
									else:
										self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] #tempo de 
										#inicio recebe tempo final de atividade realizada anteriormente pela equipe + tempo deslocamento 
									
									if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): #se tempo final da 
										#atividade atual for maior que o permitido 
										self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -
											(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) #tempo final recebe tempo de deslocamento da origem + o tempo restante 
											#para concluir a atividade
										self.dia= self.dia + 1
									
									else:
										self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][i-1]
										
								elif self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior-1][ativ] < self.tempoAtividade[anterior2-1][1]:
									
									self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior2-1][1]
									
									if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] >(iinstancia.turno- iinstancia.tempoDeslocamento[0][ativ]):#se tempo final da 
										#atividade atual for maior que o permitido 
										self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + tempoTarefa[equipe-1][ativ-1]) -
											(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]))	#tempo final recebe tempo de deslocamento da origem + o tempo restante 
											#para concluir a atividade
										self.dia= self.dia + 1
									
									
							else:
								self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior2-1][1]
								
								if self.tempoAtividade[ativ-1][0]+ iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): #se tempo final da 
									#atividade atual for maior que o permitido 
									self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -
										(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) #tempo final recebe tempo de deslocamento da origem + o tempo restante 
										#para concluir a atividade
									self.dia= self.dia + 1
									
								else:
									self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][i-1]
								
								
		return int(self.dia)
