# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlquote
from django.contrib.auth import get_user_model

class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, first_name, last_name, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                 is_staff=is_staff,
                 is_superuser=is_superuser,
                 last_login=now,
                 first_name=first_name,
                 last_name=last_name,
                 **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, first_name, last_name, **extra_fields):
        if len(first_name) > 1:
            first_name = first_name[0].upper() + first_name[1:]
        if len(last_name) > 1:
            last_name = last_name[0].upper() + last_name[1:]
            
        return self._create_user(username, email, password, False, False, first_name, last_name, **extra_fields)
    
    def create_superuser(self, username, email, password, first_name, last_name):
        user=self._create_user(username, email, password, True, True, first_name, last_name)
        user.is_active=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, verbose_name='Username', unique=True, max_length=255,
                                help_text=_('Required. 255 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
                                validators=[
                                  validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid'))
                                ])
    email = models.EmailField(db_index=True, verbose_name='Email', unique=True, max_length=255)
    first_name = models.CharField(verbose_name='First Name', max_length=254)
    last_name = models.CharField(verbose_name='Last Name', max_length=254)
#     profile_picture = models.URLField(verbose_name='Profile_Picture', default='http://thethinkinggal.files.wordpress.com/2013/04/facebook-profile-image.jpg')
#     private_profile = models.BooleanField(verbose_name='Private', default=False)
#     timezone = models.CharField(verbose_name='Timezone Information', blank=True, null=True, max_length=250)
#     country = models.CharField(verbose_name='Timezone Information', null=True, max_length=5, default="US")
    is_active = models.BooleanField(verbose_name='Active User', default=True, help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    is_staff = models.BooleanField(verbose_name='Staff User', default=False, help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    flagged = models.IntegerField(verbose_name='flagged count', default=0)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    created_at = models.DateTimeField(verbose_name='Created_At', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated_At', auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    objects = UserManager()
    
    def __unicode__(self):
        return smart_text(self.username)
    
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.rstrip()
    
    def get_short_name(self):
        return self.first_name
    
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

