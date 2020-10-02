import Instancia

class  Rota:
	
	def __init__(self, arq):
			
		self.tempoAtividade=[]		#matriz que armazena atividades com seu tempo de inicio e fim	
		self.arq = arq				#arquivo de saída
		self.solucao = []			#matriz que armazena as rotas das equipes em cada dia
			

	'''		

	Parâmetros:
		iinstancia - objeto da classe Instancia
		vetoraux - lista de atividades
		equipes - lista com sequencia de equipes e grupos de trabalho que realizam cada atividade do vetoraux 
		dias -  número de dias para realizar a sequencia de atividades
			
	Ideia: a função retorna a rota de cada equipe e seu custo total. É realizada a rota que foi pré-estabelecida na fase construtiva da função GRASP,
	pertencente a classe BRKGA, dessa forma, a rota de cada equipe em cada dia leva em conta a lista de atividades a serem realizadas e a lista de 
	equipes e grupos de trabalho, considerando os custos relativos as equipes designadas, ao tempo que ultrapassou o turno, ao tempo de ociosidade 
	das equipes e a penalização caso alguma atividade não tenha sido realizada.
		
	'''	
	def CalcularRota(self,iinstancia,vetoraux,equipes,dias): 
				
		#inicialização da matriz solucao e matriz pendente
		self.solucao = []
			
		for i in range (iinstancia.dias):
			lista = []
			for j in range (iinstancia.equipes):
				lista2 = []
				for z in range (iinstancia.quant[j]):
					lista3 = []
					lista3.append((0, None, 0, 0))
					lista2.append(lista3[:])
				lista.append(lista2[:])		
			self.solucao.append(lista[:])	
		
		tempoUltra = 0.0		#tempo que foi ultrassado do tempo de turno
		tempoOcioso = 0.0		#tempo de ociosidade das equipes 
		custoTotal = 0.0		#custo total da rota estabelecida
					
		#para facilitar o acesso aos dados
		dias = iinstancia.dias
		tempoViagem = iinstancia.tempoDeslocamento
		talhoes = iinstancia.talhoes-1
		atividades = iinstancia.atividades
		tempoTarefa = iinstancia.tempoTarefa
		numEq = iinstancia.equipes
		
		listaux = []
		equipesaux = []	
		for c in range(0,iinstancia.numAtividades):
			listaux.append(vetoraux[c])
			equipesaux.append(equipes[c])
				
		dia = 0 
		
		#quanto falta para que a atividade seja terminada
		frac = {(v+1, a):1 for v in range(talhoes) for a in atividades[v]}
			
		inacabadas = set()		#conjunto que armazenas as atividades que não foram terminadas
		
		#matriz que armazena para cada grupo de trabalho as atividades pendentes
		pendente = []	
		for i in range(numEq):
			listaUm = []
			for k in range (iinstancia.quant[i]):
				listaDois = []
				for j in range (2):
					listaDois.append(None)
				listaUm.append(listaDois[:]) 
			pendente.append(listaUm[:])	
		
			
		while listaux or inacabadas:
			
			#armazena o ultimo grupo de trabalho e equipe que foi destinado para cada talhão no mesmo dia
			quantgt = [(None, None) for k in range (talhoes)]	
			
			#lista que armazena tuplas formadas por (equipe, grupo de trabalho, talhao, atividade e tempo de conclusão da atividade)
			eventos= []	
			for eq in range(1, iinstancia.equipes+1):
				for gr in range (iinstancia.quant[eq-1]):
					eventos.append((eq, gr, 0, None, 0))  
				
			while eventos:
					
				(eq, gr, v, a, q) = eventos.pop(0)
				
				#funções para estabelecer tempos de inicio e fim da atividade			
				inicio = lambda h, b: q + tempoViagem[ self.solucao[dia][eq-1][gr][-1][0] ][h]	
				fim = lambda h, b: inicio(h, b)+ (tempoTarefa[b-1][eq-1]*frac[(h,b)])
				
				#caso o grupo de trabalho possua atividades pendentes 
				pend = False
				if (pendente[eq-1][gr][0] != None) and (pendente[eq-1][gr][1] != None):
					v = pendente[eq-1][gr][0]
					a = pendente[eq-1][gr][1]
					quantgt[v-1] = (gr, eq-1)
					pend = True
							
				else:
					
					for z in range (len(equipesaux)):
						#se a posição atual da lista de equipes e grupos de trabalho contiver os mesmos dados do evento atual, se a atividade anterior
						#do talhão já foi realizada e a atividade puder ser realizada pelo grupo de trabalho em questão, haverá realização da atividade 
						#respectiva do evento 
						if (eq, gr) == equipesaux[z] :
							ativ = listaux[z]
								
							continuar = True
							for c, ve in atividades.items():	
								if continuar:	 
									for i in range (0, len(ve)):
										if atividades[c][i] == ativ:
											t = c
											aux = i
											continuar = False
											if aux != 0:
												ant = atividades[t][aux-1]
											break
								else:
									break
									
							continuar = True
							if aux != 0:
								for at in listaux:
									if at == ant: 
										continuar = False
										
								for at in inacabadas:
									if at[-1] == ant:
										continuar = False
							
							if continuar == True:
								if (inicio(t+1, ativ) + tempoViagem[t+1][0] )> iinstancia.turno:
									continuar = False
									
							entrou = False		
							if (((gr, eq-1) == quantgt[t] and self.solucao[dia][eq-1][gr][-1][1] == ant )or (quantgt[t] == (None, None))) and continuar == True:
								v = t+1
								a = ativ
								equipesaux.pop(z)
								listaux.pop(z)
								quantgt[t] = (gr, eq-1)
								entrou = True
								break
							
				if ((v, a) != (0, None) and entrou == True) or pend :
					entrou = False
					
					tempoFim = fim(v, a)
					tempoInicio = inicio(v, a)
					
					#se a atividade foi terminada
					if tempoFim + tempoViagem[v][0] <= iinstancia.turno:
						pendente[eq-1][gr][0] = None
						pendente[eq-1][gr][1] = None
						
						if (v,a) in inacabadas:
							inacabadas.remove((v,a))
						
						eventos.append((eq, gr, v, a, tempoFim))
						self.solucao[dia][eq-1][gr].append((v, a, tempoInicio, frac[(v, a)]))
						temp = tempoFim + tempoViagem[v][0]
						
						if (not listaux) and (not inacabadas):
							tempoOcioso = tempoOcioso + (iinstancia.turno - temp)
							self.solucao[dia][eq-1][gr].append((0, None, temp, 0))
							break
						
						else:
							for i in range (len(vetoraux)):
								if a == vetoraux[i]:
									if equipes[i] not in equipesaux : 
										tempoOcioso = tempoOcioso + (iinstancia.turno - temp)
										self.solucao[dia][eq-1][gr].append((0, None, temp, 0))
									break
							
					# se a atividade não pode ser terminada, mas é o ultimo dia disponível
					elif (tempoFim + tempoViagem[v][0] > iinstancia.turno) and (dia == iinstancia.dias-1):
						
						temp = tempoFim + tempoViagem[v][0]
						self.solucao[dia][eq-1][gr].append((v, a, tempoInicio, frac[(v, a)]))
						self.solucao[dia][eq-1][gr].append((0, None, temp, 0))
						
					# se a atividade não pode ser terminada
					else: 
							
						T= iinstancia.turno - tempoViagem[v][0] - tempoInicio
						f= T/tempoTarefa[a-1][eq-1]
						frac[(v, a)] = frac[(v, a)] - f
						pendente[eq-1][gr][0] = v
						pendente[eq-1][gr][1] = a
						inacabadas.add((v, a))
						self.solucao[dia][eq-1][gr].append((v, a, tempoInicio, f))  
						self.solucao[dia][eq-1][gr].append((0, None, iinstancia.turno, 0))
				
				else:
					entrou = False				
			dia = dia +1
			#caso alguma atividade não tenha sido realizada ou completada
			if (dia == iinstancia.dias) and (listaux or inacabadas) :
				for a in listaux:
					custoTotal= custoTotal + 5.0
				break
		
			 
		#armazena o custo da equipe de maior valor
		maiorCusto = 0.0	
		for j in iinstancia.custoEquipe:
			if j > maiorCusto:
				maiorCusto = j
		penalidade = 3 * maiorCusto						
		
		for dia in range(len(self.solucao)):
			
			for equi in range(len(self.solucao[dia])):
				for cont in range (len(self.solucao[dia][equi])):
					if(len(self.solucao[dia][equi][cont])>1):	
					
						if self.solucao[dia][equi][cont][-1][1] != None:
			
							temp = self.solucao[dia][equi][cont][-1][2] + (self.solucao[dia][equi][cont][-1][-1] * tempoTarefa[ (self.solucao[dia][equi][cont][-1][1])-1 ][equi]) + tempoViagem[ self.solucao[dia][equi][cont][-1][0] ][0]
							tempoOcioso = tempoOcioso + (iinstancia.turno - temp)
							self.solucao[dia][equi][cont].append((0, None, temp, 0))	
						tempoUltra= tempoUltra + max(((self.solucao[dia][equi][cont][-1][2]) - iinstancia.turno),0)
						custoTotal= custoTotal + iinstancia.custoEquipe[equi] 
		custoTotal= custoTotal + (tempoUltra * penalidade) + tempoOcioso
		
		return self.solucao, custoTotal	
