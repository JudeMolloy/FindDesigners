from django.db import models


class Designer(models.Model):
    name = models.CharField(max_length=25)
    twitter = models.CharField(max_length=15)
    up_votes = models.IntegerField(default=0)
    available = models.BooleanField(default=False)
    thumbnail_price = models.FloatField()
    channel_art_price = models.FloatField()
    monthly = models.BooleanField(default=False)

    # TIMEZONES =(
    # )
    # timezone = models.CharField(max_length=1, choices=TIMEZONES)
    promoted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def is_available(self):
        if self.available:
            return '{} is available to work.'.format(self.name)
        else:
            return '{} is not available to work.'.format(self.name)

    def is_monthly(self):
        if self.monthly:
            return '{} does monthly deals.'.format(self.name)
        else:
            return '{} does not do monthly deals.'.format(self.name)



