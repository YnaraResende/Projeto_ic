import Instancia

class Rota:
	
	def init(self):
		self.rotaEq={}  # dicionario que possui cada equipe relacionada com as atividades que irão realizar (ordenada)
						#chave = equipes
		self.atividades={} #atividades que devem ser concluidas em cada talhao, em ordem de precedencia
		self.tempoAtividade=[] #matriz numAtividades x 2 que armazena atividades com seu tempo de inicio e fim
		self.CalcularTempo(self,iinstancia) #funcao para calcular tempo em dias gasto para realizar todas as atividades
		self.dia = 1
		self.ajuda=0
		self.equipeAtual= None
	
	
		
	def CalcularTempo(self,iinstancia):
		
		for i in range (1, iinstancia.equipes):
			rotaEq[i] = [] 	 
	
		for i in range (1, iinstancia.talhoes):
			atividades[i] = []
		
		for i in range (iinstancia.equipes):
			linha = arquivo.readline()
			espaco = linha.split(",")
			cont = int(espaco[1])
			ite = 2
			while cont != -1:
				rotaEq[i].append(cont)
				cont = int(espaco[ite])
				ite= ite+1
			
		linha = arquivo.readline()
	
		for i in range (iinstancia.talhoes):
			linha = arquivo.readline()
			espaco = linha.split(",")
			cont = int(espaco[0])
			ite = 2
			while cont != -1:
				atividades[i],append(cont)
				cont = int(espaco[ite])
				ite = ite+1
				
		linha = arquivo.readline()
	
		for i in range (iinstancia.equipes):
			linha= arquivo.readline()
			espaco = linha.split()
			tmp =[]
			for j in range (iinstancia.numAtividades):
				elemento = float(espaco[j])
				tmp.append(elemento)
			iinstancia.tempoTarefa.append(tmp[:])
			
		linha = arquivo.readline()
		
		for i in range (iinstancia.numAtividades+1):
			linha = arquivo.readline()
			espaco =  linha.split()
			tmp = []
			for j in range (iinstancia.numAtividades+1):
				elemento = float(espaco[j])
				tmp.apped(elemento)
			iinstancia.tempoDeslocamento.append(tmp[:])
		
		maior = 0
		chave_maior = None
		for chave, valor in atividades.items():
			if len(valor) > maior:
				maior = len(valor)
		
		for auxiliar in range (1, maior):
			for cont in range(1,iinstancia.talhoes):
				self.aux =[]
				self.aux2=[]
				ativ=atividades[cont][auxiliar]
				
				for k,v in rotaEq.items(): 
					if v == ativ: 
						equipe = k
						
				if auxiliar == 1:
					if rotaEq[equipe][1] == ativ:
						tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ] #matriz tempoAtividade recebe na primeira coluna(que armazena tempo de 
						#inicio de cada atividade) tempo de deslocamento da origem para cada atividade	
					
						if tempoAtividade[ativ-1][0] + tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): #se tempo de termino da 
						#atividade for maior que o permitido 
							tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) - 
							(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) 
							dia= dia + 1
						
						else:
							tempoAtividade[ativ-1][1] = tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] #matriz tempoAtividade recebe na segunda 
							#coluna(que armazena tempo final de cada atividade) tempo do inicio da atividade + tempo em que a tarefa foi 
							#executada pela equipe
					else:
						for valor in rotaEq[k]: 
							aux.append(valor)
								
						for c in range (0, len[aux]): 
							if aux[c] == ativ: #encontrar atividade na lista aux
								anterior = aux[c-1] #armazenar atividade realizada anteriormente pela equipe
								indiceAntUm = c-1
							
						if tempoAtividade[anterior-1][1]+ iintancia.tempoDeslocamento[ativ][anterior] > (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):
							tempoAtividade[ativ-1][0]=iinstancia.tempoDeslocamento[0][ativ]
							dia=dia+1
						else:
							tempoAtividade[ativ-1][0] = tempoAtividade[anterior-1][1]+ iintancia.tempoDeslocamento[ativ][anterior]
						
						if tempoAtividade[ativ-1][0] + tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):
							tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -
									(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) #tempo final recebe tempo de deslocamento da origem + o tempo restante 
									#para concluir a atividade
							dia= dia + 1
						else:
							tempoAtividade[ativ-1][1] = tempoAtividade[ativ-1][0] + tempoTarefa[equipe-1][ativ-1]
						
				else:
					for k,v in rotaEq.items(): #pegar atividades que são realizadas pela equipe
						if v == ativ: #se o valor do dicionario for igual a atividade em questao
							for valor in rotaEq[k]: 
								aux.append(valor) #armazenar atividades feita pela equipe em uma lista aux
				
					for c in range (0, len[aux]): 
						if aux[c] == ativ: #encontrar atividade na lista aux
							if c-1 >= 0:
								anterior = aux[c-1] #armazenar atividade realizada anteriormente pela equipe
								indiceAntUm = c-1	#e seu indice
							else:
								anterior = None
								indiceAntUm = None
								
					anterior2= atividades[cont][auxiliar-1]
				
					if anterior == anterior2:
						
						tempoAtividade[ativ-1][0] = tempoAtividade[anterior-1][1] #tempo de inicio da atividade recebe tempo final da anterior
						
						if tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (turno-iinstancia.tempoDeslocamento[0][ativ]):#se tempo de 
							#termino for maior que o permitido
							tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((tempoAtividade[ativ-1][0]+iinstancia.tempoTarefa[equipe-1][ativ-1]) - 
								(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) #tempo final recebe tempo de deslocamento da origem + o tempo 
								#restante para concluir a atividade
							dia= dia + 1
						else:
							tempoAtividade[ativ-1][1] = tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] #tempo final recebe tempo de
							# inicio da atividade + tempo que a equipe demora para realizar a atividade
					
							
					else: #se não é do mesmo talhão
						if anterior != None:
							if tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] > tempoAtividade[anterior2-1][1]:#se tempo
								#da equipe iniciar a atividade for maior que tempo de termino da atividade anterior do talhao
								
								if tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][i] >(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]):
									#se o tempo final da atividade realizada anteriormente pela equipe + tempo de deslocamento for maior que o permitido
									tempoAtividade[ativ-1][0] = iinstancia.tempoDeslocamento[0][ativ]   
									dia = dia + 1
								else:
									tempoAtividade[ativ-1][0] = tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior][ativ] #tempo de 
									#inicio recebe tempo final de atividade realizada anteriormente pela equipe + tempo deslocamento 
								
								if tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): #se tempo final da 
									#atividade atual for maior que o permitido 
									tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -
										(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) #tempo final recebe tempo de deslocamento da origem + o tempo restante 
										#para concluir a atividade
									dia= dia + 1
								
								else:
									tempoAtividade[ativ-1][1] = tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][i-1]
									
							elif tempoAtividade[anterior-1][1] + iinstancia.tempoDeslocamento[anterior-1][ativ] < tempoAtividade[anterior2-1][1]:
								
								tempoAtividade[ativ-1][0] = tempoAtividade[anterior2-1][1]
								
								if tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1] >(iinstancia.turno- iinstancia.tempoDeslocamento[0][ativ]):#se tempo final da 
									#atividade atual for maior que o permitido 
									tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((tempoAtividade[ativ-1][0] + tempoTarefa[equipe-1][ativ-1]) -
										(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ]))	#tempo final recebe tempo de deslocamento da origem + o tempo restante 
										#para concluir a atividade
									dia= dia + 1
								
								
						else:
							tempoAtividade[ativ-1][0] = tempoAtividade[anterior2-1][1]
							
							if tempoAtividade[ativ-1][0]+ tempoTarefa[equipe-1][ativ-1] > (iinstancia.turno-iinstancia.tempoDeslocamento[0][ativ]): #se tempo final da 
								#atividade atual for maior que o permitido 
								tempoAtividade[ativ-1][1] = iinstancia.tempoDeslocamento[0][ativ] + ((tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][ativ-1]) -
									(iinstancia.turno - iinstancia.tempoDeslocamento[0][ativ])) #tempo final recebe tempo de deslocamento da origem + o tempo restante 
									#para concluir a atividade
								dia= dia + 1
								
							else:
								tempoAtividade[ativ-1][1] = tempoAtividade[ativ-1][0] + iinstancia.tempoTarefa[equipe-1][i-1]
							
							
		return int(dias)
