from django_cron import CronJobBase, Schedule
from ..models import *
from datetime import datetime
import pytz

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        print('>> I am here <<')

        listaPartidas = Match.objects.all()
        today = datetime.now(tz=pytz.timezone('America/Belem'))

        partidasDeHoje = []

        for partida in listaPartidas:
            if partida.date.day == today.day and partida.date.month == today.month and partida.date.year == today.year:
                partidasDeHoje.append(partida)
                print('Partida %s ocorre hoje!' % partida)
            else:
                print(partida.date)

        pass    # do your thing here