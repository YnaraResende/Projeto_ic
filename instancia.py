class Instancia:
	
	def __init__(self,turno,talhoes,equipes,numAtividades,dias):
		
		self.numAtividades= numAtividades   #numero de atividades  
		self.talhoes=talhoes  		#numero de talhoes
		self.turno=turno     		#turno T que representa o tempo em que as equipes podem trabalhar por dia
		self.equipes=equipes 		#numero de equipes
		self.dias = dias		#numero de dias 
		self.tempoDeslocamento=[] 	#matriz que armazena tempo de deslocamento entre regioes e entre regioes e origem
		self.tempoPadrao= []		#lista que armazena tempo padrão de realizaçao de cada atividade
		self.tamCliente=[]		#lista que armazena tamanho de cada regiao
		self.profEquipe=[]		#lista que armazena proficiencia de cada equipe
		self.custoEquipe=[]		#lista que armazena custo de cada equipe
