import Rota
from Instancia import *

def main():
	
	arquivo = open("projetoic.txt","r")
	turno= int(arquivo.readline())
	talhoes = int(arquivo.readline())
	equipes = int(arquivo.readline())
	atividades = int(arquivo.readline())
	linha = arquivo.readline()
	b= Instancia.init(turno,talhoes,equipes,atividades)
	a=Rota.init()
	resp = a.CalcularTempo(b)
	print(resp)
	arquivo.close()
	
main()
