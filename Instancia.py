class Instancia:
	
	def __init__(self):
		
		self.atividades={} 			#atividades que devem ser concluidas em cada talhao, em ordem de precedencia
		self.ativTalhao= None		#numero de atividades por talhão
		self.numAtividades= None  	#numero de atividades  no total
		self.talhoes= None  			#numero de talhoes
		self.turno= None  				#turno que representa o tempo em que as equipes podem trabalhar por dia
		self.equipes= None				#numero de equipes
		self.dias=None					#numero de dias 
		self.tempoDeslocamento=[] 		#matriz que armazena tempo de deslocamento entre regiões e entre regiões e origem
		self.tempoPadrao= []			#lista que armazena tempo padrão de realização de cada atividade
		self.tamCliente=[]				#lista que armazena tamanho de cada região
		self.profEquipe=[]				#lista que armazena proficiência de cada equipe
		self.custoEquipe=[]				#lista que armazena custo de cada equipe
		self.tempoTarefa = []			#matriz que armazena o tempo de duração de cada tarefa para cada equipe
		self.quant = []					#lista que armazena número de grupos de atividades das equipes
		self.quantMax = None			#número de grupos de atividades no total
		 	
	'''
	Parâmetros:
		arquivo - arquivo de entrada 
			
	Ideia: a função faz a leitura de todo o arquivo de entrada, inicializa o dicionário self.atividades de acordo com o número de atividades e calcula o
	 tempo de duração de cada atividade para cada equipe, armazenando os valores na matriz self.tempoTarefa.
		
	'''		
	def inputArq(self, arquivo):
		
		#leitura do arquivo
		linhaum = arquivo.readline()
		espaco = linhaum.split()
		self.talhoes= int(espaco[1])
		linhaum = arquivo.readline()
		espaco = linhaum.split()
		self.ativTalhao = int(espaco[1])
		self.numAtividades = self.ativTalhao*(self.talhoes-1)
		linhaum = arquivo.readline()
		espaco = linhaum.split()
		self.equipes= int(espaco[1])
		linhaum = arquivo.readline()
		espaco = linhaum.split()
		self.turno= int(espaco[1])
		linhaum = arquivo.readline()
		espaco = linhaum.split()
		self.dias= int(espaco[1])
		arquivo.readline()

		for i in range (0, (self.talhoes-1)):	#self.talhoes-1 porque self.talhoes representa numero de talhoes + deposito
			self.atividades[i] = []
			
		for i in range (0,(self.talhoes-1)):
			if i != 0:
				cont = (self.atividades[i-1][self.ativTalhao-1])+1
			else:
				cont = i+1
			for z in range(cont, cont+self.ativTalhao):
				self.atividades[i].append(z)
		
		for i in range (0, self.talhoes):
			linha = arquivo.readline()
			espaco =  linha.split()
			tmp = []
			for j in range (0, self.talhoes):
				elemento = float(espaco[j])
				tmp.append(elemento)
			self.tempoDeslocamento.append(tmp[:])
			
		arquivo.readline()
		linha = arquivo.readline()
		espaco =  linha.split()
		
		for i in range (0, self.ativTalhao):
			elemento=float(espaco[i])
			self.tempoPadrao.append(elemento)
			
		arquivo.readline()
		linha = arquivo.readline()
		espaco =  linha.split()
		for i in range (0, self.talhoes):
			elemento=float(espaco[i])
			self.tamCliente.append(elemento)
			
		arquivo.readline()
		linha = arquivo.readline()
		espaco =  linha.split()
		
		for i in range (0, self.equipes):
			elemento=float(espaco[i])
			self.profEquipe.append(elemento)
			
		arquivo.readline()
		linha = arquivo.readline()
		espaco =  linha.split()
		for i in range (0, self.equipes):
			elemento=float(espaco[i])
			self.custoEquipe.append(elemento)
		
		linhaum = arquivo.readline()
		espaco = linhaum.split()
		for j in range (1,self.equipes+1):
			self.quant.append(int(espaco[j]))
			
		linhaum = arquivo.readline()
		espaco = linhaum.split()
		self.quantMax= int(espaco[1])
		
		for i in range (0, self.numAtividades):
			linha = []
			for j in range (0, self.equipes):
				linha.append(" ")
			self.tempoTarefa.append(linha[:])
		
		for c,v in self.atividades.items():
			for ajuda in range (0, len(v)):
				i =  self.atividades[c][ajuda]
				for j in range (0, self.equipes):
					self.tempoTarefa[i-1][j]= (self.tamCliente[c+1]*self.tempoPadrao[ajuda])/self.profEquipe[j]
