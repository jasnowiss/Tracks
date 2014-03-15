from django import template

register = template.Library()

@register.filter
def get_model_name(model_object):
    return model_object.__class__.__name__


# case sensitive
@register.filter
def model_is_of_type(model_object, arg):
    return (model_object.__class__.__name__ == arg)


# case insensitive
@register.filter
def model_is_of_type_i(model_object, arg):
    return (model_object.__class__.__name__.lower() == arg.lower())