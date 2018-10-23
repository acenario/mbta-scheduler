# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils.encoding import smart_unicode

class TrackedModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Created_At', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated_At', auto_now=True) 
    
    class Meta:
        abstract = True