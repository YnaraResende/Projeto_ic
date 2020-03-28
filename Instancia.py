class Instancia:
	
	def __init__(self):
		
		self.atividades={} 			#atividades que devem ser concluidas em cada talhao, em ordem de precedencia
		self.numAtividades= None  	#numero de atividades  
		self.talhoes= None  			#numero de talhoes
		self.turno= None  				#turno T que representa o tempo em que as equipes podem trabalhar por dia
		self.equipes= None				#numero de equipes
		self.dias=None					#numero de dias 
		self.tempoDeslocamento=[] 		#matriz que armazena tempo de deslocamento entre regioes e entre regioes e origem
		self.tempoPadrao= []			#lista que armazena tempo padrão de realizaçao de cada atividade
		self.tamCliente=[]				#lista que armazena tamanho de cada regiao
		self.profEquipe=[]				#lista que armazena proficiencia de cada equipe
		self.custoEquipe=[]				#lista que armazena custo de cada equipe
		self.tempoTarefa = []			#matriz que armazena o tempo de duração de cada tarefa para cada equipe
		 	
	'''
	Parâmetros:
		arquivo - arquivo de entrada 
			
	Ideia: a função faz a leitura de todo o arquivo de entrada, inicializa o dicionário self.atividades e calcula o tempo de duração de cada atividade
	 para cada equipe, colocando os valores na matriz self.tempoTarefa.
		
	'''		
	def inputArq(self, arquivo):
		
		#leitura do arquivo
		linhaum = arquivo.readline()
		espaco = linhaum.split()
		self.talhoes= int(espaco[1])
		linhaum = arquivo.readline()
		espaco = linhaum.split()
		self.numAtividades = int(espaco[1])
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
			linha = arquivo.readline()
			espaco = linha.split()
			cont = int(espaco[1])
			ite = 2
			while cont != -1:
				self.atividades[i].append(cont)
				cont = int(espaco[ite])
				ite = ite+1
				
		arquivo.readline()
		
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
		
		for i in range (0, self.numAtividades):
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
		
		#inicialização self.tempoTarefa
		for i in range (0, self.numAtividades):
			linha = []
			for j in range (0, self.equipes):
				linha.append(" ")
			self.tempoTarefa.append(linha[:])
		
		#cálculo da duração das atividades por cada equipe e armazenamento dos valores na matriz self.tempoTarefa
		for c,v in self.atividades.items():
			for ajuda in range (0, len(v)):
				i =  self.atividades[c][ajuda]
				for j in range (0, self.equipes):
					self.tempoTarefa[i-1][j]= (self.tamCliente[c+1]*self.tempoPadrao[i-1])/self.profEquipe[j]
			

