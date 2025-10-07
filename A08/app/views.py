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

def ranking_municipios(request):
    # define a página HTML (template) que deverá será carregada
    template = 'ranking_municipios.html'
    try:
        # obtem a conexao com o BD
        conexao = obter_conexao()

        # define um cursor para executar comandos SQL
        cursor = conexao.cursor()

        sql = '''SELECT TOP(15)
                    (m.nome + ' (' + m.uf + ')'), count(*) as QTD_CAMPI
                    FROM Municipio m
                    inner join Campus c on c.id_municipio = m.id_municipio
                    group by (m.nome + ' (' + m.uf + ')')
                    order by QTD_CAMPI desc'''

        resultado = cursor.execute(sql).fetchall()
        context = {
            "ranking": resultado,
        }

        # define a pagina a ser carregada, adicionando os registros das tabelas 
        return render(request, template, context=context)
    
    # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
    except Exception as err:
        return render(request, template, context={'ERRO': err})

def ranking_ofertas(request):
    # define a página HTML (template) que deverá será carregada
    template = 'ranking_ofertas_uf.html'
    try:
        # obtem a conexao com o BD
        conexao = obter_conexao()

        # define um cursor para executar comandos SQL
        cursor = conexao.cursor()

        sql = '''
                select distinct
                    m.uf
                    from Municipio m'''

        # obtem a quantidade de registros de Instituicoes Financeiras
        # obtem o valor retornado usando "fetchval"
        ufs = cursor.execute(sql).fetchall()

        dados_ranking = []
        for reg in ufs:
            sigla = reg[0]
            sql = f'''
                select top(10)
                    c.nome, count(*), round(avg(co.enade), 2), min(co.enade) as minimum, max(co.enade) as maximum
                from Cursos_Oferecidos_por_Campus co
                inner join Curso c on c.id_curso = co.id_curso
                inner join Campus on Campus.id_campus = co.id_campus
                inner join Municipio m on m.id_municipio = Campus.id_municipio
                where m.uf = '{sigla}'
                group by c.nome
                having round(avg(co.enade), 2) >= 2.5
                order by count(*) desc
            '''
            resultado = cursor.execute(sql).fetchall()
            dados_ranking.append({"uf": sigla, "resultado": resultado})

        context = {
            "ranking": dados_ranking
        }
        # define a pagina a ser carregada, adicionando os registros das tabelas 
        return render(request, template, 
                    context=context)
    
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
