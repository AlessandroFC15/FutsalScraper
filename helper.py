from bs4 import BeautifulSoup
from selenium import webdriver
from partida import *
from datetime import datetime


def get_page_html_soup(url):
    driver = webdriver.PhantomJS()

    driver.get(url)

    html = driver.page_source

    return BeautifulSoup(html, 'html.parser')


def encontrar_horarios(url):
    print('>> Visitando %s' % url)

    website = get_page_html_soup(url)

    tabela_exibicoes = website.select('.datagrid')

    exibicoes = []

    for row in tabela_exibicoes[0].find_all('tr'):
        exibicao = {}

        dados = row.find_all('td')

        exibicao['canal'] = dados[0].getText()
        exibicao['horario'] = dados[1].getText()

        exibicoes.append(exibicao)

    return exibicoes


def encontrar_exibicoes_vt(partida):
    lista_id_canais_sportv = [443, 444, 2691]

    url = "https://www1.sky.com.br/servicos/Guiadatv/CanalDetalhe.aspx?qChave="

    url_detalhes = "https://www1.sky.com.br/servicos/Guiadatv/"

    for canal in lista_id_canais_sportv:
        url_canal = url + str(canal)

        print('>> Visitando %s' % url_canal)

        website = get_page_html_soup(url_canal)

        tabela_programacao = website.select('.gvCanalDetalhes')

        if tabela_programacao:
            table_rows = tabela_programacao[0].tbody.find_all('tr')

            for row in table_rows:
                dados = row.find_all('td')

                date = dados[1].getText().strip()
                horario = dados[3].getText().strip()
                hora, minuto = [int(x) for x in horario.split(':')]
                descricao = dados[5].getText().strip()
                link = dados[5].a['href']

                if 'liga futsal' in descricao.lower() and partida.dateTime.hour == hora and partida.dateTime.minute == minuto:
                    print(partida)
                    return encontrar_horarios(url_detalhes + link)

        print('-------------')

        # encontrar_exibicoes_vt(Partida(number=1, date=datetime.strptime("22/10/2016 11:00", '%d/%m/%Y %H:%M'), home_team='Magnus',
        #                                away_team='Intelli', tv_transmission=True))
