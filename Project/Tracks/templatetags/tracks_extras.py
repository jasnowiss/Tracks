from django import template
import os
from Tracks.models import *
from customNodes import *

register = template.Library()

@register.filter
def get_model_name(model_object):
    """ADD A DESCRIPTION"""
    return model_object.__class__.__name__


# case sensitive
@register.filter
def model_is_of_type(model_object, arg):
    """ADD A DESCRIPTION"""
    return (model_object.__class__.__name__ == arg)


# case insensitive
@register.filter
def model_is_of_type_i(model_object, arg):
    """ADD A DESCRIPTION"""
    return (model_object.__class__.__name__.lower() == arg.lower())


@register.filter
def get_server_filename(model_object):
    """ADD A DESCRIPTION"""
    if (type(model_object) != Track):
        return "could not get server filename"
    server_filename = '#'
    temp_filepath = model_object.filepath
    if(os.path.exists(temp_filepath)):
        server_filename = os.path.basename(temp_filepath)
    return server_filename


##@register.filter
##def get_formatted_list_of_collab_users(model_object):
##    """ADD A DESCRIPTION"""
##    if(type(model_object) != Collaboration):
##        return "could not get list of collaboration users"
##    str_of_collab_users = ''
##    is_first = True;
##    for user in model_object.users.all():
##        if (is_first):
##            str_of_collab_users += user.firstName + ' ' + user.lastName
##            is_first = False
##        else:
##            str_of_collab_users += ', ' + user.firstName + ' ' + user.lastName
##    return str_of_collab_users


@register.filter
def is_user_authorized(model_object, user_obj):
    """ADD A DESCRIPTION"""
    try:
        bool_to_return = False
        if(type(model_object) == Collaboration):
            model_object.users.get(id=user_obj.id)
            bool_to_return = True
        return bool_to_return
    except:
        return False


@register.tag
def load_head_custom(parser, token):
    return load_head_custom_Node()
