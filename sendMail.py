import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from helper import *

def sendEmailFromGmail(email_from, email_password, email_to, listaPartidas):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_from, email_password)

    email = MIMEMultipart('alternative')
    email['Subject'] = 'Lista de jogos da Liga Futsal'
    email['From'] = email_from
    email['To'] = email_to

    content = ''

    for partida in listaPartidas:
        content += "<p><strong> %s</strong></p><br>" % partida

        exibicoes_vt = encontrar_exibicoes_vt(partida)
        if exibicoes_vt:
            content += "<p><em></em></p><br>" % exibicoes_vt
        else:
            content += '<p>Sem vt, bitches!</p><br>'

    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    html = """\
    <html>
      <head></head>
      <body>
        <p>Olá,</p>
        <br>
        <p>Segue abaixo os jogos de futsal de hoje: </p>
        <br>
        %s
      </body>
    </html>
    """ % content
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    email.attach(part1)
    email.attach(part2)

    server.send_message(email)
    server.quit()