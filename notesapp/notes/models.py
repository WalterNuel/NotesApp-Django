import datetime
from typing import Optional

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Note(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=70)
    note_text = models.TextField(null=True, blank=True,)
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.entry_date >= timezone.now() - datetime.timedelta(days=1)

    def time_written(self):
        ago = self.entry_date
        hours = ago

        # if ago.days > 30:
        #     month = ago.days // 30
        #     hours = f'{month}m'

        # elif ago.days >= 7:
        #     weeks = ago.days // 7
        #     if weeks > 1:
        #         hours = f'{weeks}wk'
        #     else:
        #         hours = f'{weeks}wks'

        # elif ago.days >= 1:
        #     hours = f'{ago.days}d ago'

        # else:
        #     if ago.seconds < 60:
        #         hours = 'Just Now'
        #     elif ago.seconds < (60 * 20):
        #         hours = 'Moments ago'
        #     else:
        #         hours = 'Today'

        return hours
