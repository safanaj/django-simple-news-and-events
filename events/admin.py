from django import forms
from django.contrib import admin
from django.db import models
from events.models import EventsItem, EventsAuthor, EventsCategory
from django.utils.translation import ugettext_lazy as _


class EventsItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ['title', 'pub_date']
    list_filter = ['pub_date']
    search_fields = ['title', 'body']
    date_hierarchy = 'date'
    ordering = ['date']
    fieldsets = (
	('Article info', {
		'fields': ('title', 'body', 'pub_date', 'date', 'tags')
		}),
	('Advanced', {
		'classes': ['collapse'],
		'fields': ('snippet', 'slug',)
		}),
	)

    def queryset(self, request):
	return EventsItem.on_site.all()
	
admin.site.register(EventsItem, EventsItemAdmin)
# admin.site.register(EventsAuthor)
# admin.site.register(EventsCategory)
