class Partida:
    def __init__(self, number=None, date=None, home_team=None, away_team=None, tv_transmission=None):
        self.number = number
        self.dateTime = date
        self.home_team = home_team
        self.away_team = away_team
        self.tv_transmission = tv_transmission

    def __str__(self):
        return "%s x %s | %s" % (self.home_team, self.away_team, self.dateTime)
