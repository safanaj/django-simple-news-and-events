from django.conf.urls.defaults import *
from django.conf import settings
from events.models import EventsItem
import events.views as events_views

try:
	PAGINATE = settings.EVENTS_PAGINATE_BY
except:
	PAGINATE = 2

events_dict = {
	'queryset': EventsItem.on_site.published(),
	'template_object_name': 'item',
}

events_date_dict = dict(events_dict, date_field='pub_date', allow_future=True)

urlpatterns = patterns('django.views.generic.date_based',
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', events_date_dict, name="events-item"),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', events_date_dict),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', events_date_dict),
	url(r'^(?P<year>\d{4})/$', 'archive_year',  dict(events_date_dict, make_object_list=True)),
)

urlpatterns += patterns('django.views.generic.list_detail',
	url(r'^$', 'object_list', dict(events_dict, paginate_by=PAGINATE), name="events-index"),
)

urlpatterns += patterns('',
	url(r'^tag/(?P<tag>.+)/$',events_views.by_tag,name='events-by-tag'),
	url(r'^category/(?P<category_slug>.+)/$',events_views.by_category,name='events-by-category'),
	url(r'^categor(y|ies)/$',events_views.category_list,name='events-categories'),
	url(r'^authors/(?P<author_slug>.+)/$',events_views.by_author,name='events-by-author'),
	url(r'^authors/$',events_views.author_list,name='events-authors'),
)

