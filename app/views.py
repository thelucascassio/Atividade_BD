from django.shortcuts import render

import pyodbc
from .util_conexao import *


def home(request):
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)


def dados_gerais(request):
    # define a página HTML (template) que deverá será carregada
    template = 'dados_gerais.html'
    try:
        # obtem a conexao com o BD
        conexao = obter_conexao()

        # define um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # obtem a quantidade de registros de Instituicoes Financeiras
        sql = 'SELECT count(*) FROM IES '
        # obtem o valor retornado usando "fetchval"
        count_ies = cursor.execute(sql).fetchval()

        # obtem a quantidade de registros de Cursos
        sql = 'SELECT count(*) FROM campus '
        count_campus = cursor.execute(sql).fetchval()

        # obtem a quantidade de registros de Cursos
        sql = 'SELECT count(*) FROM curso '
        count_cursos = cursor.execute(sql).fetchval()

        # obtem a quantidade de registros de Cursos
        sql = 'SELECT count(*) FROM cursos_oferecidos_por_campus '
        count_ofertas = cursor.execute(sql).fetchval()

        # obtem a quantidade de registros de Cursos
        sql = 'SELECT count(*) FROM area '
        count_areas = cursor.execute(sql).fetchval()

        # define a pagina a ser carregada, adicionando os registros das tabelas 
        return render(request, template, 
                    context={
                          'count_ies': count_ies,
                          'count_campus': count_campus,
                          'count_cursos': count_cursos,
                          'count_ofertas': count_ofertas,
                          'count_areas': count_areas,
                    })
    
    # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
    except Exception as err:
        return render(request, template, context={'ERRO': err})

def campi_por_uf(request):
    template = 'campi_por_uf.html'
    
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        count_ies = cursor.execute('SELECT count(*) FROM IES').fetchval()
        count_campus = cursor.execute('SELECT count(*) FROM campus').fetchval()
        count_cursos = cursor.execute('SELECT count(*) FROM curso').fetchval()
        count_ofertas = cursor.execute('SELECT count(*) FROM cursos_oferecidos_por_campus').fetchval()
        count_areas = cursor.execute('SELECT count(*) FROM area').fetchval()


        sql_uf = '''
            SELECT m.uf, COUNT(c.id_campus) AS qtd_campi
            FROM Campus c
            JOIN Municipio m ON c.id_municipio = m.id_municipio
            GROUP BY m.uf
            ORDER BY m.uf ASC;
        '''
        cursor.execute(sql_uf)
        resultados_uf = cursor.fetchall()

        
        campi_por_uf = [{'uf': row[0], 'qtd_campi': row[1]} for row in resultados_uf]

       
        return render(request, template, context={
            'count_ies': count_ies,
            'count_campus': count_campus,
            'count_cursos': count_cursos,
            'count_ofertas': count_ofertas,
            'count_areas': count_areas,
            'campi_por_uf': campi_por_uf  
        })

    except Exception as err:
        return render(request, template, context={'ERRO': err})



def cursos_por_area(request):
    
    template = 'cursos_por_area.html'
    
    try:
       
        conexao = obter_conexao()
        cursor = conexao.cursor()

        
        count_ies = cursor.execute('SELECT count(*) FROM IES').fetchval()
        count_campus = cursor.execute('SELECT count(*) FROM campus').fetchval()
        count_cursos = cursor.execute('SELECT count(*) FROM curso').fetchval()
        count_ofertas = cursor.execute('SELECT count(*) FROM cursos_oferecidos_por_campus').fetchval()
        count_areas = cursor.execute('SELECT count(*) FROM area').fetchval()

       
        sql_uf = '''
            SELECT m.uf, COUNT(c.id_campus) AS qtd_campi
            FROM Campus c
            JOIN Municipio m ON c.id_municipio = m.id_municipio
            GROUP BY m.uf
            ORDER BY m.uf ASC;
        '''
        cursor.execute(sql_uf)
        resultados_uf = cursor.fetchall()
        campi_por_uf = [{'uf': row[0], 'qtd_campi': row[1]} for row in resultados_uf]

      
        sql_area = '''
            SELECT a.descricao AS area_conhecimento,
                   COUNT(c.id) AS quantidade_cursos
            FROM Cursos_Oferecidos_por_Campus c
            JOIN Area a ON c.id_area = a.id_area
            GROUP BY a.descricao
            ORDER BY a.descricao ASC;
        '''
        cursor.execute(sql_area)
        resultados_area = cursor.fetchall()
        cursos_por_area = [{'area_conhecimento': row[0], 'quantidade_cursos': row[1]} for row in resultados_area]

      
        return render(request, template, context={
            'count_ies': count_ies,
            'count_campus': count_campus,
            'count_cursos': count_cursos,
            'count_ofertas': count_ofertas,
            'count_areas': count_areas,
            'campi_por_uf': campi_por_uf,
            'cursos_por_area': cursos_por_area  
        })

    except Exception as err:
        return render(request, template, context={'ERRO': err})
