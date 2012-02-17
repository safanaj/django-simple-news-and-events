from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from events.models import EventsItemPlugin, EventsItem

class EventsPlugin(CMSPluginBase):
    """ """
    model = EventsItemPlugin
    name = "Events Plugin"
    render_template = "events.html"

    def render (self, context, instance, placeholder):
        events = EventsItem.on_site.published(instance.num_to_show)
        context.update({'events' : events,
                        'instance' : instance,
                        'placeholder' : placeholder})
        return context

plugin_pool.register_plugin(EventsPlugin)
