from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from limits.models import LimitNewsAndEvents

class LimitNewsAndEventsAdmin(admin.ModelAdmin):
    max_num = 1

admin.site.register(LimitNewsAndEvents, LimitNewsAndEventsAdmin)
