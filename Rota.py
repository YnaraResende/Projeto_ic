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
			listaDias=[]	#lista do tamanho do numero de atividades para armazenar o dia atual de cada atividade
			listaPos = []	#lista para armazenar índice referente ao grupo de trabalho responsável pela atividade
			existe = False	#booleano para controle
			
			#para armazenar a quantidade de grupos de trabalhos existentes no total
			quant =0
			for i in (iinstancia.quant):
				quant = quant +i
			
			#inicialização da matriz solucao com a tupla que representa o depósito
			for i in range (iinstancia.dias):
				lista = []
				for j in range (iinstancia.equipes):
					lista2 = []
					for z in range (iinstancia.quant[j]):
						lista3 = []
						lista3.append((0, None, 0, 0))
						lista2.append(lista3[:])
					lista.append(lista2[:])
				solucao.append(lista[:])	
			
			
			ativ = None		#atividade atual
			talhao = None	#talhão da atividade atual
			horaIni = None	#tempo inicial da atividade 
			propExecutada = None	#proporção executada da atividade
			tempoOcioso = 0.0		#tempo de ociosidade das equipes 
			custoTotal = 0.0		
			
			for j in range(iinstancia.numAtividades):		#inicialização da lista listaDias  
				listaDias.append(0)
			
			for j in range(iinstancia.numAtividades):		#inicialização da lista listaPos 
				listaPos.append(0)
							
			for i in range (0, iinstancia.numAtividades):    #inicialização self.tempoAtividade
				linha=[]
				for j in range(2):
					linha.append(0)
				self.tempoAtividade.append(linha[:])
				
			#penalização para casos em que a lista de equipes possuI atribuição da equipe a atividades mais vezes que o permitido
			for i in range (iinstancia.equipes):
				cont = 0 
				for j in range (iinstancia.numAtividades):
					if equipes[j] == (i+1):
						if cont < iinstancia.quant[i]:
							cont = cont +1
						else:
							custoTotal = custoTotal+5.0
							break
			
			for xis in range(0, len(vetoraux)):
				equipe = equipes[xis]	#equipe correspondente a atividade atual
				ativ = vetoraux[xis]	#atividade atual
				auxiliar= -1
				indiceAntUm = -1
					
				#para descobrir a qual talhão a atividade atual pertence e sua posição nele
				continuar = True
				for c,v in iinstancia.atividades.items():	
					if continuar:	 
						for i in range (0, len(v)):
							if iinstancia.atividades[c][i] == ativ:
								auxiliar=i
								talhao=c+1
								continuar = False
								break
					else:
						break
					
				#variável armazena valor referente ao tempo de duração da atividade atual	
				tempoTarefa = iinstancia.tempoTarefa[ativ-1][equipe-1]
				
				#para verificar se há atividades a serem feitas pela mesma equipe ainda	
				existe = False				
				for z in range(xis+1, len(vetoraux)):	
					if  equipe == equipes[z]:
						existe = True
						break
						
				#para armazenar -1 se a atividade é a primeira a ser feita pela equipe ou a atividade feita anteriormente pela equipe e seu índice
				for i in range (0, xis):	
					if equipes[i] == equipe:
						anterior = vetoraux[i]
						indiceAntUm= i
				
				#para armazenar o índice do grupo de trabalho disponível para realizar a atividade, se não tiver grupo de trabalho disponível armazena -1
				cont = -1
				for aux in range (0,iinstancia.quant[equipe-1]):
					if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
						cont=aux
						break
								
				if auxiliar == 0:	#se a atividade for a primeira a ser realizada no talhao correspondente 
				
					#se a atividade for a primeira a ser realizada pela equipe correspondente: tempo inicial recebe tempo de deslocamento do 
					#deposito e para tempo final considera tempo de turno
					if indiceAntUm == -1:	
													
						horaIni = iinstancia.tempoDeslocamento[0][talhao] 	
						self.tempoAtividade[ativ-1][0] = horaIni
						listaPos[ativ-1] = 0
						
						if horaIni + tempoTarefa > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]): 
							propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
							tempoGasto=tempoTarefa*propExecutada
							solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
							temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
							solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
							listaDias[ativ-1] = listaDias[ativ-1]+1	
							#busca o primeiro grupo de trabalho disponível no dia posterior
							z = -1
							for aux in range (0,iinstancia.quant[equipe-1]):
								if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
									z=aux
									break
							listaPos[ativ-1] = z	
							if listaDias[ativ-1]< iinstancia.dias:		#se nao ultrapassou o numero de dias dado
								
								horaIni = iinstancia.tempoDeslocamento[0][talhao]
								propExecutada= 1- propExecutada		
								tempoGasto=tempoTarefa-tempoGasto
								solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
								temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
										
								if existe == False:		#se  não há atividades a serem feitas pela mesma equipe
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
									if temp < 8.0:
										tempoOcioso = tempoOcioso + (8.0 - temp)
								self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
							
						else:
								
							solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
							self.tempoAtividade[ativ-1][1] = horaIni + tempoTarefa	
							temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
									
							if existe == False :		#se  não há atividades a serem feitas pela mesma equipe
								solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
								if temp < 8.0:
									tempoOcioso = tempoOcioso + (8.0 - temp)
					
					else:	#se não: leva em consideração, se a equipe possui grupos de trabalho disponíveis, se não considera para tempo inicial o tempo
							#final com o tempo deslocamento da atividade feita anteriormente pela equipe e tempo de turno e para tempo final considera 
							#o tempo da tarefa com o tempo de turno
								
						#se possui grupos de trabalhos disponíveis: tempo inicial recebe tempo de deslocamento do deposito e para tempo final considera 
						#tempo de turno
						if cont != -1:
							
							#verifica se atividade anterior pela equipe não possui mais atividades do mesmo talhão e da mesma equipe a serem feitas, se 
							#não possuir adiciona a tupla que representa o deposito após a atividade anterior pela equipe
							talhaoAnt = solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][0]
									
							for z in range (len(iinstancia.atividades[talhaoAnt-1])):
								if iinstancia.atividades[talhaoAnt-1][z] == anterior:
									auxiliarAnt=z
									break
												
							continuar = True
							finaliza = True
							for z in range (xis+1, len(vetoraux)):
								if continuar:
									for x in range (auxiliarAnt+1,len(iinstancia.atividades[talhaoAnt-1])):
										if vetoraux[z] == iinstancia.atividades[talhaoAnt-1][x] and equipes[z] == equipe:
											finaliza = False
											continuar = False
											break
								else:
									break
												
							if finaliza:
								temp = solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][2] + (iinstancia.tempoTarefa[anterior-1][equipe-1]*solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][-1])+iinstancia.tempoDeslocamento[talhaoAnt][0]
								solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]].append((0,None,temp,0))
								if temp < 8.0:
									tempoOcioso= tempoOcioso + (8.0 - temp)
								
							horaIni = iinstancia.tempoDeslocamento[0][talhao] 
							self.tempoAtividade[ativ-1][0] = horaIni
							listaPos[ativ-1] = cont
								
										
						else: #se não possui
							
							listaDias[ativ-1] = listaDias[anterior-1]
							listaPos[ativ-1] = listaPos[anterior-1]	
							talhaoAnt= solucao[listaDias[anterior-1]][equipe-1][listaPos[ativ-1]][-1][0]
							propExecutadaAnt = solucao[listaDias[anterior-1]][equipe-1][listaPos[ativ-1]][-1][-1]
							tempoGastoAnterior =(iinstancia.tempoTarefa[anterior-1][equipe-1])*propExecutadaAnt
								
									
							if (solucao[listaDias[anterior-1]][equipe-1][listaPos[ativ-1]][-1][2]+ tempoGastoAnterior + iinstancia.tempoDeslocamento[talhaoAnt][talhao])> iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]:
								temp = solucao[listaDias[anterior-1]][equipe-1][listaPos[ativ-1]][-1][2]+ tempoGastoAnterior+ iinstancia.tempoDeslocamento[talhaoAnt][0]
								solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
								horaIni = iinstancia.tempoDeslocamento[0][talhao] 
								self.tempoAtividade[ativ-1][0] = horaIni
								listaDias[ativ-1] = listaDias[ativ-1]+1	
														
							else:
								horaIni = solucao[listaDias[anterior-1]][equipe-1][listaPos[ativ-1]][-1][2]+ tempoGastoAnterior + iinstancia.tempoDeslocamento[talhaoAnt][talhao]
								self.tempoAtividade[ativ-1][0] = horaIni
									
						if (horaIni + tempoTarefa) > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]):
							propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
							tempoGasto=tempoTarefa*propExecutada
									
							if listaDias[ativ-1] < iinstancia.dias: 			
								if listaDias[ativ-1]+1 < iinstancia.dias:
									 
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
									temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
									listaDias[ativ-1] = listaDias[ativ-1]+1	
									#busca o primeiro grupo de trabalho disponível no dia posterior	
									z = -1
									for aux in range (0,iinstancia.quant[equipe-1]):
										if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
											z=aux	
											break
											
									listaPos[ativ-1]=z
									horaIni= iinstancia.tempoDeslocamento[0][talhao]
									propExecutada= 1- propExecutada		
									tempoGasto=tempoTarefa-tempoGasto
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
									temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
												
									#se  não há atividades a serem feitas pela mesma equipe ou se o tempo e os dias foram esgotados 
									if (existe == False) or (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias) :		
										solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
										if temp < 8.0:
											tempoOcioso = tempoOcioso + (8.0 - temp)
														
										elif (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias):
											listaDias[ativ-1] = listaDias[ativ-1] + 1
												
									self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
												
								else:
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
									temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
									listaDias[ativ-1]=listaDias[ativ-1]+1
							
						else:
							if listaDias[ativ-1]< iinstancia.dias:
								
								solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
								self.tempoAtividade[ativ-1][1] = horaIni + tempoTarefa
								temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
										
								if existe == False :		#se  não há atividades a serem feitas pela mesma equipe
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
									if temp < 8.0:
										tempoOcioso = tempoOcioso + (8.0 - temp)
				
				else:	#se a atividade não for a primeira a ser realizada no talhao	
							
					anterior2 = iinstancia.atividades[talhao-1][auxiliar-1]		#anterior pelo talhão	
							
					#se a atividade for a primeira a ser realizada pela equipe correspondente: para tempo inicial considera dia posterior a atividade 
					#anterior pelo talhão e tempo de deslocamento do deposito e para tempo final considera tempo de turno
					if indiceAntUm == -1:	
													
						listaDias[ativ-1] = listaDias[anterior2-1]+1	
						listaPos[ativ-1] = 0
						horaIni = iinstancia.tempoDeslocamento[0][talhao]
						
						if horaIni+ tempoTarefa > (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]): 
									
							propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
							tempoGasto=tempoTarefa*propExecutada
							if listaDias[ativ-1] < iinstancia.dias:
								if listaDias[ativ-1]+1 < iinstancia.dias:
									
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
									temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
									listaDias[ativ-1] = listaDias[ativ-1]+1	
									horaIni= iinstancia.tempoDeslocamento[0][talhao]
									propExecutada= 1- propExecutada		
									tempoGasto=tempoTarefa-tempoGasto
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
									temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
										
									#se  não há atividades a serem feitas pela mesma equipe ou se o tempo e os dias foram esgotados
									if (existe == False) or (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias) :		
										solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
										if temp < 8.0:
											tempoOcioso =  tempoOcioso + (8.0 -temp)
										elif (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias):
											listaDias[ativ-1] = listaDias[ativ-1] + 1
												
									self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
									
								else:
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))	
									temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
									listaDias[ativ-1]=listaDias[ativ-1]+1
									
						else:
							if listaDias[ativ-1] < iinstancia.dias:
								self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + tempoTarefa
								solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
								temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
										
								if existe == False :		#se  não há atividades a serem feitas pela mesma equipe
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
									if temp < 8.0:
										tempoOcioso =  tempoOcioso + (8.0 -temp)
					
					else: #se não for a primeira da equipe
								
						if anterior == anterior2:	#se anterior da equipe correspondente for do mesmo talhao: tempo inicial recebe tempo final da 
													#atividade feita pela equipe anteriormente e tempo final considera  tempo de turno						
							listaDias[ativ-1]=listaDias[anterior-1]
							listaPos[ativ-1] = listaPos[anterior-1]
							self.tempoAtividade[ativ-1][0] = self.tempoAtividade[anterior-1][1]
							horaIni= self.tempoAtividade[ativ-1][0]
									 
							if horaIni + tempoTarefa > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]): 
					
								propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
								tempoGasto=tempoTarefa*propExecutada
										
								if listaDias[ativ-1] < iinstancia.dias:
									if listaDias[ativ-1] + 1< iinstancia.dias:
										solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
										temp = horaIni + tempoGasto + iinstancia.tempoDeslocamento[0][talhao]
										solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
										listaDias[ativ-1] = listaDias[ativ-1]+1		
										#busca o primeiro grupo de trabalho disponível no dia posterior
										z = -1
										for aux in range (0,iinstancia.quant[equipe-1]):
											if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
												z=aux
												break
										listaPos[ativ-1]=z
										horaIni= iinstancia.tempoDeslocamento[0][talhao]
										propExecutada= 1- propExecutada		
										tempoGasto=tempoTarefa-tempoGasto
										solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
										temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
												
										#se  não há atividades a serem feitas pela mesma equipe ou se o tempo e os dias foram esgotados 
										if (existe == False) or (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias) :
											solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso =  tempoOcioso + (8.0 -temp)												
											elif (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias):
												listaDias[ativ-1] = listaDias[ativ-1] + 1
										
										self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
												
									else:
										solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
										temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
										solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
										listaDias[ativ-1] = listaDias[ativ-1]+1
									
							else:
								if listaDias[ativ-1] < iinstancia.dias:
									self.tempoAtividade[ativ-1][1] = self.tempoAtividade[ativ-1][0] + tempoTarefa
									solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
									temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
												
									if existe == False :	#se  não há atividades a serem feitas pela mesma equipe
										solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
										if temp < 8.0:
											tempoOcioso =  tempoOcioso + (8.0 -temp)
						
						else:	#se o anterior pela equipe não for do mesmo talhão
							
							#para armazenar qual a posição da atividade anterior pelo talhão no vetoraux
							indice = -1
							for a in range (0, len(vetoraux)):
								if anterior2 == vetoraux[a]:
									indice = a
									break
							
							
							if listaDias[anterior-1]==listaDias[anterior2-1]:	#se a atividade anterior pela equipe e a atividade anterior pelo talhão 
																				#terminam no mesmo dia
		
								if listaDias[anterior-1] < iinstancia.dias:		#verifica se o dia em que a atividade anterior pela equipe termina é 
																				#válido
									talhaoAnt= solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][0]
									propExecutadaAnt = solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][-1]
									tempoGastoAnterior =(iinstancia.tempoTarefa[anterior-1][equipe-1])*propExecutadaAnt
									
									#se a atividade anterior pela equipe termina mais tarde: 
									if ((self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[talhaoAnt][talhao]) > self.tempoAtividade[anterior2-1][1]):
										
										#verifica se atividade anterior pela equipe não possui mais atividades do mesmo talhão e da mesma equipe a 
										#serem feitas, se não possuir adiciona a tupla que representa o deposito após a atividade anterior pela equipe
										
										for z in range (0,len(iinstancia.atividades[talhaoAnt-1])):
											if iinstancia.atividades[talhaoAnt-1][z] == anterior:
												auxiliarAnt=z
												break
																
										continuar = True
										finaliza = True
										for z in range (xis+1, len(vetoraux)):
											if continuar:
												for x in range (auxiliarAnt+1,len(iinstancia.atividades[talhaoAnt-1])):
													if vetoraux[z] == iinstancia.atividades[talhaoAnt-1][x] and equipes[z] == equipe:
														finaliza = False
														continuar = False
														break
											else:
												break
																
										if finaliza:
											temp = solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][2] + (iinstancia.tempoTarefa[anterior-1][equipe-1]*solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][-1])+iinstancia.tempoDeslocamento[talhaoAnt][0]
											solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso= tempoOcioso + (8.0 - temp)
									
										#se a equipe responsável pela atividade atual não for a mesma equipe reponsável pela atividade anterior pelo 
										#talhão: para tempo inicial considera dia posterior a atividade anterior pelo talhão e tempo de deslocamento do 
										#deposito e para tempo final considera turno
										if equipes[indice] != equipe:
											listaDias[ativ-1]= listaDias[anterior2-1] + 1
											horaIni = iinstancia.tempoDeslocamento[0][talhao] 
											self.tempoAtividade[ativ-1][0] = horaIni
											#busca o primeiro grupo de trabalho disponível no dia posterior
											z = -1
											for aux in range (0,iinstancia.quant[equipe-1]):
												if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
													z=aux
													break
											listaPos[ativ-1] = z
											
										#se não: para tempo inicial considera dia e tempo final da atividade anterior pelo talhão e para tempo final
										#considera turno
										else:
											listaDias[ativ-1]= listaDias[anterior2-1]
											horaIni= self.tempoAtividade[anterior2-1][1]
											self.tempoAtividade[ativ-1][0] = horaIni 
											listaPos[ativ-1] = listaPos[anterior2-1]
											
										if horaIni + tempoTarefa > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]):
											propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
											tempoGasto=tempoTarefa*propExecutada
														
											if listaDias[ativ-1] < iinstancia.dias:
												if listaDias[ativ-1]+1< iinstancia.dias:
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
													temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													listaDias[ativ-1] = listaDias[ativ-1]+1		
													horaIni= iinstancia.tempoDeslocamento[0][talhao]
													propExecutada= 1- propExecutada		
													tempoGasto=tempoTarefa-tempoGasto
													#busca o primeiro grupo de trabalho disponível no dia posterior
													z = -1
													for aux in range (0,iinstancia.quant[equipe-1]):
														if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
															z=aux
															break
													listaPos[ativ-1]=z
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
													temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
								
													#se  não há atividades a serem feitas pela mesma equipe ou se o tempo e os dias foram esgotados 
													if (existe == False) or (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias) :
														solucao[listaDias[ativ-1]][equipe-1][z].append((0,None,temp,0))
														if temp < 8.0:
															tempoOcioso =  tempoOcioso + (8.0 -temp)
														elif (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias):
															listaDias[ativ-1] = listaDias[ativ-1] + 1
															
													self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
														
												else:
													
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
													temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													listaDias[ativ-1]=listaDias[ativ-1]+1
								
										
										else:
											if listaDias[ativ-1] < iinstancia.dias:
												solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
												temp = horaIni + tempoTarefa + iinstancia.tempoDeslocamento[0][talhao]
																	
												if existe==False:		#se  não há atividades a serem feitas pela mesma equipe
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													if temp < 8.0:
														tempoOcioso =  tempoOcioso + (8.0 -temp)
												self.tempoAtividade[ativ-1][1] = horaIni+ tempoTarefa
									
									#se a atividade anterior pelo talhão termina mais tarde
									else:
										
										#verifica se atividade anterior pela equipe não possui mais atividades do mesmo talhão e da mesma equipe a 
										#serem feitas, se não possuir adiciona a tupla que representa o deposito após a atividade anterior pela equipe
										talhaoAnt = solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][0]
										
										for z in range (len(iinstancia.atividades[talhaoAnt-1])):
											if iinstancia.atividades[talhaoAnt-1][z] == anterior:
												auxiliarAnt=z
												break
																
										continuar = True
										finaliza = True
										for z in range (xis+1, len(vetoraux)):
											if continuar:
												for x in range (auxiliarAnt+1,len(iinstancia.atividades[talhaoAnt-1])):
													if vetoraux[z] == iinstancia.atividades[talhaoAnt-1][x] and equipes[z] == equipe:
														finaliza = False
														continuar = False
														break
											else:
												break
																
										if finaliza:
											temp = solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][2] + (iinstancia.tempoTarefa[anterior-1][equipe-1]*solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][-1])+iinstancia.tempoDeslocamento[talhaoAnt][0]
											solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso= tempoOcioso + (8.0 - temp)
						
										#se a equipe responsável pela atividade atual não for a mesma equipe reponsável pela atividade anterior pelo 
										#talhão: para tempo inicial considera dia posterior a atividade anterior pelo talhão e tempo de deslocamento do 
										#deposito e para tempo final considera turno
										if equipes[indice] != equipe:
											listaDias[ativ-1]= listaDias[anterior2-1] + 1
											horaIni = iinstancia.tempoDeslocamento[0][talhao] 
											self.tempoAtividade[ativ-1][0] = horaIni
											#busca o primeiro grupo de trabalho disponível no dia posterior
											z = -1
											for aux in range (0,iinstancia.quant[equipe-1]):
												if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
													z=aux
													break
											listaPos[ativ-1] = z
										
										#se não: para tempo inicial considera dia e tempo final da atividade anterior pelo talhão e para tempo final
										#considera turno
										else:
													
											listaDias[ativ-1]= listaDias[anterior2-1]
											horaIni= self.tempoAtividade[anterior2-1][1]
											self.tempoAtividade[ativ-1][0] = horaIni 
											listaPos[ativ-1] = listaPos[anterior2-1]
											
										if horaIni + tempoTarefa > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]):
											propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
											tempoGasto=tempoTarefa*propExecutada
														
											if listaDias[ativ-1] < iinstancia.dias:
												if listaDias[ativ-1]+1< iinstancia.dias:
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
													temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													listaDias[ativ-1] = listaDias[ativ-1]+1		
													horaIni= iinstancia.tempoDeslocamento[0][talhao]
													propExecutada= 1- propExecutada		
													tempoGasto=tempoTarefa-tempoGasto
													#busca o primeiro grupo de trabalho disponível no dia posterior
													z = -1
													for aux in range (0,iinstancia.quant[equipe-1]):
														if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
															z= aux
															break
													listaPos[ativ-1]=z
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
													temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
								
													#se  não há atividades a serem feitas pela mesma equipe ou se o tempo e os dias foram esgotados 
													if (existe == False) or (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias) :
														solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
														if temp < 8.0:
															tempoOcioso =  tempoOcioso + (8.0 -temp)
														elif (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias):
															listaDias[ativ-1] = listaDias[ativ-1] + 1
																
													self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
															
												else:
														
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
													temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													listaDias[ativ-1]=listaDias[ativ-1]+1
								
											
										else:
											if listaDias[ativ-1] < iinstancia.dias:
												solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
												temp = horaIni + tempoTarefa + iinstancia.tempoDeslocamento[0][talhao]
																	
												if existe==False:		#se  não há atividades a serem feitas pela mesma equipe
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													if temp < 8.0:
														tempoOcioso =  tempoOcioso + (8.0 -temp)
												self.tempoAtividade[ativ-1][1] = horaIni+ tempoTarefa
							
							else:	#se a atividade anterior pela equipe e a atividade anterior pelo talhão não terminam no mesmo dia
								if listaDias[anterior-1]>listaDias[anterior2-1]:	#se a atividade anterior pela equipe termina depois 
									if listaDias[anterior-1] < iinstancia.dias:		#verifica se o dia em que a atividade anterior pela equipe termina
																					#é válido
										
										#verifica se atividade anterior pela equipe não possui mais atividades do mesmo talhão e da mesma equipe a 
										#serem feitas, se não possuir adiciona a tupla que representa o deposito após a atividade anterior pela equipe												
										talhaoAnt = solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][0]
										
										for z in range (0,len(iinstancia.atividades[talhaoAnt-1])):
											if iinstancia.atividades[talhaoAnt-1][z] == anterior:
												auxiliarAnt=z
												break
												
										continuar = True
										finaliza = True
										for z in range (xis+1, len(vetoraux)):
											if continuar:
												for x in range (auxiliarAnt+1,len(iinstancia.atividades[talhaoAnt-1])):
													if vetoraux[z] == iinstancia.atividades[talhaoAnt-1][x] and equipes[z] ==equipe:
														finaliza = False
														continuar = False
														break
											else:
												break
												
										if finaliza:
											temp = solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][2] + (iinstancia.tempoTarefa[anterior-1][equipe-1]*solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][-1])+iinstancia.tempoDeslocamento[talhaoAnt][0]
											solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]].append((0,None,temp,0))
											if temp < 8.0:
												tempoOcioso = tempoOcioso + (8.0 - temp)
										
										#se a equipe responsável pela atividade atual não for a mesma equipe reponsável pela atividade anterior pelo 
										#talhão: para tempo inicial considera se há grupos de trabalhos disponíveis, se não a atividade começa após o
										#fim da atividade anterior pela equipe e para tempo final considera turno	
										if equipes[indice] != equipe:
											listaDias[ativ-1] = listaDias[anterior2-1]+1
											cont = -1
											for aux in range (0,iinstancia.quant[equipe-1]):
												if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
													cont=aux
													break
											
											if cont != -1:
												horaIni = iinstancia.tempoDeslocamento[0][talhao]
												self.tempoAtividade[ativ-1][0] = horaIni
												listaPos[ativ-1] = cont
											
											else :
												#talhaoAnt = solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][0]
												horaIni = self.tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[talhaoAnt][talhao]
												self.tempoAtividade[ativ-1][0] = horaIni
												listaPos[ativ-1]= listaPos[anterior-1]
										
										#se a equipe responsável pela atividade atual for a mesma equipe reponsável pela atividade anterior pelo 
										#talhão: para tempo inicial considera dia e tempo final da atividade anterior pelo talhão e para tempo final
										#considera turno
										else: 
											listaDias[ativ-1]= listaDias[anterior2-1]
											horaIni= self.tempoAtividade[anterior2-1][1]
											self.tempoAtividade[ativ-1][0] = horaIni 
											listaPos[ativ-1] = listaPos[anterior2-1]
											
										if horaIni + tempoTarefa > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]):
											propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
											tempoGasto=tempoTarefa*propExecutada
														
											if listaDias[ativ-1] < iinstancia.dias:
												if listaDias[ativ-1]+1< iinstancia.dias:
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
													temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													listaDias[ativ-1] = listaDias[ativ-1]+1		
													horaIni= iinstancia.tempoDeslocamento[0][talhao]
													propExecutada= 1- propExecutada		
													tempoGasto=tempoTarefa-tempoGasto
													#busca o primeiro grupo de trabalho disponível no dia posterior
													z = -1
													for aux in range (0,iinstancia.quant[equipe-1]):
														if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
															z=aux
															break
													listaPos[ativ-1] = z
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
													temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
								
													#se  não há atividades a serem feitas pela mesma equipe ou se o tempo e os dias foram esgotados 
													if (existe == False) or (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias) :
														solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
														if temp < 8.0:
															tempoOcioso =  tempoOcioso + (8.0 -temp)
														elif (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias):
															listaDias[ativ-1] = listaDias[ativ-1] + 1
																
													self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
															
												else:
														
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
													temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													listaDias[ativ-1]=listaDias[ativ-1]+1
								
										
										else:
											if listaDias[ativ-1] < iinstancia.dias:
												
												solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
												temp = horaIni + tempoTarefa + iinstancia.tempoDeslocamento[0][talhao]
																	
												if existe==False:		#se  não há atividades a serem feitas pela mesma equipe
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													if temp < 8.0:
														tempoOcioso =  tempoOcioso + (8.0 -temp)
												self.tempoAtividade[ativ-1][1] = horaIni+ tempoTarefa
											
								else:	#se a atividade anterior pelo talhão termina depois
									if listaDias[anterior2-1] < iinstancia.dias:	#se o dia em que a atividade anterior pelo talhão termina for válido
										
										#se a equipe responsável pela atividade atual não for a mesma equipe reponsável pela atividade anterior pelo 
										#talhão: para tempo inicial considera dia posterior a atividade anterior pelo talhão e tempo de deslocamento do
										#deposito e para tempo final considera tempo de turno
										if equipes[indice] != equipe:
											
											#verifica se atividade anterior pela equipe não possui mais atividades do mesmo talhão e da mesma equipe a 
											#serem feitas, se não possuir adiciona a tupla que representa o deposito após a atividade anterior pela equipe
											talhaoAnt = solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][0]
									
											for z in range (len(iinstancia.atividades[talhaoAnt-1])):
												if iinstancia.atividades[talhaoAnt-1][z] == anterior:
													auxiliarAnt=z
													break
													
											continuar = True
											finaliza = True
											for z in range (xis+1, len(vetoraux)):
												if continuar:
													for x in range (auxiliarAnt+1,len(iinstancia.atividades[talhaoAnt-1])):
														if vetoraux[z] == iinstancia.atividades[talhaoAnt-1][x] and equipes[z] ==equipe:
															finaliza = False
															continuar = False
															break
												else:
													break
													
											if finaliza:
												temp = solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][2] + (iinstancia.tempoTarefa[anterior-1][equipe-1]*solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]][-1][-1])+iinstancia.tempoDeslocamento[talhaoAnt][0]
												solucao[listaDias[anterior-1]][equipe-1][listaPos[anterior-1]].append((0,None,temp,0))
												if temp < 8.0:
													tempoOcioso = tempoOcioso + (8.0 - temp)
											listaDias[ativ-1] = listaDias[anterior2-1]+1
											#busca o primeiro grupo de trabalho disponível no dia posterior
											z = -1
											for aux in range (0,iinstancia.quant[equipe-1]):
												if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
													z=aux
													break
												
											horaIni = iinstancia.tempoDeslocamento[0][talhao]
											self.tempoAtividade[ativ-1][0] = horaIni
											listaPos[ativ-1] = z
										
										#se a equipe responsável pela atividade atual for a mesma equipe reponsável pela atividade anterior pelo 
										#talhão: para tempo inicial considero dia e tempo final da atividade anterior pelo talhão e para tempo final
										#considera turno
										else:
											listaDias[ativ-1]= listaDias[anterior2-1]
											horaIni= self.tempoAtividade[anterior2-1][1]
											self.tempoAtividade[ativ-1][0] = horaIni 
											listaPos[ativ-1] = listaPos[anterior2-1]
											
										if horaIni + tempoTarefa > (iinstancia.turno - iinstancia.tempoDeslocamento[0][talhao]):
											propExecutada= (iinstancia.turno-iinstancia.tempoDeslocamento[0][talhao]-horaIni)/tempoTarefa
											tempoGasto=tempoTarefa*propExecutada
														
											if listaDias[ativ-1] < iinstancia.dias:
												if listaDias[ativ-1]+1< iinstancia.dias:
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
													temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													listaDias[ativ-1] = listaDias[ativ-1]+1		
													horaIni= iinstancia.tempoDeslocamento[0][talhao]
													propExecutada= 1- propExecutada		
													tempoGasto=tempoTarefa-tempoGasto
													
													z = -1
													for aux in range (0,iinstancia.quant[equipe-1]):
														if len(solucao[listaDias[ativ-1]][equipe-1][aux]) == 1:
															z=aux
															break
													
													listaPos[ativ-1] = z
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,propExecutada))
													temp =horaIni+tempoGasto+iinstancia.tempoDeslocamento[0][talhao]
													
													
													#se  não há atividades a serem feitas pela mesma equipe ou se o tempo e os dias foram esgotados 
													if (existe == False) or (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias) :
														solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
														if temp < 8.0:
															tempoOcioso =  tempoOcioso + (8.0 -temp)
														elif (temp > 8.0 and listaDias[ativ-1]+1 >= iinstancia.dias):
															listaDias[ativ-1] = listaDias[ativ-1] + 1
																
													self.tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][talhao] + tempoGasto
															
												else:
														
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
													temp =horaIni+tempoTarefa+iinstancia.tempoDeslocamento[0][talhao]
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													listaDias[ativ-1]=listaDias[ativ-1]+1
								
											
										else:
											if listaDias[ativ-1] < iinstancia.dias:
												solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((talhao,ativ,horaIni,1))
												temp = horaIni + tempoTarefa + iinstancia.tempoDeslocamento[0][talhao]
																	
												if existe==False:		#se  não há atividades a serem feitas pela mesma equipe
													solucao[listaDias[ativ-1]][equipe-1][listaPos[ativ-1]].append((0,None,temp,0))
													if temp < 8.0:
														tempoOcioso =  tempoOcioso + (8.0 -temp)
												self.tempoAtividade[ativ-1][1] = horaIni+ tempoTarefa
			
			tempoUltra = 0.0	#armazena tempo que ultrapassa tempo de turno
			#armazena o custo da equipe de maior valor
			maiorCusto = 0.0	
			for j in iinstancia.custoEquipe:
				if j > maiorCusto:
					maiorCusto = j
			penalidade = 3 * maiorCusto
			achou = False						
			self.arq.write("------------------------------\n")
			self.arq.write(str(vetoraux))
			self.arq.write(str(equipes))
			self.arq.write("\n")
			for dia in range(len(solucao)):
				prim = 0
				for equi in range(len(solucao[dia])):
					for cont in range (len(solucao[dia][equi])):
						if(len(solucao[dia][equi][cont])>1):
							if prim == 0 :
								self.arq.write('dia')
								self.arq.write(str(dia))
								self.arq.write("\n")
								prim = 1	
							self.arq.write('    Equipe')
							self.arq.write(str(equi))
							self.arq.write('->')
							self.arq.write(str(solucao[dia][equi][cont])) 
							self.arq.write("\n")
							tempoUltra= tempoUltra + max(((solucao[dia][equi][cont][-1][2]) - 8.0),0)
							custoTotal= custoTotal + iinstancia.custoEquipe[equi] 
							#condição para verificar se todas as atividades foram feitas
							ultEquipe=(equipes[iinstancia.numAtividades-1])-1
							if equi == ultEquipe:
								if solucao[dia][equi][cont][(len(solucao[dia][equi][cont]))-2][1] == vetoraux[iinstancia.numAtividades-1]:
									achou = True
				
			#se alguma atividade não foi realizada, há uma penalização
			if achou == False:
				custoTotal= custoTotal + 5.0
				
			self.arq.write("\n")
			custoTotal= custoTotal + (tempoUltra * penalidade) + tempoOcioso
			self.arq.write(str(custoTotal))
			self.arq.write("\n")				
			
			return custoTotal
