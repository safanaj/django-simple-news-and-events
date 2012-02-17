from django.db import models 
from django.conf import settings
# from django.contrib.sites.models import Site
# from django.contrib.sites.managers import CurrentSiteManager
from tagging.fields import TagField
from datetime import datetime
from django.contrib.comments.models import Comment
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
    
class EventsAuthor(models.Model):
    objects = models.Manager()
    # on_site = CurrentSiteManager()
    
    # site = models.ForeignKey(Site, editable=False, default=settings.SITE_ID)
    name = models.CharField(max_length=500)
    slug = models.SlugField()
    
    def __unicode__(self):
	return self.name
    
    def save(self,*args,**kwargs):
	self.slug = slugify(self.name)
	self.slug = self.slug.lower().replace('-','_')
	super(EventsAuthor,self).save(*args,**kwargs)
	
class EventsCategory(models.Model):
    objects = models.Manager()
    # on_site = CurrentSiteManager()
    
    # site = models.ForeignKey(Site, editable=False, default=settings.SITE_ID)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    
    def __unicode__(self):
	return self.name
    
    def save(self,*args,**kwargs):
	self.slug = slugify(self.name)
	self.slug = self.slug.lower().replace('-','_')
	super(EventsCategory,self).save(*args,**kwargs)


#class EventsManager(CurrentSiteManager):
class EventsManager(models.Manager):
    def published(self, limit=None):
	qs = self.get_query_set().filter(pub_date__isnull=False)
        qs = qs.filter(pub_date__lte=datetime.now()).order_by('date')
	if limit:
	    return qs[:limit]
	return qs

class EventsItem(models.Model):
    
    objects = models.Manager()
    on_site = EventsManager()
    
    title = models.CharField(max_length=100)
    slug = models.SlugField(help_text=u'A slug is used as part of the URL for this article.  It is recommended to use the default value if possible.')
    date = models.DateField(blank=False, null=False, help_text=u'YYYY-MM-DD  --  Required. Date of Event.' )
    pub_date = models.DateField(blank=True, null=True, help_text=u'YYYY-MM-DD  --  Leave blank if you don\'t want the article to appear on the site yet.' )
    snippet = models.TextField(blank=True, help_text=u'Snippets are used as a preview for this article (in sidebars, etc).')
    body = models.TextField(blank=True)
    # site = models.ForeignKey(Site, editable=False, default=settings.SITE_ID)
    tags = TagField(null=True,blank=True, max_length=500, help_text=u'Tags allow you categorize your articles. Separate tags with commas.')
    author = models.ForeignKey(EventsAuthor,null=True,editable=True)
    allow_comments = models.BooleanField(default=True,blank=False,editable=True)
    category = models.ForeignKey(EventsCategory, null=True, editable=True)
    
    def approved_comments(self):
	return Comment.objects.for_model(self).filter(is_public=True)
    
    def unapproved_comments(self):
	return Comment.objects.for_model(self).filter(is_public=False)
    
    def total_comments(self):
	return Comment.objects.for_model(self)
    
    def __unicode__(self):
	return self.title
    
    # @models.permalink
    def get_absolute_url(self):
	return '/events/%s/%s/%s/%s/' % (self.pub_date.strftime('%Y'), self.pub_date.strftime('%b').lower(), self.pub_date.strftime('%d'), self.slug)
        # return ('events-item', (), {
	# 	'year': self.date.strftime('%Y'),
	# 	'month': self.date.strftime('%b').lower(),
	# 	'day': self.date.strftime('%d'),
	# 	'slug': self.slug
	# })
    
    def get_previous(self):
	try:
	    # isnull is to check whether it's published or not - drafts don't have dates, apparently
	    return EventsItem.on_site.filter(date__lt=self.date,date__isnull=False)[0]
	except IndexError, e:
	    # print 'Exception: %s' % e.message
	    return None
	
    def get_next(self):
	try:
	    # isnull is to check whether it's published or not - drafts don't have dates, apparently
	    return EventsItem.on_site.filter(date__gt=self.date,date__isnull=False).order_by('date')[0]
	except IndexError, e:
	    # print 'Exception: %s' % e.message
	    return None
	
    class Meta:
	ordering = ['-date']
	unique_together = (('slug', 'date', 'pub_date'), )


## cms plugs
try:
    from cms.models import CMSPlugin

    class EventsItemPlugin(CMSPlugin):
        """
        """
        num_to_show = models.PositiveIntegerField(_("Number of EventsItem to show"),
                      help_text=_("Limits the number of items that will be displayed"))
    
        def __unicode__(self):
	    return "Latest Events"

except:
    pass
