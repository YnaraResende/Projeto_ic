from Rota import *
from Instancia import *

def main():
	
	arquivo = open("BRKGA.txt","r")
	turno= int(arquivo.readline())
	talhoes = int(arquivo.readline())
	equipes = int(arquivo.readline())
	atividades = int(arquivo.readline())
	linha = arquivo.readline()
	objetoInstancia = Instancia(turno,talhoes,equipes,atividades)
	objetoRota = Rota(objetoInstancia,arquivo)
	resp = objetoRota.BRKGA(objetoInstancia)
	print(resp)
	arquivo.close()
	
if __name__ == '__main__':
	main()


