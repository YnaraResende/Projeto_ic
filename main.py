from RotaRascunhoTeste import *
from Instancia import *

def main():
	
	arquivo = open("teste.txt","r")
	arq = open('arqX.txt','w')
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
	resp = objetoRota.BRKGA(objetoInstancia,arq)
	arq.write(str(resp))
	arquivo.close()
	arq.close()
	
if __name__ == '__main__':
	main()
