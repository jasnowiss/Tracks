from django import template
from django.template import loader, RequestContext
import os
from Tracks.models import *
from django.shortcuts import render
from Project.settings import MEDIA_URL

class load_head_custom_Node(template.Node):
    def render(self, context):
        return template.loader.render_to_string("Tracks/load_head_custom.html", {"MEDIA_URL" : MEDIA_URL})