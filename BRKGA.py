from Rota import *
from random import *
from threading import Timer
import time 


class BRKGA:
	
	def __init__(self, pe, pmuta, pcross):
		
		self.pe = pe			#probabilidade elite 
		self.pmuta = pmuta		#probabilidade mutacao
		self.pcross = pcross	#probabilidade crossover
		self.resposta = None
		
	''' 	
	Ideia: Quando chamada, a função termina o programa.
		
	'''
	def Fim(self):
		exit()
	
	'''
	Parâmetros:
		iinstancia- objeto da classe Instancia
		arq- arquivo de saída de dados, utilizado para gravar a resposta
			
	Ideia: a função retorna o menor custo dentre todas as listas de sequências de atividades e suas respetivas equipes. Primeiramente é formada uma 
	matriz de números reais para representar as atividades e uma matriz para suas respectivas equipes. Assim, as listas de atividades da matriz são 
	decodificadas e enviadas com sua lista de equipes para a função CalcularRota, para dar inicio a uma nova população, os piores custos são substituídos
	por vetores de atividades gerados pela reprodução e mutação.
		
	'''
	def BRKGA(self,iinstancia,arq):
		
		reini=0							#variável de controle 
		k = iinstancia.equipes			#número de equipes
		n = iinstancia.numAtividades	#número de atividades
		fim = 0.0						#variável que controla fim da execução do programa
		objetoRota = Rota(arq)			#criação de um objeto para acessar os métodos da classe Rota
		inicio = time.time()			#determina tempo de início da execução da função
						
		while reini < 100 :
				
			if (fim - inicio) >= 1800.00:
				arq.write(str(self.resposta))
				BRKGA.Fim(self)
					
			novaPopulacao=[]		
			equipes = []
			contador = 0	#variavel de controle
			respAnterior = -1
				
			if self.resposta != None:
				respAnterior = self.resposta
					
			for i in range (100):		#inicializa matriz novaPopulacao
				lista=[]
				for j in range(0,n):
					lista.append(' ')
				novaPopulacao.append(lista[:])
			
			#preenche matriz novaPopulacao com numeros reais de 0 a 1, que representam as atividades e consideram a precedência destas				
			for i in range(100):		
				for c, v in iinstancia.atividades.items():
					for ajuda in range (0, len(v)):
						num = iinstancia.atividades[c][ajuda]
						if ajuda == 0:
							novaPopulacao[i][num-1] = random()
						else:
							ant = iinstancia.atividades[c][ajuda-1]
							maxi = 1 - novaPopulacao[i][ant-1]
							aux = uniform(0.0000000000000001,maxi) 
							novaPopulacao[i][num-1] = novaPopulacao[i][ant-1] + aux 
				
				lista=[]
				
				#preenche matriz equipes de acordo com a equipe que corresponde a cada atividade da matriz novaPopulacao
				for j in range(0, n):	
					for z in range(1,k+1):
						if (z/k > novaPopulacao[i][j]) and (novaPopulacao[i][j]>= (z-1)/k):
							lista.append(z)
				equipes.append(lista[:])
					
			while contador < 100:
				zis = 1
				indiceElite = []		#armazena indices das linhas correspondentes aos vetores com menores custos 	
				indiceNaoElite = []		#armazena indices das linhas correspondentes aos vetores restantes
				custos = []				#lista que armazena custos dos vetores de atividades
				
				#a cada linha da matriz novaPopulacao preenche vetoraux com os numeros das atividades correspondentes
				for i in range(0,len(novaPopulacao)):		
					vetoraux=[]	
					for j in range (0,n):
						vetoraux.append(novaPopulacao[i][j])
					vetoraux=sorted(vetoraux)
					
					for j in range(0,n):
						for b in range (0,n):
							if novaPopulacao[i][j] == vetoraux[b]:
								vetoraux[b] = j+1
								break
					
					#calcula custo da rota das equipes, baseado no numero de dias dado e na sequência de atividades	
					resul = objetoRota.CalcularRota(iinstancia,vetoraux,equipes[i],iinstancia.dias)		
					custos.append(float(resul))	
						
				#para armazenar os indices dos vinte vetores de menores custos da populacao
				while zis <= 20:		
						
					men= -1.0
						
					#percorre a lista custos armazenando o menor custo, garantindo que nao se repita indice de menor custo
					for j in range(len(custos)):
						ajuda = False
						
						for a in indiceElite:		
							if j == a:
								ajuda = True
												
						if (custos[j] < men) and (ajuda==False):	
							if zis == 1:
								menor = custos[j]
								vetorum = novaPopulacao[j]		#para retornar vetor atividade equivalente	
							men = custos[j]	
							indice = j
												
						elif (men == -1) and (ajuda==False):
							if zis == 1:
								menor = custos[j]
								vetorum = novaPopulacao[j]		#para retornar vetor atividade equivalente
									
							men = custos[j]
							indice = j
							
					indiceElite.append(indice)
					zis = zis+1	
					
				#armazena os indices dos vetores de atividades que não tiveram os menores custos 
				for i in range(len(novaPopulacao)):
					ajuda = False
						
					for j in indiceElite:
						if i == j:
							ajuda = True 
								
					if ajuda == False:
						indiceNaoElite.append(i)
						
				proximaGeracao=[]
				proximaGeracao= novaPopulacao		#proximaGeracao recebe as atividades da novaPopulacao
				vetorProbabilidade=[]
				
				for b in range(0,n):
					vetorProbabilidade.append(random())	#geração de vetorProbabilidade com números gerados aleatoriamente 
						
				for i in range(70):									
												
					#escolha de pais originados de um vetor elite e outro não elite
					paium = choice(indiceElite)
					paidois = choice(indiceNaoElite)
					
					#geração de um número real aleatório para definir se os pais são aptos a reprodução			
					rand = random()
						
					if rand <= self.pcross:		#se forem aptos a reproducao
						
						vetorFilho = []
						
						#para cada número real aleatório relativo à atividade no vetor dos pais
						for j in range (0,n):				
							if vetorProbabilidade[j] <= self.pe: #se o número for menor que a probabilidade elite, recebe o valor do pai elite
								vetorFilho.append(novaPopulacao[paium][j])
					
							else: #se não, recebe o valor do pai não elite
								vetorFilho.append(novaPopulacao[paidois][j])
									
						#reorganizando a formação do vetor filho, respeitando a ordem de precedência	
						for c, v in iinstancia.atividades.items():		
							for ajuda in range (0, len(v)):
								if ajuda != 0:
									num = iinstancia.atividades[c][ajuda]
									ant = iinstancia.atividades[c][ajuda-1]
									if vetorFilho[num-1] <= vetorFilho[ant-1]:
										if (vetorFilho[num-1] + vetorFilho[ant-1]) < 1:
											vetorFilho[num-1] = vetorFilho[num-1] + vetorFilho[ant-1]
										else:	
											maxi = 1-vetorFilho[ant-1]
											aux = uniform(0.0000000000000001,maxi) 
											vetorFilho[num-1]= vetorFilho[ant-1]+aux
												
						maior = -1
							
						#percorre toda a população garantindo que não haja decodificação de atividades iguais
						for i in range(len(proximaGeracao)):
							vetoraux=[]	
									
							for j in range (0,n):
								vetoraux.append(proximaGeracao[i][j])
							vetoraux=sorted(vetoraux)
								
							for j in range(0,n):
								for b in range (0,n):
									if  proximaGeracao[i][j] == vetoraux[b]:
										vetoraux[b] = j+1
										break
												
							#calcula custo da rota das equipes de acordo com número de dias dado e com a sequência de atividades 
							resul = objetoRota.CalcularRota(iinstancia,vetoraux,equipes[i],iinstancia.dias)		
							
							#armazena o índice do vetor de atividades de pior custo	
							if resul > maior:
								maior = resul
								indicemaior=i
							
						#substituicao do vetor de atividades de pior custo com o vetor filho gerado pela reprodução
						for i in range(0,n):
							proximaGeracao[indicemaior][i]=vetorFilho[i]
						
						#geração de um número real aleatório para definir se o vetor filho é apto a mutação	
						rand = random()
									
						if rand <= self.pmuta:	#se for apto a mutação
							controle = 0
								
							#são trocadas de posição duas atividades de talhões diferentes, que respeitem a ordem de precedência após a troca 
							while controle == 0:
								primeira = 1
								indum = randint(0,(n-1))
								inddois= randint(0,(n-1))
									
								talhaoum = -1
								talhaodois = -1
								vetaux=sorted(vetorFilho)
									
								for j in range(0,n):
									for b in range (0,n):
										if vetaux[j] == vetorFilho[b]:
											vetaux[j]= b+1
											
								for c,v in iinstancia.atividades.items():		
											
									for ajuda in range (0, len(v)):
										if vetaux[indum] == iinstancia.atividades[c][ajuda]:
											talhaoum= c
										if vetaux[inddois] == iinstancia.atividades[c][ajuda]:
											talhaodois= c
									
									
								if talhaoum != talhaodois:
												
									atividade = vetaux[indum] 
									vetaux[indum] = vetaux[inddois]
									vetaux[inddois] = atividade
										
									for c,v in iinstancia.atividades.items():
										for ajuda in range (0, len(v)):
											if vetaux[indum] == iinstancia.atividades[c][ajuda]:
												for auxil in range (0, len(v)):
													if auxil > ajuda:
														for a in range (0,n):
															if vetaux[a]== iinstancia.atividades[c][auxil]:				
																if a >indum and controle != 0:
																	controle = 1
																elif a>indum and primeira==1:
																	controle= 1	
																else:	
																	controle = 0
																primeira = 0
																	
																							
													elif auxil < ajuda:
																				
														for a in range (0,n):
															if vetaux[a] == iinstancia.atividades[c][auxil]:		
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
																		
											elif vetaux[inddois] == iinstancia.atividades[c][ajuda]:
												for auxil in range (0, len(v)):
													if auxil > ajuda:
														for a in range (0,n):
															if vetaux[a]== iinstancia.atividades[c][auxil]:
																						
																if a > inddois and controle !=0: 
																	controle = 1
																				
																elif a > inddois and primeira == 1:
																	controle = 1 
																else:
																	controle = 0			
																primeira = 0
																				
													elif auxil < ajuda:
														for a in range (0,n):
															if vetaux[a]== iinstancia.atividades[c][auxil]:
																					
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
									
							maior = -1
								
							#vetor filho após mutação substitui o vetor de atividades de pior custo da população
							for i in range(len(proximaGeracao)):
								vetoraux=[]	
									
								for j in range (0,n):
									vetoraux.append(proximaGeracao[i][j])
								vetoraux=sorted(vetoraux)
						
								for j in range(0,n):
									for b in range (0,n):
										if proximaGeracao[i][j] == vetoraux[b]:
											vetoraux[b]= j+1
											break
					
								#calcula custo da rota das equipes de acordo com número de dias dado e com a sequência de atividades
								resul = objetoRota.CalcularRota(iinstancia,vetoraux,equipes[i],iinstancia.dias)	
								
								if resul > maior:
									maior = resul
									indicemaior=i
									
							for i in range(0,n):
								proximaGeracao[indicemaior][i]=vetorFilho[i]
								
				novaPopulacao=[]
				novaPopulacao = proximaGeracao			#proximaGeracao vira a novaPopulação para a próxima iteração 
				equipes=[]
					 
				m = -1
				for i in range(len(novaPopulacao)):		
					lista=[]
						
					#preenche matriz equipes de acordo com a equipe que correponde a cada número real da atual matriz novaPopulacao
					for j in range(0, n):	
						for z in range(1,k+1):
							if (z/k > novaPopulacao[i][j]) and (novaPopulacao[i][j]>= (z-1)/k):
								lista.append(z)
					equipes.append(lista[:])
					
					vetoraux=[]	
					#a cada linha da matriz novaPopulacao preenche vetoraux com os números das atividades correspondentes	
					for j in range (0,n):		
						vetoraux.append(novaPopulacao[i][j])	
					vetoraux=sorted(vetoraux)				
						
					for j in range(0,n):
						for b in range (0,n):
							if novaPopulacao[i][j] == vetoraux[b]:
								vetoraux[b]= j+1
								break
					
					#calcula custo da rota das equipes de acordo com número de dias dado e com a sequência de atividades
					resul = objetoRota.CalcularRota(iinstancia,vetoraux,equipes[i],iinstancia.dias)		
					
					#armazena o vetor da população atual com menor custo	
					if (resul<m) or m == -1:	
						m = resul
							
						
				#se houve otimização do custo: atualiza o vetor de atividades e o menor custo 
				if(m < menor):	
					self.resposta = m
					
				#se não: incrementa o contador para que satisfaça o critério de parada
				else: 	
					self.resposta = menor		
					contador= contador+1
			
			#incrementa o contador para que satisfaça o critério de parada
			reini=reini+1
			
			#comparar o self.resposta
			if (respAnterior!= -1) and (respAnterior < self.resposta):	
				self.resposta = respAnterior
			
			#atualização do tempo final 
			fim = time.time()
			
		return(self.resposta)
