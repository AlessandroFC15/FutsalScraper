from django.http import HttpResponse
from bs4 import BeautifulSoup
from selenium import webdriver
import unicodedata
from .models import *
from datetime import datetime
import pytz
from .send_mail import *

def loadData(request):
    def normalize_team_name(team_name):
        return unicodedata.normalize("NFKD", team_name[0].getText()).strip()

    Match.objects.all().delete()

    print('>> Iniciando coleta de dados...')

    driver = webdriver.PhantomJS()

    driver.get('http://ligafutsal.com.br/classificacao/')

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    partidas = soup.select('.match_item_right') + soup.select('.match_item_left')

    dadosPartidas = []

    for p in partidas:
        partida = {}

        data = p.select('.match-date')
        if data:
            data_partida, numero_partida = data[0].getText().split('\n')
            partida['data'], partida['time'] = map(lambda x: x.strip(), data_partida.split('|'))
            partida['number'] = int(numero_partida.replace('| Nr. ', ''))

            partida['dateTime'] = datetime.strptime(partida['data'] + ' ' + partida['time'], '%d/%m/%Y %H:%M')


        home_team = p.select('.home.team-name .resumed-name')
        if home_team:
            partida['home_team'] = normalize_team_name(home_team)
        else:
            continue

        away_team = p.select('.away.team-name .resumed-name')
        if away_team:
            partida['away_team'] = normalize_team_name(away_team)
        else:
            continue

        sportv_transmission = p.select('.match-place img[alt=SporTV]')
        partida['sportTV_transmission'] = True if sportv_transmission else False

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

    for partida in dadosPartidas:
        print(partida)

        try:
            match = Match.objects.get(pk=partida['number'])
            print(">> Partida %s já cadastrada" % match)
        except:
            match = Match.create(partida['dateTime'], partida['number'], partida['home_team'], partida['away_team'], partida['sportTV_transmission'])
            match.save()
            print(">> Partida %s foi cadastrada" % match)

    return HttpResponse("Hello, world. You're at the polls index.")

def sendMail(request):
    listaPartidas = Match.objects.all()
    today = datetime.now(tz=pytz.timezone('America/Belem'))

    partidasDeHoje = []

    for partida in listaPartidas:
        if partida.date.day == today.day and partida.date.month == today.month and partida.date.year == today.year and \
                partida.tv_transmission:
            partidasDeHoje.append(partida)
            print('Partida %s ocorre hoje!' % partida)

    if partidasDeHoje:
        print('>> Enviando e-mail...')
        sendEmailFromGmail('alessandro.sysdata@gmail.com', 'ZOVHHMWIL', 'edson.alessandro96@gmail.com', partidasDeHoje)
        print('>> E-mail enviado!')

    return HttpResponse("Hello, world. You're at the polls index.")
