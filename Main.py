from Rota import *
from Instancia import *
from BRKGA import *

def main():
	
	arquivo = open("teste.txt","r")
	arq = open("arqX.txt","w")
	objetoInstancia = Instancia.Instancia()
	objetoInstancia.inputArq(arquivo)
	objetoBRKGA = BRKGA()
	resp = objetoBRKGA.BRKGA(objetoInstancia,arq)
	arq.write(str(resp))
	arquivo.close()
	arq.close()
	
if __name__ == '__main__':
	main()
