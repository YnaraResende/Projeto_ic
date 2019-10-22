from Rota import *
from Instancia import *

def main():
	
	arquivo = open("projetoic.txt","r")
	turno= int(arquivo.readline())
	talhoes = int(arquivo.readline())
	equipes = int(arquivo.readline())
	atividades = int(arquivo.readline())
	linha = arquivo.readline()
	objetoInstancia = Instancia(turno,talhoes,equipes,atividades)
	objetoRota = Rota()
	resp = objetoRota.CalcularTempo(objetoInstancia,arquivo)
	print(resp)
	arquivo.close()
	
if __name__ == '__main__':
	main()

