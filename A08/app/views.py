from django.shortcuts import render

import pyodbc
from .util_conexao import *


def home(request):
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)

def exercicio1(request):
    # define a página HTML (template) que deverá será carregada
    template = 'exercicio1.html'
    try:
        # obtem a conexao com o BD
        conexao = obter_conexao()

        # define um cursor para executar comandos SQL
        cursor = conexao.cursor()

        sql = '''SELECT * FROM view_uf
                order by unidade_federativa'''

        resultado = cursor.execute(sql).fetchall()
        context = {
            "result": resultado,
        }

        # define a pagina a ser carregada, adicionando os registros das tabelas 
        return render(request, template, context=context)
    
    # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
    except Exception as err:
        return render(request, template, context={'ERRO': err})
