# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin

class AdminUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()

class SignUpAdmin(UserAdmin):
    form = AdminUserChangeForm
    
    fieldsets = UserAdmin.fieldsets + (
            (None,{"fields" : ()}),
        )
        
        
admin.site.register(get_user_model(), SignUpAdmin)
