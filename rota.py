import Instancia
from random import *



class  Rota:
	
	def __init__(self,iinstancia,arquivo):
		
		
		self.atividades={} 		#atividades que devem ser concluidas em cada talhao, em ordem de precedencia
		self.tempoAtividade=[]  #matriz que armazena atividades com seu tempo de inicio e fim
		self.dia=1				#dias gastos
		self.resposta = None	
		self.pe = 0.70			#probabilidade elite 
		self.pmuta = 0.10		#probabilidade mutacao
		self.pcross = 0.70		#probabilidade crossover
				 
		#recebe dados do arquivo texto
		for i in range (1, iinstancia.talhoes+1):
			self.atividades[i] = []
		
		for i in range (0, iinstancia.numAtividades):
			linha=[]
			for j in range(2):
			 linha.append(0)
			self.tempoAtividade.append(linha)
		
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
			
	
	def CalcularTempo(self,iinstancia,vetoraux,equipes): #funcao para calcular os dias gastos de acordo 
		self.dia = 1
		
		for xis in range(0, len(vetoraux)):
			
			indiceAntUm = -1
			ativ = vetoraux[xis]	#atividade a ser feita	
			equipe = equipes[xis]	#equipe correspondente
			
			if xis == 0:	#se for a primeira atividade da sequencia dada: tempo inicial recebe tempo de deslocamento do deposito e para tempo final 
							#considera tempo de turno 
				
				self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ] 	
				
				if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]): 
					self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) - (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
					self.dia= self.dia + 1
								
				else:
					self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]
				
			
			else:	
				
				auxiliar= -1
				talhao = -1
				
				for c,v in self.atividades.items():		 
					for i in range (0, len(v)):
						if self.atividades[c][i] == ativ:
							auxiliar=i
							talhao=c
				
				if auxiliar == 0:	#se a atividade for a primeira a ser realizada no talhao correspondente
			 
					for i in range (0, xis):
						if equipes[i] == equipe:
							anterior = vetoraux[i]
							indiceAntUm= i 
				
							
					if indiceAntUm == -1:	#se a atividade for a primeira a ser realizada pela equipe correspondente: tempo inicial recebe tempo de 
											#deslocamento do deposito e para tempo final considera tempo de turno
						
						self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ] 	
							
						if (self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) > (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]): 
							self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) - (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
							self.dia= self.dia + 1
									
						else:
							self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]
							
						
					
					else:	#se não: considera para tempo inicial o tempo final e o deslocamento da atividade feita anteriormente pela equipe e 
							#tempo de turno e para tempo final considera tempo de turno
						
						if (self.tempoAtividade[anterior-1][1]+ iinstancia.tempoDeslocamento[ativ][anterior]) > (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):	
							self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ]
							self.dia= self.dia+1
										
						else:
							self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1]+ iinstancia.tempoDeslocamento[ativ][anterior]
									
						if (self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) > (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):
							self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) - (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]))
							self.dia= self.dia + 1
								
						else:
							self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]	
						
							
				
				else:	#se a atividade não for a primeira a ser realizada no talhao
					
					for i in range (0, xis):
						if equipes[i] == equipe:
							anterior = vetoraux[i]
							indiceAntUm= i
					
					anterior2 = self.atividades[talhao][auxiliar-1] 
							
					if indiceAntUm == -1:	#se a atividade for a primeira a ser realizada pela equipe correspondente: para tempo inicial recebe tempo
											#final da ultima atividade feita no talhao e para tempo final considera tempo de turno
						
						self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior2-1][1]
									
						if self.tempoAtividade[ativ-1][0]+ iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): 
							self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1])-(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]))
							self.dia= self.dia + 1
										
						else:
							self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]
					
					else: 
						
						
						if anterior == anterior2:	#se anterior da equipe correspondente for do mesmo talhao: tempo inicial recebe tempo final da 
													#atividade feita pela equipe anteriormente e tempo final considera  tempo de turno
							
							self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1] 
						
							if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): 
					
								self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0]+iinstancia.tempoTarefa[equipe-1][ativ-1]) - 
								(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
								self.dia= self.dia + 1
									
							else:
								self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]
							
					
						else:	#se não: considera como tempo inicial o maior tempo entre o tempo final da atividade realizada anteriormente pela equipe
								# com o deslocamento e o tempo final da atividade anterior do talhao, levando em conta o tempo de turno para o tempo 
								#inicial e final
							
							if self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] > self.tempoAtividade[anterior2-1][1]:
								
								if self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] >(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):
									
									self.tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ]   
									self.dia = self.dia + 1
								else:
									self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] 
											
								if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]): 
									
									self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
									self.dia= self.dia + 1
											
								else:
									self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]
												
							else:
										
								self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior2-1][1]
										
								if self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] >(iinstancia.turno- iinstancia.tempoDeslocamento[0][ativ]):
									self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -
									(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]))
									self.dia= self.dia + 1
							
								else:
									self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]
										
		return self.dia
		
	def BRKGA(self,iinstancia):	#funcao para gerar sequencia de atividades aleatorias
		
		reini=0		#variavel de controle 
		k = iinstancia.equipes			#numero de equipes
		n = iinstancia.numAtividades	#numero de atividades
		
		while reini < 10 :	 
			novaPopulacao=[]
			equipes = []
			contador = 0	#variavel de controle
			
			for i in range (6):		#inicializa matriz novaPopulacao
				lista=[]
				for j in range(0,n):
					lista.append(' ')
				novaPopulacao.append(lista[:])
			
			for i in range(6):		#preenche matriz novaPopulacao com numeros reais de 0 a 1, que representam as atividades e consideram a precedencia
				for c, v in self.atividades.items():
					for ajuda in range (0, len(v)):
						num = self.atividades[c][ajuda]
						if ajuda == 0:
							novaPopulacao[i][num-1] = random()
						else:
							ant = self.atividades[c][ajuda-1]
							maxi = 1 - novaPopulacao[i][ant-1]
							aux = uniform(0.0000000000000001,maxi) 
							novaPopulacao[i][num-1] = novaPopulacao[i][ant-1] + aux 
			
				lista=[]
				for j in range(0, n):	#preenche matriz equipes de acordo com a equipe que correponde a cada numero real da matriz novaPopulacao
					for z in range(1,k+1):
						if (z/k > novaPopulacao[i][j]) and (novaPopulacao[i][j]>= (z-1)/k):
							lista.append(z)
				equipes.append(lista[:])
				
			while contador < 3:
				menor = -1
				
				for i in range(len(novaPopulacao)):		#a cada linha da matriz novaPopulacao preenche vetoraux com os numeros das atividades
										#correspondentes
					vetoraux=[]	
					for j in range (0,n):
						vetoraux.append(novaPopulacao[i][j])
					vetoraux=sorted(vetoraux)
			
					for j in range(0,n):
						for b in range (0,n):
							if vetoraux[j] == novaPopulacao[i][b]:
								vetoraux[j]= b+1
					
					resul = Rota.CalcularTempo(self,iinstancia,vetoraux,equipes[i])		#calcula tempo em dias para cada sequencia de atividades dada
														#pelo vetoraux
					#para armazenar os dois vetores que tiveram menor custo
					if resul <= menor:	
														 
						vetordois= vetorum								
						segmenor = menor
						vetorum = novaPopulacao[i]
						vetorajuda=vetoraux 			#para retornar vetor de atividades no fim
						vetorajudaEquipe= equipes[i]	#para retornar vetor equipe equivalente
						menor= resul	
								
					elif menor == -1:
						
						vetordois= novaPopulacao[i]						
						vetorum=novaPopulacao[i]									
						segmenor= resul
						vetorajuda=vetoraux
						vetorajudaEquipe= equipes[i]
						menor=resul
								
					elif ((resul>menor) and (resul<segmenor)) or vetorum==vetordois:
						segmenor=resul
						vetordois= novaPopulacao[i]
						
					
				
				proximaGeracao=[]					
				proximaGeracao.append(vetorum[:])		#adição dos dois vetores de menor custo da geração anterior na proxima geração 
				proximaGeracao.append(vetordois[:])
				
				vetorProbabilidade=[]
				for b in range(0,n):
					vetorProbabilidade.append(random())	#geração de vetor probabilidade com números gerados aleatoriamente 
				
				indiceElite = []		#armazena indices das linhas correspondentes aos vetores com menores custos 
				indiceNaoElite = []		#armazena indices das linhas correspondentes aos vetores restantes 
				
				for i in range(0,len(novaPopulacao)):
					
					if novaPopulacao[i] == vetorum:
						indiceElite.append(i)
						
					elif novaPopulacao[i] == vetordois:
						indiceElite.append(i)
						
					else:
						indiceNaoElite.append(i)
				
				if len(indiceNaoElite) != 0:	#se a populacao anterior não for formada apenas pelos dois vetores de menor custo
					
					for i in range(2):	#se forem aptos a reproducao forma dois vetores filhos, que respeitam a precedencia das atividades, 
								#originados de um vetor elite outro não elite 
						
						paium = choice(indiceElite)
						paidois = choice(indiceNaoElite)
						
						rand = random()
						
						if rand <= self.pcross:
							vetorFilho = []
							for j in range (0,n):
								
								if vetorProbabilidade[j] <= self.pe:
									vetorFilho.append(novaPopulacao[paium][j])
								else:
									vetorFilho.append(novaPopulacao[paidois][j])
							
							
							for c, v in self.atividades.items():		
								for ajuda in range (0, len(v)):
									if ajuda != 0:
										num = self.atividades[c][ajuda]
										ant = self.atividades[c][ajuda-1]
										if vetorFilho[num-1] <= vetorFilho[ant-1]:
											if (vetorFilho[num-1] + vetorFilho[ant-1]) < 1:
												vetorFilho[num-1] = vetorFilho[num-1] + vetorFilho[ant-1]
											else:
												maxi = 1-vetorFilho[ant-1]
												aux = uniform(0.0000000000000001,maxi) 
												vetorFilho[num-1]= vetorFilho[ant-1]+aux
							
							proximaGeracao.append(vetorFilho[:])	#adição do vetor filho na proxima geração
							
							rand = random()
								
							if rand <= self.pmuta:		#se o vetor filho for apto a mutação, ocorre a troca de posição entre duas atividades, respeitando
											#a ordem de precedencia 
								controle = 0
								
								while controle == 0:
									primeira = 1
									indum = randint(0,(n-1))
									inddois= randint(0,(n-1))
									talhaoum = -1
									talhaodois = -1
									vetaux=vetorFilho
									vetaux=sorted(vetaux)
									
									for j in range(0,n):
										for b in range (0,n):
											if vetaux[j] == vetorFilho[b]:
												vetaux[j]= b+1
									
									for c,v in self.atividades.items():		
										for ajuda in range (0, len(v)):
											if vetaux[indum] == self.atividades[c][ajuda]:
												talhaoum= c
											if vetaux[inddois] == self.atividades[c][ajuda]:
												talhaodois= c
									
									
									if talhaoum != talhaodois:
										
										atividade = vetaux[indum] 
										vetaux[indum] = vetaux[inddois]
										vetaux[inddois] = atividade
										
										for c,v in self.atividades.items():
											for ajuda in range (0, len(v)):
												if vetaux[indum] == self.atividades[c][ajuda]:
													for auxil in range (0, len(v)):
														if auxil > ajuda:
															for a in range (0,n):
																if vetaux[a]== self.atividades[c][auxil]:
																	
																	if a >indum and controle != 0:
																		
																		controle = 1
																	elif a>indum and primeira==1:
																		controle= 1	
																	else:
																		controle = 0
																	primeira = 0
																				
														elif auxil < ajuda:
																	
															for a in range (0,n):
																if vetaux[a] == self.atividades[c][auxil]:		
																	if a < indum and controle != 0:
																		controle = 1
																	elif a < indum and primeira == 1:
																		controle = 1
																			
																	else:
																		controle = 0
												
																	primeira = 0
														elif (len(v))== 1:
															controle = 1
															primeira = 0
															
												elif vetaux[inddois] == self.atividades[c][ajuda]:
													for auxil in range (0, len(v)):
														if auxil > ajuda:
															for a in range (0,n):
																if vetaux[a]== self.atividades[c][auxil]:
																			
																	if a > inddois and controle !=0: 
																		controle = 1
																	
																	elif a > inddois and primeira == 1:
																		controle = 1 
																	else:
																		controle = 0			
																	primeira = 0
																	
														elif auxil < ajuda:
															for a in range (0,n):
																if vetaux[a]== self.atividades[c][auxil]:
																			
																	if a < inddois and controle != 0: 
																		controle = 1
																		
																	elif a<inddois and primeira == 1: 
																		controle = 1		
																	else:
																		controle = 0		
																	primeira = 0
														
														elif (len(v))== 1:
															controle = 1
															primeira = 0
															
								atividadetrocaum = vetaux[indum]-1
								atividadetrocadois = vetaux[inddois]-1
								troca = vetorFilho[atividadetrocaum]
								vetorFilho[atividadetrocaum]=vetorFilho[atividadetrocadois]
								vetorFilho[atividadetrocadois] = troca
								proximaGeracao.append(vetorFilho[:])	#adição do vetor filho após a mutação na proxima geração
								
				novaPopulacao=[]
				novaPopulacao = proximaGeracao					#proximaGeracao vira a nova população para a próxima iteração 
				equipes=[]
				
				m= -1
				for i in range(len(novaPopulacao)):
					
					lista=[]
					
					for j in range(0, n):	#preenche matriz equipes de acordo com a equipe que correponde a cada numero real da atual matriz novaPopulacao
						for z in range(1,k+1):
							if (z/k > novaPopulacao[i][j]) and (novaPopulacao[i][j]>= (z-1)/k):
								lista.append(z)
					equipes.append(lista[:])
					
					vetoraux=[]	
					for j in range (0,n):	#a cada linha da matriz novaPopulacao preenche vetoraux com os numeros das atividades correspondentes		
						vetoraux.append(novaPopulacao[i][j])
					vetoraux=sorted(vetoraux)				
					
					for j in range(0,n):
						for b in range (0,n):
							if vetoraux[j] == novaPopulacao[i][b]:
								vetoraux[j]= b+1
					
					resul = Rota.CalcularTempo(self,iinstancia,vetoraux,equipes[i])		#calcula tempo em dias para cada sequencia de atividades dada
														#pelo vetoraux
					
					if (resul<m) or m == -1:	#armazena menor vetor da populacao atual com menor custo
						m = resul
						auxiliar = vetoraux
						auxiliarEquipe = equipes[i]
				
				if(m < menor):	#se houve otimização do custo: atualiza a melhor rota e o número de dias
					self.resposta = m
					vetorResp= auxiliar
					vetorRespEquipe = auxiliarEquipe
				else: 	#se não: incrementa o contador para que satisfaça o critério de parada
					self.resposta = menor
					vetorResp = vetorajuda
					vetorRespEquipe = vetorajudaEquipe
					contador= contador+1
			
			reini = reini+1	
						
			
			print(vetorResp)
			print(vetorRespEquipe)
			return(self.resposta)		
