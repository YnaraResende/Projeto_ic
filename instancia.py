class Instancia:
	
	def init(self,turno,talhoes,equipes,numAtividades):
		
		self.numAtividades= numAtividades   #numero de atividades
		self.tempoTarefa=[]   #matriz para armazear tempo NxM em que N representa as equipes e M as atividades 
		self.talhoes=talhoes  #numero de talhoes
		self.turno=turno     #turno T que representa o tempo em que as equipes podem trabalhar por dia
		self.equipes=equipes #numero de equipes
		self.tempoDeslocamento=[] #matriz que armazena tempo de deslocamento entre atividades e entre atividades e origem, entre atividades
									#de um mesmo talhao nao devem ter tempo calculado
									#numAtividades+1 X numAtividades+1, 0 representa origem.
