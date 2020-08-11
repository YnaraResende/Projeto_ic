from Rota import *
import random
import time
import timeit
from math import ceil
from heapq import heappush, heappop

class BRKGA:
	
	def __init__(self, pe, pmuta, pcross):
		
		self.pe = pe			#probabilidade elite 
		self.pmuta = pmuta		#probabilidade mutacao
		self.pcross = pcross	#probabilidade crossover
		self.resposta = None
		self.menor = None
		self.solucaoFinal = None
	
	'''
	Parâmetros:
		iinstancia - objeto da classe Instancia
		listaAux - lista de atividades
			
	Ideia: a função retorna a lista de equipes e grupos de trabalho que devem ser destinadas as atividades, a equipe com a menor relação 
	custo/proficiencia possui prioridade, após o estabelecimento da lista de equipes por meio do método construtivo, pode haver troca de 
	equipes visando maior variabilidade e diminuição do custo da solução.
		
	'''
	def GRASP(self, iinstancia, listaAux):
		
		#Para facilitar o acesso aos dados
		equipes = iinstancia.equipes
		talhoes = iinstancia.talhoes-1
		ativs = iinstancia.atividades
		tempoTarefa = iinstancia.tempoTarefa
		tempoViagem = iinstancia.tempoDeslocamento
		
		lista=[]	#lista que será preenchida com as equipes das atividades da listaAux
		for c in range(0, iinstancia.numAtividades):
			lista.append('')
			
		tipoTime = []	#lista que armazena as equipes de forma crecente em relação ao menor custo/proficiencia
		for k in range(1, equipes+1):
		   tipoTime.append(k)
		
		tipoTime.sort(key = lambda x: iinstancia.custoEquipe[x-1]/iinstancia.profEquipe[x-1])
		
		numTime = 0
		
		while True:
			
			dia = 0
			eq = tipoTime[numTime]
			
			numGT = iinstancia.quant[eq-1]	#número de grupos de trabalho da equipe
			
			disponivel = {(v+1, ativs[v][0]) for v in range (talhoes)}	#conjunto com todas as atividades disponíveis
			
			solucao = []
			estrutura = []	#armazena em cada dia, custo das equipes X o numero de vezes que as equipes foram utilizadas
			
			#estrutura que armazena para cada grupo de trabalho as atividades pendentes
			pendente = [(None, None) for k in range (numGT)]
			
			#quanto falta para que a atividade seja terminada
			frac = {(v+1, a):1 for v in range(talhoes) for a in ativs[v]}
		
			inacabadas = set()	#conjunto que armazenas as atividades que não foram terminadas
		
			while disponivel or inacabadas:
				
				#armazena o ultimo grupo de trabalho que foi destinado para cada talhão
				quantgt = [None for k in range (talhoes)]
				
				#armazena as rotas traçadas
				solucao.append( [[(0, None, 0, 0)] for k in range(numGT)] )
					
				estrutura.append([0 for k in range (equipes)])
				
				#tupla formada por (grupo de trabalho, equipe, talhao, atividade e tempo de conclusão da atividade)
				eventos = [(t, eq, 0, None, 0) for t in range(numGT)]
				
				while eventos:
					
					(t, k, v, a, q) = heappop(eventos)
					
					#caso a atividade tenha sido concluida, a próxima do talhão fica disponível
					if (v, a) != (0, None) and a+1 < (ativs[v-1][0] + iinstancia.ativTalhao):
						disponivel.add((v, a+1))
					
					#funções para estabelecer tempos de inicio e fim da atividade
					inicio = lambda h, b: q + tempoViagem[ solucao[dia][t][-1][0] ][h]
					
					fim = lambda h, b: inicio(h, b)+ tempoTarefa[b-1][k-1]*frac[(h,b)]
					
					#caso o grupo de trabalho possua atividades pendentes 
					pend = False
					if pendente[t] != (None, None):
						v, a = pendente[t]
						quantgt[v-1] = t
						pend = True
						
					else:
						
						#escolha da atividade a ser feita
						if disponivel:
							aux = []
							for (u, w) in disponivel:
								aux.append((u, w))
							
							if len( disponivel ) != 1:
								aux.sort(key = lambda x: iinstancia.tempoTarefa[(x[-1])-1][eq-1])
								num = ceil( 0.4*len( disponivel ))
								aux = aux[:num] if(num>2) else aux[:2]
								(tal,ativ)  = random.choice(aux)
								
							else:
								ativ = w
								tal = u
																		
							while True:
								
								#caso a atividade não possa ser realizada pelo grupo de trabalho em questão
								if (t != quantgt[tal-1] and quantgt[tal-1] != None) or (inicio(tal, ativ) + tempoViagem[tal][0]> iinstancia.turno):
										
									if len(aux) == 1 :
										ativ = None
										break
									
									else:
										(tal, ativ) = random.choice(aux)
										aux.remove((tal, ativ))
								else:
									break 
							
							#a atividade escolhida não está mais disponível		
							if ativ != None:
								for (u, w) in disponivel:
									
									if ativ == w:
										v, a = (u, w)
										quantgt[v-1] = t
										disponivel.remove((v, a))
										break
					
							
					if ((u, w) != (0, None) and (v, a) != (0, None)) or pend:
						(u, w) = (0, None)
						# se a atividade não pode ser terminada
						if fim(v, a)+ tempoViagem[v][0] > iinstancia.turno: 
							T= iinstancia.turno - tempoViagem[v][0] - inicio(v, a)
							f= T/tempoTarefa[a-1][k-1]
							frac[(v, a)] = frac[(v, a)] - f
							pendente[t] = (v, a)
							inacabadas.add((v, a))
							solucao[-1][t].append((v, a, inicio(v,a), f))  
							solucao[-1][t].append((0, None, iinstancia.turno, 0))
						
						#se a atividade foi terminada	
						else:
							pendente[t] = None, None
							if (v,a) in inacabadas:
								inacabadas.remove((v,a))
								
							for itera in range(0, len(listaAux)):
								if listaAux[itera] == a:
									lista[itera] = (k, t)
									
							heappush(eventos, (t, k, v, a, fim(v, a)))
							solucao[-1][t].append((v, a, inicio(v, a), frac[(v, a)]))
							
					
				dia= dia+1	
			
			maior = 0
			if len(solucao) <= iinstancia.dias:
				
				for j in range(len(solucao)):
					soma = 0
					for k, rota in enumerate(solucao[j]):
						if len(rota)> 1:
							estrutura[j][eq-1] = estrutura[j][eq-1] + iinstancia.custoEquipe[eq-1]
					for k in range (equipes):
						soma = soma + estrutura[j][k]
						if soma > maior:
							maior = soma
							numDia = j			
				break
				
			elif numTime < equipes:
				numTime = numTime + 1
			
			else:
				print("Solução Inválida")
			
		menCusto = 0
		#analisa para todos os grupos de trabalho do dia com maior custo, se há outro grupo de trabalho relativo a uma outra equipe
		#com custo menor, que consiga realizar as atividades no mesmo período de tempo, para que ocorra a troca de equipes
		for g, r in enumerate (solucao[numDia]):
			if len(r) > 1 and r[1][-1] == 1 and r[-1][-1] == 1:
				for e in tipoTime: 
					tempo = 0
					errado = False
					aj = ceil(estrutura[numDia][e-1]/iinstancia.custoEquipe[e-1])
					if (aj < iinstancia.quant[e-1]):
						for (v, a, ini, f) in r:
							if a != None:
								tempo = tempo + tempoViagem[r[-1][0]][v] 

								if tempo + tempoTarefa[a-1][e-1] + tempoViagem[v][0] > iinstancia.turno:
									errado = True
									break
								else:
									tempo = tempo + tempoTarefa[a-1][e-1]
									
						if errado == False:
							if menCusto == 0 or iinstancia.custoEquipe[e-1] < menCusto:
								menCusto = iinstancia.custoEquipe[e-1]
								respEq= e
								respGp = aj
							
				if menCusto != 0:
					for (v, a, ini, f) in r:
						if a != 0:
							for itera in range(0, len(listaAux)):
								if listaAux[itera] == a:
									if respEq != lista[itera][0]:
										lista[itera] = (respEq, respGp)
										break
									else:
										break
		
		
		return lista

	
	'''
	Parâmetros:
		iinstancia - objeto da classe Instancia
		arq - arquivo de saída de dados, utilizado para gravar a resposta
			
	Ideia: a função retorna o menor custo em relação as rotas criadas pela função CalcularRota. Há a criação de populações por meio de números reais, 
		que são decodificados em atividades, a lista de atividades gerada é enviada para a função GRASP, que retorna uma lista formada por equipes e
		seus respectivos de grupos de trabalho. Para dar inicio a uma nova população, as listas de atividades relacionadas aos piores custos são 
		substituídas por novas listas geradas pela reprodução e mutação.
		
	'''
	def BRKGA(self,iinstancia,arq):
		
		reini=0							#variável de controle 
		k = iinstancia.equipes			#número de equipes
		n = iinstancia.numAtividades 	#número de atividades
		fim = 0.0						#variável que controla fim da execução do programa
		objetoRota = Rota(arq)			#criação de um objeto para acessar os métodos da classe Rota
		inicio = time.time()			#determina tempo de início da execução da função
		
		#o critério de parada é estabelecido por 1000 iterações ou 30 minutos				
		while reini < 100 :
			
			if (fim - inicio) >= 120:
				return self.solucaoFinal, self.resposta
				
			#inicialização das variáveis e estrturas		
			novaPopulacao=[]		
			equipes = []
			contador = 0		
			respAnterior = -1
			matrizAux = []
				
			if self.resposta != None:
				respAnterior = self.resposta
					
			for i in range (100):		
				lista=[]
				for j in range(0,n):
					lista.append(' ')
				novaPopulacao.append(lista[:])
			
			#preenche matriz novaPopulacao com numeros reais de 0 a 1, que representam as atividades, considerando a ordem de precedência				
			for i in range(100):		
				for c, v in iinstancia.atividades.items():
					for ajuda in range (0, len(v)):
						num = iinstancia.atividades[c][ajuda]
						if ajuda == 0:
							novaPopulacao[i][num-1] = random.random()		
						else:
							ant = iinstancia.atividades[c][ajuda-1]
							maxi = 1 - novaPopulacao[i][ant-1]
							aux = random.uniform(0.0000000000000001,maxi) 
							novaPopulacao[i][num-1] = novaPopulacao[i][ant-1] + aux 
				
				#decodificação das atividades
				listaAux =[]	 
				for j in range (0,n):	
					listaAux.append(novaPopulacao[i][j])
				listaAux=sorted(listaAux)
					
				for j in range(0,n):
					for b in range (0,iinstancia.numAtividades):
						if novaPopulacao[i][j] == listaAux[b]:
							listaAux[b] = j+1
							break
				
				#formação da lista de equipes e grupos de trabalho			
				lista = BRKGA.GRASP(self,iinstancia, listaAux)
				equipes.append(lista[:])
			
			while contador < 100:
				
				zis = 1
				indiceElite = []		#armazena indices das linhas correspondentes aos vetores com menores custos 	
				indiceNaoElite = []		#armazena indices das linhas correspondentes aos vetores restantes
				custos = []				#lista que armazena custos dos vetores de atividades
				
				#decodificação das atividades
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
					
					#calcula e armazena os custos das rotas 	
					resul = objetoRota.CalcularRota(iinstancia,vetoraux,equipes[i],iinstancia.dias)
					
					custos.append((resul[0], resul[-1]))	
				
				#armazena os indices dos vinte vetores de menores custos da populacao
				while zis <= 20:
							
					men = -1
					indice = 0
					#percorre a lista custos armazenando o menor custo, garantindo que nao se repita indice de menor custo
					for j in range(len(custos)):
						
						if j not in indiceElite:
													
							if custos[j][-1] < men or men == -1:
									
								if zis == 1:
									self.menor = custos[j][-1]
									self.solucaoFinal = custos[j][0]
								men = custos[j][-1]
								indice = j
							
					indiceElite.append(indice)
					zis = zis+1	
				
				#armazena os indices dos vetores de atividades que não tiveram os menores custos 
				for i in range(len(novaPopulacao)):
						
					if i not in indiceElite:
						indiceNaoElite.append(i)
					
				proximaGeracao=[]
				proximaGeracao= novaPopulacao		#proximaGeracao recebe as atividades da novaPopulacao
				vetorProbabilidade=[]
				
				for b in range(0,n):
					vetorProbabilidade.append(random.random())	#geração de vetorProbabilidade com números gerados aleatoriamente 
						
				for i in range(70):									
								
					#escolha de pais originados de um vetor elite e outro não elite
					paium = random.choice(indiceElite)
					paidois = random.choice(indiceNaoElite)
					
					#geração de um número real aleatório para definir se os pais são aptos a reprodução			
					rand = random.random()
						
					if rand <= self.pcross:		#se forem aptos a reproducao
						
						vetorFilho = []
						
						#criação do vetorFilho baseado nos valores dos vetores pais 
						for j in range (0,n):				
							if vetorProbabilidade[j] <= self.pe: 
								vetorFilho.append(novaPopulacao[paium][j])
					
							else: 
								vetorFilho.append(novaPopulacao[paidois][j])
									
						#reorganização do vetor filho, com base na ordem de precedência	
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
											aux = random.uniform(0.0000000000000001,maxi) 
											vetorFilho[num-1]= vetorFilho[ant-1]+aux
												
						maior = -1
							
						#decodificação das atividades
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
												
							#calculo dos custos das rotas
							sol, resul = objetoRota.CalcularRota(iinstancia,vetoraux,equipes[i],iinstancia.dias)		
							
							#armazena o índice do vetor de atividades de pior custo	
							if resul > maior:
								maior = resul
								indicemaior=i
								
						#substituicao do vetor de atividades de pior custo com o vetor filho gerado pela reprodução
						proximaGeracao[indicemaior] = vetorFilho
						
							
						rand = random.random()
									
						if rand <= self.pmuta:	#se o vetor filho for apto a mutação
							controle = 0
								
							#permutação de duas atividades de talhões diferentes, respeitando a ordem de precedência 
							while controle == 0:
								
								primeira = 1
								indum = random.randint(0,(n-1))
								inddois= random.randint(0,(n-1))
									
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
								
							#substituição do vetor de atividades de pior custo da população pelo vetor filho mutado
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
								
								#calculo do custo das rotas 
								sol, resul = objetoRota.CalcularRota(iinstancia,vetoraux,equipes[i],iinstancia.dias)	
								
								if resul > maior:
									maior = resul
									indicemaior=i
							
							proximaGeracao[indicemaior]=vetorFilho
				
								
				novaPopulacao=[]
				novaPopulacao = proximaGeracao			#proximaGeracao vira a novaPopulação para a próxima iteração 
				equipes=[]
					 
				m = -1
				for i in range(len(novaPopulacao)):		
					
					lista=[]	
					for c in range(0,n):
						lista.append('')
					
					#decodificação de equipes
					listaAux =[]	 
					for j in range (0,n):	
						listaAux.append(novaPopulacao[i][j])
					listaAux=sorted(listaAux)
						
					for j in range(0,n):
						for b in range (0,iinstancia.numAtividades):
							if novaPopulacao[i][j] == listaAux[b]:
								listaAux[b] = j+1
								break

					vetoraux=[]
					for c in range(0,n):
						vetoraux.append(listaAux[c])
					
					lista = BRKGA.GRASP(self,iinstancia, listaAux) 
					equipes.append(lista[:])
					#calculo do custos das rotas 
					sol, resul = objetoRota.CalcularRota(iinstancia,vetoraux,equipes[i],iinstancia.dias)		
					
					#armazena o vetor da população atual com menor custo	
					if (resul < m) or m == -1:	
						m = resul
						menorSolucao = sol
						
				#se houve otimização do custo, há atualização da resposta 
				if(m < self.menor):	
					self.resposta = m
					self.solucaoFinal = menorSolucao
					
				#se não, há o incremento o contador que satisfaz o critério de parada
				else: 	
					self.resposta = self.menor		
					contador= contador+1
			
			#incrementa o contador para que satisfaça o critério de parada
			reini=reini+1
			
			#comparar o self.resposta
			if (respAnterior!= -1) and (respAnterior < self.resposta):	
				self.resposta = respAnterior
			
			#atualização do tempo final 
			fim = time.time()
		
		return self.resposta, self.solucaoFinal
