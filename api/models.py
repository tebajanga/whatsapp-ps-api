from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone

class Inbox(models.Model):
    """ Inbox message """
    category = models.CharField(max_length=255, blank=False,default='')
    mimetype = models.CharField(max_length=20,blank=False,default='')
    sender = models.CharField(max_length=30,blank=False,default='') # +255 766 266 161
    body = models.TextField(default='')
    processed = models.BooleanField(default=False)
    processed_at = models.DateField(blank=True,null=True)
    created_at = models.DateField(default=timezone.now(), blank=False)


class Outbox(models.Model):
    """Outbox message """
    category = models.CharField(max_length=255, blank=False,default='')
    mimetype = models.CharField(max_length=20,blank=False,default='')
    receiver = models.CharField(max_length=30,blank=False,default='') # +255 766 266 161
    body = models.TextField(default='')
    chat_found = models.IntegerField(max_length=1,blank=False,default=0)
    processed = models.BooleanField(default=False)
    processed_at = models.DateField(blank=True,null=True)
    created_at = models.DateField(default=timezone.now(), blank=False)
