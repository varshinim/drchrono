# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    access_token = models.CharField(max_length = 100)
    refresh_token = models.CharField(max_length = 100)
    expires = models.DateTimeField()
