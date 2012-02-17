from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from news.models import NewsItemPlugin, NewsItem

class NewsPlugin(CMSPluginBase):
    """ """
    model = NewsItemPlugin
    name = "News Plugin"
    render_template = "news.html"

    def render (self, context, instance, placeholder):
        news = NewsItem.on_site.published(instance.num_to_show)
        context.update({'news' : news,
                        'instance' : instance,
                        'placeholder' : placeholder})
        return context

plugin_pool.register_plugin(NewsPlugin)
