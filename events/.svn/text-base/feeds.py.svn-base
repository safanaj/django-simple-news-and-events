from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from events.models import EventsItem

class EventsFeed(Feed):

	def title(self):
		return u"%s" % Site.objects.get_current().name

	def description(self):
		return u'Latest events from %s' % Site.objects.get_current().name

	def link(self):
		# return reverse('events-index')
		return '/events/'

	def items(self):
		return EventsItem.on_site.published(5)
		
	def item_pubdate(self, item):
		from datetime import datetime
		return datetime(item.pub_date.year, item.pub_date.month, item.pub_date.day)

