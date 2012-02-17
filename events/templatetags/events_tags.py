from django.conf import settings
from django import template
from events.models import EventsItem, EventsAuthor, EventsCategory

register = template.Library()


@register.tag
def get_events(parser, token):
    """
        {% get_events 5 as events_items %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        limit = None
    elif len(bits) == 4:
        try:
            limit = abs(int(bits[1]))
        except ValueError:
            raise template.TemplateSyntaxError("If provided, second argument to `get_events` must be a positive whole number.")
    if bits[-2].lower() != 'as':
        raise template.TemplateSyntaxError("Missing 'as' from 'get_events' template tag.  Format is {% get_events 5 as events_items %}.")
    return EventsItemNode(bits[-1], limit)

        
class EventsItemNode(template.Node):
    """
    Returns a QuerySet of published EventsItems based on the lookup parameters.
    """
    
    def __init__(self, varname, limit=None, author=None, category_slug=None, filters=None):
        self.varname = varname
        self.limit = limit
        self.filters = filters
        # author is either a literal EventsAuthor slug,
        # or a template variable containing a EventsAuthor slug.
        self.author = author
        self.category = category_slug
        
    def render(self, context):
        # Base QuerySet, which will be filtered further if necessary.
        events = EventsItem.on_site.published()
        
        # Do we filter by author?  If so, first attempt to resolve `author` as
        # a template.Variable.  If that doesn't work, use `author` as a literal
        # EventsAuthor.slug lookup.
        if self.author is not None:
            try:
                author_slug = template.Variable(self.author).resolve(context)
            except template.VariableDoesNotExist:
                author_slug = self.author
            events = events.filter(author__slug=author_slug)
            
        if self.category is not None:
            try:
                category_slug = template.Variable(self.category).resolve(context)
            except template.VariableDoesNotExist:
                category_slug = self.category
            events = events.filter(category__slug=category_slug)
            
        # Apply any additional lookup filters
        if self.filters:
            events = events.filter(**self.filters)
            
        # Apply a limit.
        if self.limit:
            events = events[:self.limit]
            
        context[self.varname] = events
        return u''


def parse_token(token):
    """
    Parses a token into 'slug', 'limit', and 'varname' values.
    Token must follow format {% tag_name <slug> [<limit>] as <varname> %}
    """
    bits = token.split_contents()
    if len(bits) == 5:
        # A limit was passed it -- try to parse / validate it.
        try:
            limit = abs(int(bits[2]))
        except:
            limit = None
    elif len(bits) == 4:
        # No limit was specified.
        limit = None
    else:
        # Syntax is wrong.
        raise template.TemplateSyntaxError("Wrong number of arguments: format is {%% %s <slug> [<limit>] as <varname> %%}" % bits[0])
    if bits[-2].lower() != 'as':
        raise template.TemplateSyntaxError("Missing 'as': format is {%% %s <slug> [<limit>] as <varname> %%}" % bits[0])
    return (bits[1], limit, bits[-1])


@register.tag
def get_posts_by_author(parser,token):
    """
    {% get_posts_by_author <slug> [<limit>] as <varname> %}
        {% get_posts_by_author foo 5 as events_items %}   # 5 articles
        {% get_posts_by_author foo as events_items %} # all articles
    """
    author_slug, limit, varname = parse_token(token)
    return EventsItemNode(varname, limit, author=author_slug)

    
@register.tag
def get_posts_by_category(parser,token):
    """
    {% get_posts_by_category <slug> [<limit>] as <varname> %}
        {% get_posts_by_category foo 5 as events_items %} # 5 articles
        {% get_posts_by_category foo as events_items %}   # all articles
    """
    category_slug, limit, varname = parse_token(token)
    return EventsItemNode(varname, limit, category_slug=category_slug)
    
@register.tag
def get_events_by_category(parser,token):
    """
    This is because I got sick of having to debug issues due to the fact that I typed one or the other.
    """
    return get_posts_by_category(parser,token)

    
@register.tag
def get_posts_by_tag(parser,token):
    """
    {% get_posts_by_tag <tag> [<limit>] as <varname> %}
    """
    tag, limit, varname = parse_token(token)
    return EventsItemNode(varname, limit, filters={'tags__contains':tag})
        
@register.tag
def months_with_events(parser, token):
    """
        {% months_with_events 4 as months %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        limit = None
    elif len(bits) == 4:
        try:
            limit = abs(int(bits[1]))
        except ValueError:
            raise template.TemplateSyntaxError("If provided, second argument to `months_with_events` must be a positive whole number.")
    if bits[-2].lower() != 'as':
        raise template.TemplateSyntaxError("Missing 'as' from 'months_with_events' template tag.  Format is {% months_with_events 5 as months %}.")
    return MonthNode(bits[-1], limit=limit)
    
    
class MonthNode(template.Node):
    
    def __init__(self,varname,limit=None):
        self.varname = varname
        self.limit = limit  # for MonthNode inheritance
    
    def render(self, context):
        try:
            months = EventsItem.on_site.published().dates('date', 'month', order="DESC")
        except:
            months = None
        if self.limit is not None:
            months = list(months)
            months = months[:self.limit]
        context[self.varname] = months
        return ''
        
@register.tag
def get_categories(parser,token):
    """
        {% get_categories as <varname> %}
        {% get_categories 5 as <varname> %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        limit = None
    elif len(bits) == 4:
        try:
            limit = abs(int(bits[1]))
        except ValueError:
            raise template.TemplateSyntaxError("If provided, second argument to `get_categories` must be a positive whole number.")
    if bits[-2].lower() != 'as':
        raise template.TemplateSyntaxError("Missing 'as' from 'get_categories' template tag.  Format is {% get_categories 5 as categories %}.")
    return CategoryNode(bits[-1], limit=limit)
    
class CategoryNode(template.Node):
    
    def __init__(self,varname,limit=None):
        self.varname = varname
        self.limit = limit
    
    def render(self, context):
        categories = EventsCategory.on_site.all()
        if self.limit is not None:
            categories = list(categories)
            categories = categories[:self.limit]
        context[self.varname] = categories
        return ''