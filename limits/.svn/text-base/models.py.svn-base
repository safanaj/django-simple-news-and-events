from django.db import models 
from django.conf import settings
#from django.contrib.sites.models import Site
#from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import ugettext_lazy as _

class LimitNewsAndEvents(models.Model):
    """
    """
    objects = models.Manager()
    #on_site = CurrentSiteManager()
    #site = models.ForeignKey(Site, editable=False, default=settings.SITE_ID)
    
    limit_news_to_show = models.PositiveIntegerField(_("Number of NewsItem to show"),
                                                     help_text=_("Limits the number of items that will be displayed"),
                                                     default=3)
    
    limit_events_to_show = models.PositiveIntegerField(_("Number of EventsItem to show"),
                                                       help_text=_("Limits the number of items that will be displayed"),
                                                       default=3)
    
    def __unicode__(self):
        """ """
        return "Limits Display: %d News and %d Events" % (self.limit_news_to_show, self.limit_events_to_show)


    def save(self, *args, **kw):
        super(LimitNewsAndEvents,self).save(*args,**kw)


