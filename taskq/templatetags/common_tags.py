import os
import sys
import math
from os.path import join, abspath, sep, basename
from datetime import datetime
from django import template
from django.conf import settings
from datetime import datetime, timedelta
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

register = template.Library()


@register.inclusion_tag("show_admin_user.html", takes_context = True)
def show_admin_user(context):
    print "TTTT"
#   for k,v in context.__dict__.iteritems():
#       print k, v
    try:
        print "AAA"
        request = context['request']
        print "BBB"
    except Exception, msg:
        print "CCC"
        request = None
        pass
    print "DDD",request.user
    is_admin = False
    username = ""
    try:
        if request.user.is_superuser or request.user.is_staff:
            is_admin = True
            username = request.user.username

    except Exception, msg:
        pass

    return {'is_admin': is_admin, 'username' : username }


