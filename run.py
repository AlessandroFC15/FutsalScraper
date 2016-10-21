# Import the email modules we'll need
from email.mime.text import MIMEText
import smtplib
from bs4 import BeautifulSoup
from selenium import webdriver
import unicodedata


def sendEmailFromGmail(email_from, email_password, email_to, content, subject):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_from, email_password)

    email = MIMEText(content)
    email['Subject'] = subject
    email['From'] = email_from
    email['To'] = email_to

    server.send_message(email)
    server.quit()


def normalize_team_name(team_name):
    return unicodedata.normalize("NFKD", team_name[0].getText()).strip()

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
        partida['number'] = numero_partida.replace('| Nr. ', '')

    home_team = p.select('.home.team-name .resumed-name')
    if home_team:
        partida['home_team'] = normalize_team_name(home_team)

    away_team = p.select('.away.team-name .resumed-name')
    if away_team:
        partida['away_team'] = normalize_team_name(away_team)

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


# sendEmailFromGmail("alessandro.sysdata@gmail.com", 'ZOVHHMWIL',"ale-remo@hotmail.com", 'HA-HA!')
