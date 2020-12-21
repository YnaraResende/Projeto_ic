from Rota import *
from Instancia import *
from BRKGA import *
import time
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#definição do layout do dashboard
app.layout = html.Div([
    html.H6("Insira o nome do arquivo a ser tratado:"),
    html.Div(["Input: ",
              dcc.Input(id="input1", type="text", placeholder="", debounce=True)
              ]),
    html.Br(),
    dcc.Graph(id = "my-output")
	
])
#com base na inserção do nome do arquivo o retorno é um gráfico
@app.callback(
    Output(component_id='my-output', component_property='figure'),
    Input("input1", "value")
)

def update_output(input1):
		#delay para que o usuário insira o nome do arquivo
		time.sleep(30)
		arquivo = open(str(input1),"r")
		arq = open("arqX.txt","w")
		objetoInstancia = Instancia.Instancia()
		objetoInstancia.inputArq(arquivo)
		objetoBRKGA = BRKGA(0.7, 0.1, 0.7)
		resp, sol = objetoBRKGA.BRKGA(objetoInstancia,arq)
		ajd = resp
		arq.write(str(resp))
		arquivo.close()
		arq.close()
		
		#com base no dicionário de rotas gerado, há formação de listas, que armazenam os dados do dashboard				
		ativs = []
		inicio = []
		fim = []
		cor = []
							
		for dia in range(len(ajd)):
			for equi in range(len(ajd[dia])):
				for cont in range (len(ajd[dia][equi])):
					if(len(ajd[dia][equi][cont])>1):	
						for a in (ajd[dia][equi][cont]):
							if a[1] != None:
								horaInicio = a[2]
								hours = (int(horaInicio)+8)
								minutes = (horaInicio*60) % 60
								seconds = (horaInicio*3600) % 60
								horaComeco = ("%d:%02d:%02d" % (hours, minutes, seconds))
													
								horaFim = horaInicio + (a[-1]*objetoInstancia.tempoTarefa[(a[1]-1)][equi])
								hours = (int(horaFim)+8)
								minutes = (horaFim*60) % 60
								seconds = (horaFim*3600) % 60
								horaFinal = ("%d:%02d:%02d" % (hours, minutes, seconds))
													
					
								ativs.append('Atividade ' + str(a[1]))	
								inicio.append(pd.to_datetime('2020-12-0'+ str(dia+1) +' '+ horaComeco))
								fim.append(pd.to_datetime('2020-12-0'+ str(dia+1) +' '+ horaFinal))
								cor.append(str(equi+1))
							
		data = {'Task': ativs, 
				'Start': inicio,
				'Finish': fim,	
				'Team': cor}			
													
		df = pd.DataFrame(data)
							
		fig = go.Figure()

		fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color = "Team")
							
		fig.update_yaxes(autorange="reversed")
	
	
		return (fig)


if __name__ == '__main__':
	app.run_server(debug=True)
