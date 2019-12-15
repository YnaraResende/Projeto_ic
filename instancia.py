class Instancia:
	
	def __init__(self,turno,talhoes,equipes,numAtividades):
		
		self.numAtividades= numAtividades   #numero de atividades
		self.tempoTarefa=[]   			#matriz para armazenar tempo em que cada equipe realiza cada atividade  
		self.talhoes=talhoes  			#numero de talhoes
		self.turno=turno     			#turno T que representa o tempo em que as equipes podem trabalhar por dia
		self.equipes=equipes 			#numero de equipes
		self.tempoDeslocamento=[] 		#matriz que armazena tempo de deslocamento entre atividades e entre atividades e origem
