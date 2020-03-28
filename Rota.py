import Instancia


class  Rota:
	
		def __init__(self, arq):
			
			self.tempoAtividade=[]  #matriz que armazena atividades com seu tempo de inicio e fim	
			self.arq = arq
			
		'''
		Parâmetros:
			iinstancia- objeto da classe Instancia
			vetoraux- lista com sequencia de atividade
			equipes- lista com sequencia de equipes que realizam cada atividade do vetoraux 
			dias-  número de dias para realizar a sequencia de atividades
			
		Ideia: a função retorna a rota de cada equipe e seu custo total. A rota de cada equipe em cada dia leva em conta a lista de atividades a serem 
		realizadas e a lista de equipes, considerando condições específicas para cada atividade, como posição da atividade no talhão e a ordem em que 
		esta é realizada pela respectiva equipe e respeitando o número máximo de horas para o turno.
		
		'''	
		def CalcularRota(self,iinstancia,vetoraux,equipes,dias): 
			
			solucao =[]		#matriz que armazena rotas das equipes em cada dia
			listaDias=[]	#lista do tamanho do numero de equipes para armazenar o dia atual de cada equipe
			existe = False	#booleano para controle
			
			#inicialização da matriz solucao com a tupla que representa o depósito
			for i in range (iinstancia.dias):	
				lista=[]
				for j in range(iinstancia.equipes):
					lista2=[]
					lista2.append((0, None, 0, 0))
					lista.append(lista2[:])
				solucao.append(lista[:])
			
			
			ativ = None		#atividade atual
			talhao = None	#talhão da atividade atual
			horaIni = None	#tempo inicial da atividade 
			propExecutada = None	#proporção executada da atividade
			tempoOcioso = 0.0		#tempo de ociosidade das equipes 
			
			for j in range(iinstancia.equipes):		#inicialização da lista listaDias  
				listaDias.append(0)
						
			for i in range (0, iinstancia.numAtividades):    #inicialização self.tempoAtividade
				linha=[]
				for j in range(2):
					linha.append(0)
				self.tempoAtividade.append(linha[:])
			
			for xis in range(0, len(vetoraux)):
				equipe = equipes[xis]	#equipe correspondente a atividade atual
	
				if listaDias[equipe-1] < iinstancia.dias:	#se o dia atual da equipe for menor que o número de dias dado 
				
					ativ = vetoraux[xis]		
					auxiliar= -1
					indiceAntUm = -1
						
					continuar = True
					
					#para descobrir a qual talhão a atividade atual pertence e sua posição nele
					for c,v in iinstancia.atividades.items():	
						if continuar:	 
							for i in range (0, len(v)):
								if continuar:
									if iinstancia.atividades[c][i] == ativ:
										auxiliar=i
										talhao=c+1
										continuar = False
										break
						else:
							break
					
					
							
					tempoTarefa = iinstancia.tempoTarefa[ativ-1][equipe-1]
					
					existe = False
								
					for z in range(xis+1, len(vetoraux)):	#para verificar se há atividades a serem feitas pela mesma equipe ainda
						if  equipe == equipes[z]:
							existe = True
							break
					
				
					#se for a primeira atividade do vetoraux: tempo inicial recebe tempo de deslocamento do depósito e tempo final considera turno
					if xis == 0: 
						
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
										
								if existe == False:		#se  não há atividades a serem feitas pela mesma equipe
									solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
									if temp < 8.0:
										tempoOcioso= tempoOcioso + (8.0 - temp)
									
								self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
								
						else:
							
							solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
							self.tempoAtividade[ativ-1][1] = horaIni + tempoTarefa
							temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
							
							if existe == False :		#se  não há atividades a serem feitas pela mesma equipe
								solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
								if temp < 8.0:
									tempoOcioso= tempoOcioso + (8.0 - temp)
								
					
					else:		#se não for a primeira atividade da sequência dada no vetoraux
						
						#para armazenar -1 se a atividade é a primeira a ser feita pela equipe ou o índice da atividade feita anteriormente pela equipe
						for i in range (0, xis):	
							if equipes[i] == equipe:
								anterior = vetoraux[i]
								indiceAntUm= i
								break
						
						
								
						if auxiliar == 0:	#se a atividade for a primeira a ser realizada no talhao correspondente 
				
							#se a atividade for a primeira a ser realizada pela equipe correspondente: tempo inicial recebe tempo de deslocamento do 
							#deposito e para tempo final considera tempo de turno
							if indiceAntUm == -1:	
													
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
										
										if existe == False:		#se  não há atividades a serem feitas pela mesma equipe
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso = tempoOcioso + (8.0 - temp)
										self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
						
									
								else:
									
									solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
									self.tempoAtividade[ativ-1][1] = horaIni + tempoTarefa
									temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
									
									if existe == False :		#se  não há atividades a serem feitas pela mesma equipe
										solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
										if temp < 8.0:
											tempoOcioso = tempoOcioso + (8.0 - temp)
					
							else:	#se não: considera para tempo inicial o tempo final com o tempo deslocamento da atividade feita anteriormente pela 
									#equipe e tempo de turno e para tempo final considera o tempo da tarefa com o tempo de turno
									
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
										
										#se  não há atividades a serem feitas pela mesma equipe ou se o tempo e os dias foram esgotados 
										if (existe == False) or (temp > 8.0 and listaDias[equipe-1]+1 >= iinstancia.dias) :		
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso = tempoOcioso + (8.0 - temp)
												
											elif (temp > 8.0 and listaDias[equipe-1]+1 >= iinstancia.dias):
												listaDias[equipe-1] = listaDias[equipe-1] + 1
											
									
										self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
								
								else:
									if listaDias[equipe-1]< iinstancia.dias:
										solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
										self.tempoAtividade[ativ-1][1] = horaIni + tempoTarefa
										temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
										
										if existe == False :		#se  não há atividades a serem feitas pela mesma equipe
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso = tempoOcioso + (8.0 - temp)
						
						else:	#se a atividade não for a primeira a ser realizada no talhao	
							
							anterior2 = iinstancia.atividades[talhao-1][auxiliar-1] 	
							
							#se a atividade for a primeira a ser realizada pela equipe correspondente: para tempo inicial recebe tempo final da ultima 
							#atividade feita no talhao e para tempo final considera tempo de turno
							if indiceAntUm == -1:	
													
								
								if self.tempoAtividade[anterior2-1][1] < 8.0 :
									self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior2-1][1]
									horaIni = self.tempoAtividade[ativ-1][0]
								else:
									horaIni = iinstancia.tempoDeslocamento[0][talhao]
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
										
										if existe == False :		#se  não há atividades a serem feitas pela mesma equipe
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso =  tempoOcioso + (8.0 -temp)
									
										self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
									
								
									
								else:
									self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + tempoTarefa
									solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
									temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
									
									if existe == False :		#se  não há atividades a serem feitas pela mesma equipe
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
										temp =horaIni + tempoGasto + iinstancia.tempoDeslocamento[0][talhao]
										solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
										listaDias[equipe-1] = listaDias[equipe-1]+1	
										if listaDias[equipe-1] < iinstancia.dias:		
											horaIni= iinstancia.tempoDeslocamento[0][talhao]
											propExecutada= 1- propExecutada		
											tempoGasto=tempoTarefa-tempoGasto
											solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,propExecutada))
											temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
											
											if existe == False:			#se  não há atividades a serem feitas pela mesma equipe
												solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
												if temp < 8.0:
													tempoOcioso =  tempoOcioso + (8.0 -temp)
									
											self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
									
									else:
										self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + tempoTarefa
										solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
										temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
											
										if existe == False :	#se  não há atividades a serem feitas pela mesma equipe
											solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso =  tempoOcioso + (8.0 -temp)
										
								#se não: considera como tempo inicial o maior tempo entre: o tempo final da atividade realizada anteriormente pela equipe
								# + o deslocamento e o tempo final da atividade anterior do talhao, levando em conta o tempo de turno para o tempo 
								#inicial e final
								else:
										
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
														
												if existe==False:		#sse  não há atividades a serem feitas pela mesma equipe
													solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
													if temp < 8.0:
														tempoOcioso =  tempoOcioso + (8.0 -temp)
													
												self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
									
										else:
											if listaDias[equipe-1] < iinstancia.dias:
												solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
												temp = horaIni + tempoTarefa + iinstancia.tempoDeslocamento[0][talhao]
														
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
												
														
												if existe == False:		#se  não há atividades a serem feitas pela mesma equipe
													solucao[listaDias[equipe-1]][equipe-1].append((0,None,temp,0))
													if temp < 8.0:
														tempoOcioso = tempoOcioso + (8.0-temp)
												self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
										
										else:
											solucao[listaDias[equipe-1]][equipe-1].append((talhao,ativ,horaIni,1))
											temp = horaIni + tempoTarefa + iinstancia.tempoDeslocamento[0][talhao]
											
													
											if existe == False:		#se  não há atividades a serem feitas pela mesma equipe
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
			self.arq.write("------------------------------\n")
			self.arq.write(str(vetoraux))
			self.arq.write("\n")
			for dia in range(len(solucao)):
				prim = 0
				for equi in range(len(solucao[dia])):
					if(len(solucao[dia][equi])>1):
						if prim == 0 :
							self.arq.write('dia')
							self.arq.write(str(dia))
							self.arq.write("\n")
							prim = 1	
						self.arq.write('    Equipe')
						self.arq.write(str(equi))
						self.arq.write('->')
						self.arq.write(str(solucao[dia][equi])) 
						self.arq.write("\n")
						tempoUltra= tempoUltra + max( ((solucao[dia][equi][(len(solucao[dia][equi]))-1][2]) - 8),0)
						custoTotal= custoTotal + iinstancia.custoEquipe[equi] 
			self.arq.write("\n")
			custoTotal= custoTotal + (tempoUltra * penalidade) + tempoOcioso
			self.arq.write(str(custoTotal))
			self.arq.write("\n")
			
			return(custoTotal)
