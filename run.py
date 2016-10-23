import unicodedata, pytz
from sendMail import *
from helper import *


def normalize_team_name(team_name):
    return unicodedata.normalize("NFKD", team_name[0].getText()).strip()


def get_team_name(css_selector):
    team = p.select(css_selector + '.team-name .resumed-name')
    if team:
        return normalize_team_name(team)


def team_has_score(css_selector):
    team_score = p.select(css_selector + '.team-points')
    return team_score and team_score[0].getText().strip()


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

# Coleta de partidas da coluna direita e esquerda
partidas = website.select('.match_item_right') + website.select('.match_item_left')

dadosPartidas = []

for p in partidas:
    partida = Partida()

    data = p.select('.match-date')
    if data:
        data_horario_partida, numero_partida = data[0].getText().split('\n')
        data_partida, horario_partida = map(lambda x: x.strip(), data_horario_partida.split('|'))

        partida.number = int(numero_partida.replace('| Nr. ', ''))
        partida.dateTime = datetime.strptime(data_partida + ' ' + horario_partida, '%d/%m/%Y %H:%M')

    partida.home_team = get_team_name('.home')
    partida.away_team = get_team_name('.away')
    # Caso a partida não possua os 2 times definidos, será ignorada
    if not (partida.home_team and partida.away_team):
        continue

    # Caso a partida possua placar, não nos interessa mais.
    if team_has_score('.home') or team_has_score('.away'):
        continue

    partida.tv_transmission = True if p.select('.match-place img[alt=SporTV]') else False

    if partida:
        dadosPartidas.append(partida)

# encontrar_exibicoes_vt(dadosPartidas[0])

sendMail(dadosPartidas)
