from django import template

register = template.Library()

@register.filter(name='addattr')
def addattr(value, arg):
    attrs = {}
    css = arg.split(',')

    for tag in css:
        taglist = tag.split(': ')
        attrs[taglist[0]] = taglist[1]
    return value.as_widget(attrs=attrs)
    
