from events.models import EventsItem, EventsAuthor, EventsCategory
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import get_object_or_404

def by_tag(request,tag):
	qs = EventsItem.on_site.filter(tags__contains=tag,pub_date__isnull=False)
	return object_list(request,qs,template_object_name='item')
	
def by_category(request,category_slug):
	the_category = get_object_or_404(EventsCategory.on_site, slug=category_slug)
	qs = EventsItem.on_site.filter(category=the_category,pub_date__isnull=False)
	return object_list(request,qs,template_object_name='item',extra_context={'category':the_category})
	
def category_list(request,empty_arg):
	return object_list(request,EventsCategory.on_site.all(),template_object_name='item')
	
def by_author(request,author_slug):
	the_author = get_object_or_404(EventsAuthor.on_site, slug=author_slug)
	qs = EventsItem.on_site.filter(author=the_author,pub_date__isnull=False)
	return object_list(request,qs,template_object_name='item')
	
def author_list(request):
	return object_list(request,EventsAuthor.on_site.all(),template_object_name='item')
