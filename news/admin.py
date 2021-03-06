from django import forms
from django.contrib import admin
from django.db import models
from news.models import NewsItem, NewsAuthor, NewsCategory
from django.utils.translation import ugettext_lazy as _


class NewsItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ['title', 'pub_date']
    list_filter = ['pub_date']
    search_fields = ['title', 'body']
    date_hierarchy = 'pub_date'
    ordering = ['-pub_date']
    fieldsets = (
	('Article info', {
		'fields': ('title', 'body', 'pub_date', 'tags',)
		}),
	('Advanced', {
		'classes': ['collapse'],
		'fields': ('snippet', 'slug',)
		}),
	)

    def queryset(self, request):
	return NewsItem.on_site.all()
	
admin.site.register(NewsItem, NewsItemAdmin)
# admin.site.register(NewsAuthor)
# admin.site.register(NewsCategory)
