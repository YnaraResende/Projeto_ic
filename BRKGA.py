from Rota import *
from random import *
from threading import Timer
import time 
from math import ceil


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
		n = iinstancia.numAtividades 	#número de atividades
		fim = 0.0						#variável que controla fim da execução do programa
		objetoRota = Rota(arq)			#criação de um objeto para acessar os métodos da classe Rota
		inicio = time.time()			#determina tempo de início da execução da função
		
						
		while reini < 100 :
				
			if (fim - inicio) >= 1800:
				arq.write(str(self.resposta))
				BRKGA.Fim(self)
					
			novaPopulacao=[]		
			equipes = []
			contador = 0	#variavel de controle
			respAnterior = -1
			matrizAux = []
				
			if self.resposta != None:
				respAnterior = self.resposta
					
			for i in range (300):		#inicializa matriz novaPopulacao
				lista=[]
				for j in range(0,n):
					lista.append(' ')
				novaPopulacao.append(lista[:])
			
			#preenche matriz novaPopulacao com numeros reais de 0 a 1, que representam as atividades e consideram a precedência destas				
			for i in range(300):		
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
				
				lista=[]	#inicialização da lista que vai ser preenchida com as equipes referentes as atividades de cada lista da matriz novaPopulacao
				for c in range(0,n):
					lista.append('')
			
				listaDispo =[]	#lista que irá conter as atividades disponiveis (que ainda não foram destinadas a alguma equipe) 
				for j in range (0,n):	#será equivalente ao vetor de atividades para facilitar o acesso à posição que a equipe deve estar na lista de equipes
					listaDispo.append(novaPopulacao[i][j])
				listaDispo=sorted(listaDispo)
					
				for j in range(0,n):
					for b in range (0,iinstancia.numAtividades):
						if novaPopulacao[i][j] == listaDispo[b]:
							listaDispo[b] = j+1
							break
	
				matrizAux = []	#matriz para simular a distribuição das atividades ao longo dos dias para cada grupo de equipes e facilitar o acesso aos dados
				for c in range (iinstancia.dias):
					listaum = []
					for j in range (iinstancia.equipes):
						lista2 = []
						for z in range (iinstancia.quant[j]):
							lista3 = []
							lista2.append(lista3[:])
						listaum.append(lista2[:])
					matrizAux.append(listaum[:])
				
				contDias = 0	#variavel para controlar o número de dias
				while contDias < iinstancia.dias:
					listaGT=[]	#lista que contem o número de grupos de trabalho já ocupados a cada dia
					lim = False
					
					for c in range (iinstancia.equipes):
						listaGT.append(0)
					
					for talhao in range (iinstancia.talhoes-1):
						#verifica se o talhão já teve todas as suas atividades destinadas a equipes
						ajuda = False
						for a in listaDispo:
							if a == iinstancia.atividades[talhao][len(iinstancia.atividades[talhao])-1]:
								ajuda = True
						if ajuda:
							melhorCB = 0
							
							for z in range (iinstancia.equipes):
								#verifica se alguma outra equipe possui grupos de trabalho disponíveis, assim se a aquipe atual não 
								#possuir grupos de trabalhos disponíveis, mas outras equipes possuir, as outras equipes serão priorizadas 
								for b in range(iinstancia.equipes):
									if z != b:
										if listaGT[b] < iinstancia.quant[b]:
											lim = True
								#se a equipe atual possui grupos de trabalho disponíveis ou se totas as equipes estão com seus grupos de
								#trabalho ocupados
								if (listaGT[z] < iinstancia.quant[z]) or (lim == False):
									
									for a in range (len(matrizAux[contDias][z])):
										
										CB =0
										probExec =0.0
										resto = iinstancia.turno -(iinstancia.tempoDeslocamento[0][talhao+1]+iinstancia.tempoDeslocamento[talhao+1][0])
										for ativ in iinstancia.atividades[talhao]:
											
											#verifica se a atividade atual do talhão ainda está disponível
											cont = False
											for pos in range (0,len(listaDispo)):
												if ativ == listaDispo[pos]:
													cont = True
													break
											
											if cont:
												entrou = False
												#se o grupo de trabalho atual deve finalizar alguma atividade que foi realizada parcialmente
												if matrizAux[contDias][z][a] != [] and probExec == 0.0:
													for b in iinstancia.atividades[talhao]:
														if matrizAux[contDias][z][a][-1][0] == b:
															entrou = True
															break
													#se essa atividade a ser finalizada for do mesmo talhão da atividade atual, se for, essa
													#equipe e seu respectivo grupo de trabalho são priorizados
													if entrou:
														probExec = matrizAux[contDias][z][a][-1][1]
														resto = resto - (probExec* iinstancia.tempoTarefa[(matrizAux[contDias][z][a][-1][0])-1][z])
														if resto <= 0:
															resto = 0
													#se não, contabiliza além do tempo da atividade a ser finalizada o tempo de deslocamento
													else:
														continuar = True
														for c,v in iinstancia.atividades.items():	
															if continuar:	 
																for k in range (0, len(v)):
																	if iinstancia.atividades[c][k] == matrizAux[contDias][z][a][-1][0]:
																		tal=c+1
																		continuar = False
																		break
															else:
																break
														probExec = matrizAux[contDias][z][a][-1][1]
														resto = resto - (probExec* iinstancia.tempoTarefa[(matrizAux[contDias][z][a][-1][0])-1][z])
														resto = resto - iinstancia.tempoDeslocamento[tal][talhao]
														if resto <= 0:
															resto = 0
														
												#contabiliza a proporção executada das atividades 
												if resto - iinstancia.tempoTarefa[ativ-1][z] >= 0:
													resto = resto - iinstancia.tempoTarefa[ativ-1][z]
													probExec = probExec + 1
																			
												elif resto == 0:
													break
																		
												else:
													probExec = probExec + resto/iinstancia.tempoTarefa[ativ-1][z]
													ultAtiv = ativ
													probUlt = resto/iinstancia.tempoTarefa[ativ-1][z]
													break
										#armareza custo beneficio de cada grupo de trabalho da equipe para posteriormente realizar a comparação
										CB = iinstancia.custoEquipe[z]/probExec
										if (CB < melhorCB) or (melhorCB == 0) or entrou:
											melhorProbExec = probExec
											melhorProbUlt = probUlt
											melhorCB = CB
											melhorEquipe = z
											melhorGT = a
											numAtivExec = ceil(melhorProbExec)
											if entrou:
												break
								if entrou:
									break
							#o grupo de trabalho ocupado é contabilizado
							listaGT[melhorEquipe]= listaGT[melhorEquipe]+1
							#a lista da matriz matrizAux ocupada é deletada para evitar inconsistências					
							del(matrizAux[contDias][melhorEquipe][melhorGT])
							
							#se a ultima atividade do talhão foi realizada parcialmente, o número da atividade e sua proporção que falta a ser realizada
							#são armazenados na matrizAux no dia posterior 
							if melhorProbExec != numAtivExec:
								aj = -1
								for aux in range (0,iinstancia.quant[melhorEquipe]):
									if len(matrizAux[contDias+1][melhorEquipe][aux]) == 0:
										aj=aux
										break
								matrizAux[contDias+1][melhorEquipe][aj].append((ultAtiv, (1- melhorProbUlt)))
							
							#as atividades realizadas são destinadas a sua equipe respectiva 
							cont = 0		
							for ativ in iinstancia.atividades[talhao]:
								if cont < numAtivExec :
									for pos in range (len(listaDispo)):
									
										if ativ == listaDispo[pos] and cont < numAtivExec :
											cont = cont + 1								   
											lista[pos] = melhorEquipe+1
											listaDispo[pos] = None
											break
								else: 
									break
					#némero de dias é contabilizado
					contDias = contDias+1 
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
					lista=[]	#inicialização da lista que vai ser preenchida com as equipes referentes as atividades de cada lista da matriz novaPopulacao
					for c in range(0,n):
						lista.append('')
			
					listaDispo =[]	#lista que irá conter as atividades disponiveis (que ainda não foram destinadas a alguma equipe) 
					for j in range (0,n):	#será equivalente ao vetor de atividades para facilitar o acesso à posição que a equipe deve estar na lista de equipes
						listaDispo.append(novaPopulacao[i][j])
					listaDispo=sorted(listaDispo)
						
					for j in range(0,n):
						for b in range (0,iinstancia.numAtividades):
							if novaPopulacao[i][j] == listaDispo[b]:
								listaDispo[b] = j+1
								break

					vetoraux=[]
					for c in range(0,n):
						vetoraux.append(listaDispo[c])
					
					matrizAux = []	#matriz para simular a distribuição das atividades ao longo dos dias para cada grupo de equipes e facilitar o acesso aos dados
					for c in range (iinstancia.dias):
						listaum = []
						for j in range (iinstancia.equipes):
							lista2 = []
							for z in range (iinstancia.quant[j]):
								lista3 = []
								lista2.append(lista3[:])
							listaum.append(lista2[:])
						matrizAux.append(listaum[:])
				
					contDias = 0	#variavel para controlar o número de dias
					while contDias < iinstancia.dias:
						listaGT=[]	#lista que contem o número de grupos de trabalho já ocupados a cada dia
						lim = False
						
						for c in range (iinstancia.equipes):
							listaGT.append(0)
						
						for talhao in range (iinstancia.talhoes-1):
							#verifica se o talhão já teve todas as suas atividades destinadas a equipes
							ajuda = False
							for a in listaDispo:
								if a == iinstancia.atividades[talhao][len(iinstancia.atividades[talhao])-1]:
									ajuda = True
							if ajuda:
								melhorCB = 0
								
								for z in range (iinstancia.equipes):
									#verifica se alguma outra equipe possui grupos de trabalho disponíveis, assim se a aquipe atual não 
									#possuir grupos de trabalhos disponíveis, mas outras equipes possuir, as outras equipes serão priorizadas 
									for b in range(iinstancia.equipes):
										if z != b:
											if listaGT[b] < iinstancia.quant[b]:
												lim = True
									#se a equipe atual possui grupos de trabalho disponíveis ou se totas as equipes estão com seus grupos de
									#trabalho ocupados
									if (listaGT[z] < iinstancia.quant[z]) or (lim == False):
										
										for a in range (len(matrizAux[contDias][z])):
											
											CB =0
											probExec =0.0
											resto = iinstancia.turno -(iinstancia.tempoDeslocamento[0][talhao+1]+iinstancia.tempoDeslocamento[talhao+1][0])
											for ativ in iinstancia.atividades[talhao]:
												
												#verifica se a atividade atual do talhão ainda está disponível
												cont = False
												for pos in range (0,len(listaDispo)):
													if ativ == listaDispo[pos]:
														cont = True
														break
												
												if cont:
													entrou = False
													#se o grupo de trabalho atual deve finalizar alguma atividade que foi realizada parcialmente
													if matrizAux[contDias][z][a] != [] and probExec == 0.0:
														for b in iinstancia.atividades[talhao]:
															if matrizAux[contDias][z][a][-1][0] == b:
																entrou = True
																break
														#se essa atividade a ser finalizada for do mesmo talhão da atividade atual, se for, essa
														#equipe e seu respectivo grupo de trabalho são priorizados
														if entrou:
															probExec = matrizAux[contDias][z][a][-1][1]
															resto = resto - (probExec* iinstancia.tempoTarefa[(matrizAux[contDias][z][a][-1][0])-1][z])
															if resto <= 0:
																resto = 0
														#se não, contabiliza além do tempo da atividade a ser finalizada o tempo de deslocamento
														else:
															continuar = True
															for c,v in iinstancia.atividades.items():	
																if continuar:	 
																	for k in range (0, len(v)):
																		if iinstancia.atividades[c][k] == matrizAux[contDias][z][a][-1][0]:
																			tal=c+1
																			continuar = False
																			break
																else:
																	break
															probExec = matrizAux[contDias][z][a][-1][1]
															resto = resto - (probExec* iinstancia.tempoTarefa[(matrizAux[contDias][z][a][-1][0])-1][z])
															resto = resto - iinstancia.tempoDeslocamento[tal][talhao]
															if resto <= 0:
																resto = 0
															
													#contabiliza a proporção executada das atividades 
													if resto - iinstancia.tempoTarefa[ativ-1][z] >= 0:
														resto = resto - iinstancia.tempoTarefa[ativ-1][z]
														probExec = probExec + 1
																				
													elif resto == 0:
														break
																			
													else:
														probExec = probExec + resto/iinstancia.tempoTarefa[ativ-1][z]
														ultAtiv = ativ
														probUlt = resto/iinstancia.tempoTarefa[ativ-1][z]
														break
											#armareza custo beneficio de cada grupo de trabalho da equipe para posteriormente realizar a comparação
											CB = iinstancia.custoEquipe[z]/probExec
											if (CB < melhorCB) or (melhorCB == 0) or entrou:
												melhorProbExec = probExec
												melhorProbUlt = probUlt
												melhorCB = CB
												melhorEquipe = z
												melhorGT = a
												numAtivExec = ceil(melhorProbExec)
												if entrou:
													break
									if entrou:
										break
								#o grupo de trabalho ocupado é contabilizado
								listaGT[melhorEquipe]= listaGT[melhorEquipe]+1
								#a lista da matriz matrizAux ocupada é deletada para evitar inconsistências					
								del(matrizAux[contDias][melhorEquipe][melhorGT])
								
								#se a ultima atividade do talhão foi realizada parcialmente, o número da atividade e sua proporção que falta a ser realizada
								#são armazenados na matrizAux no dia posterior 
								if melhorProbExec != numAtivExec:
									aj = -1
									for aux in range (0,iinstancia.quant[melhorEquipe]):
										if len(matrizAux[contDias+1][melhorEquipe][aux]) == 0:
											aj=aux
											break
									matrizAux[contDias+1][melhorEquipe][aj].append((ultAtiv, (1- melhorProbUlt)))
								
								#as atividades realizadas são destinadas a sua equipe respectiva 
								cont = 0		
								for ativ in iinstancia.atividades[talhao]:
									if cont < numAtivExec :
										for pos in range (len(listaDispo)):
										
											if ativ == listaDispo[pos] and cont < numAtivExec :
												cont = cont + 1								   
												lista[pos] = melhorEquipe+1
												listaDispo[pos] = None
												break
									else: 
										break
						#número de dias é contabilizado
						contDias = contDias+1 
					equipes.append(lista[:])
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
