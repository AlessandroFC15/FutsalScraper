from bs4 import BeautifulSoup
from selenium import webdriver
import unicodedata, pytz
from datetime import datetime
from sendMail import *
from partida import *

def get_page_html_soup(url):
    driver = webdriver.PhantomJS()

    driver.get(url)

    html = driver.page_source

    return BeautifulSoup(html, 'html.parser')

def normalize_team_name(team_name):
    return unicodedata.normalize("NFKD", team_name[0].getText()).strip()

def sendMail(listaPartidas):
    today = datetime.now(tz=pytz.timezone('America/Belem'))

    partidasDeHoje = []

    for partida in listaPartidas:
        if partida.dateTime.day == today.day and partida.dateTime.month == today.month and partida.dateTime.year == today.year and \
                partida.tv_transmission:
            partidasDeHoje.append(partida)
            print('Partida %s ocorre hoje!' % partida)

    if partidasDeHoje:
        print('>> Enviando e-mail...')
        sendEmailFromGmail('alessandro.sysdata@gmail.com', 'ZOVHHMWIL', 'ale-remo@hotmail.com', partidasDeHoje)
        print('>> E-mail enviado!')

print('>> Iniciando coleta de dados...')

website = get_page_html_soup('http://ligafutsal.com.br/classificacao/')

partidas = website.select('.match_item_right') + website.select('.match_item_left')

dadosPartidas = []

for p in partidas:
    partida = Partida()

    data = p.select('.match-date')
    if data:
        data_partida, numero_partida = data[0].getText().split('\n')
        data_partida, time_partida = map(lambda x: x.strip(), data_partida.split('|'))

        partida.number = int(numero_partida.replace('| Nr. ', ''))

        partida.dateTime = datetime.strptime(data_partida + ' ' + time_partida, '%d/%m/%Y %H:%M')

    home_team = p.select('.home.team-name .resumed-name')
    if home_team:
        partida.home_team = normalize_team_name(home_team)
    else:
        continue

    away_team = p.select('.away.team-name .resumed-name')
    if away_team:
        partida.away_team = normalize_team_name(away_team)
    else:
        continue

    sportv_transmission = p.select('.match-place img[alt=SporTV]')
    partida.tv_transmission = True if sportv_transmission else False

    # Caso a partida possua placar, não nos interessa mais.
    home_team_score = p.select('.home.team-points')
    if home_team_score:
        if home_team_score[0].getText().strip():
            continue

    away_team_score = p.select('.away.team-points')
    if away_team_score:
        if away_team_score[0].getText().strip():
            continue

    if partida:
        dadosPartidas.append(partida)

sendMail(dadosPartidas)
