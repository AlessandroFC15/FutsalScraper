# Import the email modules we'll need
from email.mime.text import MIMEText
import smtplib
from bs4 import BeautifulSoup
from selenium import webdriver

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

driver = webdriver.Chrome()

driver.get('http://ligafutsal.com.br/classificacao/')

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

partidas = soup.select('.match_item_right') + soup.select('.match_item_left')

dadosPartidas = []

for p in partidas:
    print(p)

    partida = {}

    data = p.select('.match-date')

    if data:
        partida['data'] = data[0].getText()

    if partida:
        dadosPartidas.append(partida)

    print('------')

print(dadosPartidas)

# sendEmailFromGmail("alessandro.sysdata@gmail.com", 'ZOVHHMWIL',"ale-remo@hotmail.com", 'HA-HA!')
