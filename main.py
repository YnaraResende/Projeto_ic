from Rota import *
from Instancia import *

def main():
	
	arquivo = open("BRKGA.txt","r")
	linhaum = arquivo.readline()
	espaco = linhaum.split()
	regioes= int(espaco[1])
	linhaum = arquivo.readline()
	espaco = linhaum.split()
	atividades= int(espaco[1])
	linhaum = arquivo.readline()
	espaco = linhaum.split()
	equipes= int(espaco[1])
	linhaum = arquivo.readline()
	espaco = linhaum.split()
	turno= int(espaco[1])
	linhaum = arquivo.readline()
	espaco = linhaum.split()
	dias= int(espaco[1])
	objetoInstancia = Instancia(turno,regioes,equipes,atividades,dias)
	objetoRota = Rota(objetoInstancia,arquivo)
	resp = objetoRota.BRKGA(objetoInstancia)
	print(resp)
	arquivo.close()
	
if __name__ == '__main__':
	main()


