# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Team(models.Model):
    userId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    emailId = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=50, default='regular')

    class Meta:
        db_table = 'members'

    def __unicode__(self):
        return "%s" % (self.userId)
