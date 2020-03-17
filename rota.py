import Instancia
from random import *
from threading import Timer
import time 

class  Rota:
		def __init__(self,iinstancia,arquivo):
			
			
			self.atividades={} 		#atividades que devem ser concluidas em cada talhao, em ordem de precedencia
			self.tempoAtividade=[]  #matriz que armazena atividades com seu tempo de inicio e fim
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
				
			linha = arquivo.readline()
			
			for i in range (1,iinstancia.talhoes):
				linha = arquivo.readline()
				espaco = linha.split()
				cont = int(espaco[1])
				ite = 2
				while cont != -1:
					self.atividades[i].append(cont)
					cont = int(espaco[ite])
					ite = ite+1
		
						
			linha = arquivo.readline()
				
				
			for i in range (0, iinstancia.talhoes):
				linha = arquivo.readline()
				espaco =  linha.split()
				tmp = []
				for j in range (0,iinstancia.talhoes):
					elemento = float(espaco[j])
					tmp.append(elemento)
				iinstancia.tempoDeslocamento.append(tmp[:])
			
			linha = arquivo.readline()
			linha = arquivo.readline()
			espaco =  linha.split()
			for i in range (0, iinstancia.numAtividades):
				elemento=float(espaco[i])
				iinstancia.tempoPadrao.append(elemento)
			
			linha = arquivo.readline()
			linha = arquivo.readline()
			espaco =  linha.split()
			for i in range (0, iinstancia.talhoes):
				elemento=float(espaco[i])
				iinstancia.tamCliente.append(elemento)
			
			linha = arquivo.readline()
			linha = arquivo.readline()
			espaco =  linha.split()
			for i in range (0, iinstancia.equipes):
				elemento=float(espaco[i])
				iinstancia.profEquipe.append(elemento)
			
			linha = arquivo.readline()
			linha = arquivo.readline()
			espaco =  linha.split()
			for i in range (0, iinstancia.equipes):
				elemento=float(espaco[i])
				iinstancia.custoEquipe.append(elemento)
			
			
		def CalcularRota(self,iinstancia,vetoraux,equipes,dias,arq): #funcao para otimizar custo de equipe de acordo com numero de dias
			
			
			solucao =[]		#matriz que armazena rotas das equipes em cada dia
			listaDias=[]	#lista do tamanho do numero de equipes para armazenar o dia atual de cada equipe
			existe = False	#booleano para controle
			
			for i in range (iinstancia.dias):	
				lista=[]
				for j in range(iinstancia.equipes):
					lista2=[]
					lista.append(lista2[:])
				solucao.append(lista[:])
				
			
			for i in range(iinstancia.dias):		#inicialização da matriz solucao com a tupla que representa o deposito
				for k in range(iinstancia.equipes):
					solucao[i][k].append((0, None, 0, 0))
			
			ativ = None
			talhao = None
			horaIni = None
			propExecutada = None
			tempoOcioso = 0.0
			
			for j in range(iinstancia.equipes):		#inicialização da lista listaDias  
				listaDias.append(0)
			

			for xis in range(0, len(vetoraux)):
				equipe = equipes[xis]	#equipe correspondente
	
				if listaDias[equipe-1] < iinstancia.dias:	#se o dia atual da equipe for menor que o numero de dias dado 
					ativ = vetoraux[xis]	#atividade a ser feita	
					auxiliar= -1
					indiceAntUm = -1
						
					for c,v in self.atividades.items():		 
						for i in range (0, len(v)):
							if self.atividades[c][i] == ativ:
								auxiliar=i
								talhao=c
					
					#calculo do tempo de realização da atividade 				
					tempoTarefa = (iinstancia.tamCliente[talhao]*iinstancia.tempoPadrao[ativ-1])/iinstancia.profEquipe[equipe-1]
				
					if xis == 0:	#se for a primeira atividade da sequencia dada: tempo inicial recebe tempo de deslocamento do deposito e tempo 
									#final considera tempo de turno 
						
						horaIni = iinstancia.tempoDeslocamento[0][talhao] 	
						self.tempoAtividade[ativ-1][0] = horaIni
						
						if horaIni + tempoTarefa > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]): 
							propExecutada= (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao] - horaIni)/tempoTarefa
							tempoGasto=((iinstancia.tamCliente[talhao]*iinstancia.tempoPadrao[ativ-1])/iinstancia.profEquipe[equipe-1])*propExecutada
							
							solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
							temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
							solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
							
							listaDias[equipe-1] = listaDias[equipe-1] +1	
							
							if listaDias[equipe-1] < iinstancia.dias:	#se nao ultrapassou o numero de dias dado	
								
								propExecutada= 1- propExecutada		
								tempoGasto=tempoTarefa-tempoGasto
								
								solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
								temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
								existe = False
								
								for z in range(xis+1, len(vetoraux)):	#para verificar se há atividades a serem feitas pela mesma equipe ainda
									if  equipe == equipes[z]:
										existe = True
										
								if existe == False:		#se  não há atividades a serem feitas pela mesma equipe
									solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
									if temp < 8.0:
										tempoOcioso= tempoOcioso + (8.0 - temp)
									
								self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
								
						else:
							
							solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
							self.tempoAtividade[ativ-1][1] = horaIni + tempoTarefa
							temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
							existe = False
										
							for z in range(xis+1, len(vetoraux)):	#para verificar se há atividades a serem feitas pela mesma equipe ainda
								if  equipe == equipes[z]:
									existe = True
							if existe == False :		#se  não há atividades a serem feitas pela mesma equipe
								solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
								if temp < 8.0:
									tempoOcioso= tempoOcioso + (8.0 - temp)
								
					
					else:		#se não for a primeira atividade da sequencia dada no vetoraux
						
						for i in range (0, xis):
							if equipes[i] == equipe:
								anterior = vetoraux[i]
								indiceAntUm= i
									
						if auxiliar == 0:	#se a atividade for a primeira a ser realizada no talhao correspondente 
				
							
							if indiceAntUm == -1:	#se a atividade for a primeira a ser realizada pela equipe correspondente: tempo inicial recebe tempo de 
													#deslocamento do deposito e para tempo final considera tempo de turno
													
								horaIni = iinstancia.tempoDeslocamento[0][talhao] 	
								self.tempoAtividade[ativ-1][0] = horaIni
							
								if horaIni + tempoTarefa > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]): 
									propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
									tempoGasto=((iinstancia.tamCliente[talhao]*iinstancia.tempoPadrao[ativ-1])/iinstancia.profEquipe[equipe-1])*propExecutada
									solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
									temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
									solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
									listaDias[equipe-1] = listaDias[equipe-1]+1	
									
									if listaDias[equipe-1]< iinstancia.dias:		#se nao ultrapassou o numero de dias dado
								
										propExecutada= 1- propExecutada		
										tempoGasto=tempoTarefa-tempoGasto
										solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
										temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
										existe = False
										
										for z in range(xis+1, len(vetoraux)):		#para verificar se há atividades a serem feitas pela mesma equipe ainda
											if  equipe == equipes[z]:
												existe = True
										if existe == False:		#se  não há atividades a serem feitas pela mesma equipe
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso = tempoOcioso + (8.0 - temp)
										self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
						
									
								else:
									
									solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
									self.tempoAtividade[ativ-1][1] = horaIni + tempoTarefa
									temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
									existe = False
										
									for z in range(xis+1, len(vetoraux)):		#para verificar se há atividades a serem feitas pela mesma equipe ainda
										if  equipe == equipes[z]:
											existe = True
									if existe == False :		#se o tempo de turno foi esgotado ou se  não há atividades a serem feitas
																			#pela mesma equipe
										solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
										if temp < 8.0:
											tempoOcioso = tempoOcioso + (8.0 - temp)
					
							else:	#se não: considera para tempo inicial o tempo final com o tempo deslocamento da atividade feita anteriormente pela equipe e 
									#tempo de turno e para tempo final considera o tempo da tarefa com o tempo de turno
									
								talhaoAnt= solucao[listaDias[equipe-1]][equipe-1][-1][0]
								propExecutadaAnt = solucao[listaDias[equipe-1]][equipe-1][-1][-1]
								tempoGastoAnterior =((iinstancia.tamCliente[talhaoAnt]* iinstancia.tempoPadrao[anterior-1])/iinstancia.profEquipe[equipe-1])*propExecutadaAnt
								
								if (solucao[listaDias[equipe-1]][equipe-1][-1][2]+ tempoGastoAnterior + iinstancia.tempoDeslocamento[talhaoAnt][talhao])> iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]:
									temp = solucao[listaDias[equipe-1]][equipe-1][-1][2]+ tempoGastoAnterior+ iinstancia.tempoDeslocamento[talhaoAnt][0]
									solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
									horaIni = iinstancia.tempoDeslocamento[0][talhao] 
									self.tempoAtividade[ativ-1][0] = horaIni
									listaDias[equipe-1] = listaDias[equipe-1]+1	
									
									
								else:
									horaIni = solucao[listaDias[equipe-1]][equipe-1][-1][2]+ tempoGastoAnterior + iinstancia.tempoDeslocamento[talhaoAnt][talhao]
									self.tempoAtividade[ativ-1][0] = horaIni
									#temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
									
									
								if (horaIni + tempoTarefa) > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]):
									propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
									tempoGasto=((iinstancia.tamCliente[talhao]*iinstancia.tempoPadrao[ativ-1])/iinstancia.profEquipe[equipe-1])*propExecutada
									if listaDias[equipe-1] < iinstancia.dias: 
										solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
										temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
										solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
									
									listaDias[equipe-1] = listaDias[equipe-1]+1	
									
									if listaDias[equipe-1]< iinstancia.dias:		
										horaIni= iinstancia.tempoDeslocamento[0][talhao]
										propExecutada= 1- propExecutada		
										tempoGasto=tempoTarefa-tempoGasto
										solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
										temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
										existe = False
										
										for z in range(xis+1, len(vetoraux)):		#para verificar se há atividades a serem feitas pela mesma equipe ainda
											if  equipe == equipes[z]:
												existe = True
												
										if existe == False:		#se o tempo de turno foi esgotado ou se  não há atividades a serem feitas
																				#pela mesma equipe
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso = tempoOcioso + (8.0 - temp)
											
									
										self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
								
								else:
									if listaDias[equipe-1]< iinstancia.dias:
										solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
										self.tempoAtividade[ativ-1][1] = horaIni + tempoTarefa
										temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
										existe = False
											
										for z in range(xis+1, len(vetoraux)):		#para verificar se há atividades a serem feitas pela mesma equipe ainda
											if  equipe == equipes[z]:
												existe = True
										if existe == False :		#se o tempo de turno foi esgotado ou se  não há atividades a serem feitas
																				#pela mesma equipe
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso = tempoOcioso + (8.0 - temp)
						
						else:	#se a atividade não for a primeira a ser realizada no talhao	
							
							for i in range (0, xis):
								if equipes[i] == equipe:
									anterior = vetoraux[i]
									indiceAntUm= i
					
							anterior2 = self.atividades[talhao][auxiliar-1] 	
							
							if indiceAntUm == -1:	#se a atividade for a primeira a ser realizada pela equipe correspondente: para tempo inicial recebe tempo
													#final da ultima atividade feita no talhao e para tempo final considera tempo de turno
						
								self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior2-1][1]
								horaIni = self.tempoAtividade[ativ-1][0]
								tempoOcioso = tempoOcioso + max((self.tempoAtividade[anterior2-1][1]- iinstancia.tempoDeslocamento[0][talhao]),0)
									
								if horaIni+ tempoTarefa > (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]): 
									
									propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
									tempoGasto=((iinstancia.tamCliente[talhao]*iinstancia.tempoPadrao[ativ-1])/iinstancia.profEquipe[equipe-1])*propExecutada
									
									solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
									temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
									solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
									listaDias[equipe-1] = listaDias[equipe-1]+1	
									if listaDias[equipe-1]< iinstancia.dias:		
										horaIni= iinstancia.tempoDeslocamento[0][talhao]
										propExecutada= 1- propExecutada		
										tempoGasto=tempoTarefa-tempoGasto
										solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
										temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
										existe = False
										
										for z in range(xis+1, len(vetoraux)):		#para verificar se há atividades a serem feitas pela mesma equipe ainda
											if  equipe == equipes[z]:
												
												existe = True
												
										if existe == False :			#se o tempo de turno foi esgotado ou se  não há atividades a serem feitas
																					#pela mesma equipe
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso =  tempoOcioso + (8.0 -temp)
									
										self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
									
								
									
								else:
									self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + tempoTarefa
									solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
									temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
									existe = False
										
									for z in range(xis+1, len(vetoraux)):		#para verificar se há atividades a serem feitas pela mesma equipe ainda
										if  equipe == equipes[z]:
											existe = True
											
									if existe == False :			#se o tempo de turno foi esgotado ou se  não há atividades a serem feitas
																				#pela mesma equipe
										solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
										if temp < 8.0:
											tempoOcioso =  tempoOcioso + (8.0 -temp)
					
							else: 
								
								if anterior == anterior2:	#se anterior da equipe correspondente for do mesmo talhao: tempo inicial recebe tempo final da 
															#atividade feita pela equipe anteriormente e tempo final considera  tempo de turno
							
									self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1]
									horaIni= self.tempoAtividade[ativ-1][0]
									 
						
									if horaIni + tempoTarefa> (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]): 
					
										propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
										tempoGasto=((iinstancia.tamCliente[talhao]*iinstancia.tempoPadrao[ativ-1])/iinstancia.profEquipe[equipe-1])*propExecutada
										
										solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
										temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
										solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
										listaDias[equipe-1] = listaDias[equipe-1]+1	
										if listaDias[equipe-1] < iinstancia.dias:		
											horaIni= iinstancia.tempoDeslocamento[0][talhao]
											propExecutada= 1- propExecutada		
											tempoGasto=tempoTarefa-tempoGasto
											solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
											temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
											existe = False
										
											for z in range(xis+1, len(vetoraux)):		#para verificar se há atividades a serem feitas pela mesma equipe ainda
												if  equipe == equipes[z]:
													existe = True
													
											if existe == False:			#se o tempo de turno foi esgotado ou se  não há atividades a serem feitas
																						#pela mesma equipe
												solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
												if temp < 8.0:
													tempoOcioso =  tempoOcioso + (8.0 -temp)
									
											self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
									
									else:
										self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + tempoTarefa
										solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
										temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
										existe = False
										
										for z in range(xis+1, len(vetoraux)):	#para verificar se há atividades a serem feitas pela mesma equipe ainda
											if  equipe == equipes[z]:
												existe = True
												
										if existe == False :		#se o tempo de turno foi esgotado ou se  não há atividades a serem feitas
																				#pela mesma equipe
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso =  tempoOcioso + (8.0 -temp)
										
							
								else:	#se não: considera como tempo inicial o maior tempo entre o tempo final da atividade realizada anteriormente pela equipe
										# com o deslocamento e o tempo final da atividade anterior do talhao, levando em conta o tempo de turno para o tempo 
										#inicial e final
									talhaoAnt= solucao[listaDias[equipe-1]][equipe-1][-1][0]
									propExecutadaAnt = solucao[listaDias[equipe-1]][equipe-1][-1][-1]
									tempoGastoAnterior =((iinstancia.tamCliente[talhaoAnt]* iinstancia.tempoPadrao[anterior-1])/iinstancia.profEquipe[equipe-1])*propExecutadaAnt
									
									if self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[talhaoAnt][talhao] > self.tempoAtividade[anterior2-1][1]:
								
										propExecutadaAnt = solucao[listaDias[equipe-1]][equipe-1][-1][-1]
										tempoGastoAnterior =((iinstancia.tamCliente[talhaoAnt]* iinstancia.tempoPadrao[anterior-1])/iinstancia.profEquipe[equipe-1])*propExecutadaAnt
										if (solucao[listaDias[equipe-1]][equipe-1][-1][2]+ tempoGastoAnterior + iinstancia.tempoDeslocamento[talhaoAnt][talhao])> iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]:
											temp = solucao[listaDias[equipe-1]][equipe-1][-1][2]+ tempoGastoAnterior + iinstancia.tempoDeslocamento[talhaoAnt][0]
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											listaDias[equipe-1] = listaDias[equipe-1]+1	 
											horaIni = iinstancia.tempoDeslocamento[0][talhao] 
											self.tempoAtividade[ativ-1][0] = horaIni
											
											
										else:
											horaIni = solucao[listaDias[equipe-1]][equipe-1][-1][2]+ tempoGastoAnterior + iinstancia.tempoDeslocamento[talhaoAnt][talhao]
											self.tempoAtividade[ativ-1][0]= horaIni
											
											
										if (horaIni + tempoTarefa) > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]):
											propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
											tempoGasto=((iinstancia.tamCliente[talhao]*iinstancia.tempoPadrao[ativ-1])/iinstancia.profEquipe[equipe-1])*propExecutada
											if listaDias[equipe-1] < iinstancia.dias:
												solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
												temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
												solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											
											listaDias[equipe-1] = listaDias[equipe-1]+1	
											
											if listaDias[equipe-1]< iinstancia.dias:		
												horaIni= iinstancia.tempoDeslocamento[0][talhao]
												propExecutada= 1- propExecutada		
												tempoGasto=tempoTarefa-tempoGasto
												solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
												temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
												
												existe = False
												
												
												
												for z in range(xis+1, len(vetoraux)):		#para verificar se há atividades a serem feitas pela mesma equipe ainda
													if  equipe == equipes[z]:	
														
														existe = True
														
												if existe==False:		#se o tempo de turno foi esgotado ou se  não há atividades a serem feitas
																						#pela mesma equipe
													solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
													if temp < 8.0:
														tempoOcioso =  tempoOcioso + (8.0 -temp)
													
												self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
									
										else:
											if listaDias[equipe-1] < iinstancia.dias:
												solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
												temp = horaIni + tempoTarefa + iinstancia.tempoDeslocamento[0][talhao]
												existe = False
											
												for z in range(xis+1, len(vetoraux)):		#para verificar se há atividades a serem feitas pela mesma equipe ainda
													if  equipe == equipes[z]:
														existe = True
												if existe==False:		#se  não há atividades a serem feitas pela mesma equipe
													solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
													if temp < 8.0:
														tempoOcioso =  tempoOcioso + (8.0 -temp)
												self.tempoAtividade[ativ-1][1] = horaIni+ tempoTarefa
								
									else:
										self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior2-1][1]
										horaIni = self.tempoAtividade[ativ-1][0]
										tempoChegada = self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[talhaoAnt][talhao]
										tempoOcioso = tempoOcioso + max((self.tempoAtividade[anterior2-1][1]- tempoChegada),0)
										
										if (horaIni + tempoTarefa) > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]):
											propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
											tempoGasto=((iinstancia.tamCliente[talhao]*iinstancia.tempoPadrao[ativ-1])/iinstancia.profEquipe[equipe-1])*propExecutada
											solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
											temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											listaDias[equipe-1] = listaDias[equipe-1]+1	
											if listaDias[equipe-1]< iinstancia.dias:		
												horaIni= iinstancia.tempoDeslocamento[0][talhao]
												propExecutada= 1- propExecutada		
												tempoGasto=tempoTarefa-tempoGasto
												solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
												temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
												existe = False
										
												for z in range(xis+1, len(vetoraux)):	#para verificar se há atividades a serem feitas pela mesma equipe ainda
													if  equipe == equipes[z]:
														existe = True
														
												if existe == False:		#se o tempo de turno foi esgotado ou se  não há atividades a serem feitas	
																						#pela mesma equipe
													solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
													if temp < 8.0:
														tempoOcioso = tempoOcioso + (8.0-temp)
												self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
										
										else:
											solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
											temp = horaIni + tempoTarefa + iinstancia.tempoDeslocamento[0][talhao]
											existe = False
										
											for z in range(xis+1, len(vetoraux)):	#para verificar se há atividades a serem feitas pela mesma equipe ainda
												if  equipe == equipes[z]:
													existe = True
											if existe == False:		#se o tempo de turno foi esgotado ou se  não há atividades a serem feitas	
																					#pela mesma equipe
												solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
												if temp < 8.0:
													tempoOcioso =  tempoOcioso + (8.0 -temp)
												
											self.tempoAtividade[ativ-1][1] = horaIni+tempoTarefa
				
			custoTotal = 0.0
			tempoUltra = 0.0
			maiorCusto = 0.0
			for j in iinstancia.custoEquipe:
				if j > maiorCusto:
					maiorCusto = j
			penalidade = 3 * maiorCusto
			arq.write("------------------------------\n")
			arq.write(str(vetoraux))
			arq.write("\n")
			for dia in range(len(solucao)):
				prim = 0
				for equi in range(len(solucao[dia])):
					if(len(solucao[dia][equi])>1):
						if prim == 0 :
							arq.write('dia')
							arq.write(str(dia))
							arq.write("\n")
							prim = 1	
						arq.write('    Equipe')
						arq.write(str(equi))
						arq.write('->')
						arq.write(str(solucao[dia][equi])) 
						arq.write("\n")
						tempoUltra= tempoUltra + max( ((solucao[dia][equi][(len(solucao[dia][equi]))-1][2]) - 8),0)
						custoTotal= custoTotal + iinstancia.custoEquipe[equi] 
			arq.write("\n")
			custoTotal= custoTotal + (tempoUltra * penalidade) + tempoOcioso
			arq.write(str(custoTotal))
			arq.write("\n")
			
			
			return(custoTotal)
	
		def Fim(self):
			exit()
			
		
		def BRKGA(self,iinstancia,arq):	#funcao para gerar sequencia de atividades aleatorias
			
			reini=0		#variavel de controle 
			k = iinstancia.equipes			#numero de equipes
			n = iinstancia.numAtividades	#numero de atividades
			fim = 0.0
			inicio = time.time()
						
			while reini < 100 :
			
				if fim - inicio >= 1800.0:
					Rota.Fim(self)
					
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
				
				for i in range(100):		#preenche matriz novaPopulacao com numeros reais de 0 a 1, que representam as atividades e consideram a precedencia
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
					for j in range(0, n):	#preenche matriz equipes de acordo com a equipe que corresponde a cada numero real da matriz novaPopulacao
						for z in range(1,k+1):
							if (z/k > novaPopulacao[i][j]) and (novaPopulacao[i][j]>= (z-1)/k):
								lista.append(z)
					equipes.append(lista[:])
					
				while contador < 100:
					zis = 1
					indiceElite = []		#armazena indices das linhas correspondentes aos vetores com menores custos 
					indiceNaoElite = []		#armazena indices das linhas correspondentes aos vetores restantes
					custos = []				#lista que armazena custos dos vetores de atividades
					
				
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
						
						resul = Rota.CalcularRota(self,iinstancia,vetoraux,equipes[i],iinstancia.dias,arq)		#calcula custo de rota das equipes de acordo com numero 
																											# de dias dado e sequencia de atividades dada pelo vetoraux
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
									vetorajudaEquipe= equipes[j]	#para retornar vetor equipe equivalente	
								men = custos[j]	
								indice = j
												
							elif (men == -1) and (ajuda==False):
								if zis == 1:
									menor = custos[j]
									vetorum = novaPopulacao[j]		#para retornar vetor atividade equivalente
									vetorajudaEquipe= equipes[j]	#para retornar vetor equipe equivalente
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
					proximaGeracao= novaPopulacao		#proximaGeracao recebe as atividades da nova população 
					
					vetorProbabilidade=[]
					for b in range(0,n):
						vetorProbabilidade.append(random())	#geração de vetor probabilidade com números gerados aleatoriamente 
						
					for i in range(70):									
												
						#escolha de pais originados de um vetor elite outro não elite
						paium = choice(indiceElite)
						paidois = choice(indiceNaoElite)
								
						rand = random()
						
						if rand <= self.pcross:		#se forem aptos a reproducao
							
							#formação do vetor filho, respeitando a ordem de precedencia
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
												
							maior = -1
							
							#percorre toda a população garantindo que não haja decodificação de atividades iguais e armazenando o indice do
							#vetor de atividades de maior custo
							for i in range(len(proximaGeracao)):
								vetoraux=[]	
									
								for j in range (0,n):
									vetoraux.append(proximaGeracao[i][j])
								vetoraux=sorted(vetoraux)
								
								for j in range (0,n):
									for b in range (j+1,n):
										if proximaGeracao[i][j] == proximaGeracao[i][b]:
											indicePrim = j
											indiceSeg = b
											
								for j in range(0,n):
									for b in range (0,n):
										if vetoraux[j] == proximaGeracao[i][b]:
											vetoraux[j]= b+1
											
					
								for a in range(0,len(vetoraux)):
									for b in range(a+1,len(vetoraux)):
										if a != b:
											if vetoraux[a] == vetoraux[b]:
												
												vetoraux[b] = indiceSeg+1
												
								
								resul = Rota.CalcularRota(self,iinstancia,vetoraux,equipes[i],iinstancia.dias,arq)		#calcula custo de rota das equipes de acordo com numero 
																													# de dias dado e sequencia de atividades dada pelo vetoraux
								
								if resul > maior:
									maior = resul
									indicemaior=i
							
							#substituicao do vetor de atividades de maior custo com o vetor filho gerado na reproducao
							for i in range(0,n):
								proximaGeracao[indicemaior][i]=vetorFilho[i]
							
							rand = random()
								
							#se vetor filho for apto a mutacao		
							if rand <= self.pmuta:
								controle = 0
								
								#duas atividades de talhoes diferentes e que respeitem a ordem de precedencia após a troca sao trocadas de posicao 
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
								
								
								maior = -1
								
								#vetor apos mutacao substitui vetor de atividades de maior custo da populacao
								for i in range(len(proximaGeracao)):
									vetoraux=[]	
									
									for j in range (0,n):
										vetoraux.append(proximaGeracao[i][j])
									vetoraux=sorted(vetoraux)
						
									for j in range(0,n):
										for b in range (0,n):
											if vetoraux[j] == proximaGeracao[i][b]:
												vetoraux[j]= b+1
									
									
									resul = Rota.CalcularRota(self,iinstancia,vetoraux,equipes[i],iinstancia.dias,arq)	#calcula custo de rota das equipes de acordo com numero 
																													# de dias dado e sequencia de atividades dada pelo vetoraux
								
									if resul > maior:
										maior = resul
										indicemaior=i
										
								for i in range(0,n):
									proximaGeracao[indicemaior][i]=vetorFilho[i]
								
					novaPopulacao=[]
					novaPopulacao = proximaGeracao			#proximaGeracao vira a nova população para a próxima iteração 
					equipes=[]
					 
					m = -1
					for i in range(len(novaPopulacao)):
						
						lista=[]
						
						#preenche matriz equipes de acordo com a equipe que correponde a cada numero real da atual matriz novaPopulacao
						for j in range(0, n):	
							for z in range(1,k+1):
								if (z/k > novaPopulacao[i][j]) and (novaPopulacao[i][j]>= (z-1)/k):
									lista.append(z)
						equipes.append(lista[:])
						
						vetoraux=[]	
						#a cada linha da matriz novaPopulacao preenche vetoraux com os numeros das atividades correspondentes	
						for j in range (0,n):		
							vetoraux.append(novaPopulacao[i][j])
						vetoraux=sorted(vetoraux)				
						
						for j in range(0,n):
							for b in range (0,n):
								if vetoraux[j] == novaPopulacao[i][b]:
									vetoraux[j]= b+1
						
						resul = Rota.CalcularRota(self,iinstancia,vetoraux,equipes[i],iinstancia.dias,arq)		#calcula custo de rota das equipes de acordo com numero 
																											# de dias dado e sequencia de atividades dada pelo vetoraux
						#armazena menor vetor da populacao atual com menor custo
						if (resul<m) or m == -1:	
							m = resul
							auxiliar = vetoraux
							auxiliarEquipe = equipes[i]	
						
					#se houve otimização do custo: atualiza a melhor rota e o número de dias
					if(m < menor):	
						self.resposta = m
						vetorResp= auxiliar
						vetorRespEquipe = auxiliarEquipe
					
					#se não: incrementa o contador para que satisfaça o critério de parada
					else: 	
						self.resposta = menor
						
						vetorResp=sorted(vetorum)
					
						for j in range(0,n):
							for b in range (0,n):
								if vetorResp[j] == vetorum[b]:
									vetorResp[j]= b+1
						vetorRespEquipe = vetorajudaEquipe
						contador= contador+1
				
				
				reini=reini+1
				#comparar o self.resposta
				if respAnterior!= -1 and respAnterior < self.resposta:
					self.resposta = respAnterior
					
				fim = time.time()
			return(self.resposta)		
