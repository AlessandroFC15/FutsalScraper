from django.db import models


class Match(models.Model):
    date = models.DateTimeField()
    match_number = models.PositiveSmallIntegerField(primary_key=True)
    home_team = models.CharField(max_length=200)
    away_team = models.CharField(max_length=200)
    tv_transmission = models.BooleanField(default=False)

    @classmethod
    def create(cls, date, match_number, home_team, away_team, tv_transmission):
        match = cls(date=date, match_number=match_number, home_team=home_team, away_team=away_team, tv_transmission=tv_transmission)
        return match

    def __str__(self):
        return "%s x %s | Nr. %d" % (self.home_team, self.away_team, self.match_number)


