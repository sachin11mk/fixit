import os
import sys
import math
from os.path import join, abspath, sep, basename
from datetime import datetime
from django import template
from django.conf import settings
from datetime import datetime, timedelta
from  taskq.models import TaskQ
from django.utils.timesince import timesince


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

register = template.Library()


@register.inclusion_tag("show_admin_user.html", takes_context = True)
def show_admin_user(context):
#   for k,v in context.__dict__.iteritems():
#       print k, v
    try:
        request = context['request']
    except Exception, msg:
        request = None
        pass
    is_admin = False
    username = ""
    try:
        if request.user.is_superuser or request.user.is_staff:
            is_admin = True
            username = request.user.username

    except Exception, msg:
        pass

    return {'is_admin': is_admin, 'username' : username }




@register.simple_tag
def time_required(task_id):
    task = TaskQ.objects.get(id=task_id)
    open_time = task.created
    close_time = task.completed

    try:
        delta = close_time - open_time
    except:
        return "NA"

    deltaMinutes      = delta.seconds // 60
    deltaHours        = delta.seconds // 3600
    deltaMinutes     -= deltaHours * 60
    deltaWeeks        = delta.days    // 7
    deltaSeconds      = delta.seconds - deltaMinutes * 60 - deltaHours * 3600
    deltaDays         = delta.days    - deltaWeeks * 7

    print close_time , open_time
    print delta.seconds, deltaHours, deltaWeeks, deltaMinutes, deltaDays
    time_req = ""
    if deltaWeeks:
        time_req += "%s Weeks "%deltaWeeks
    if deltaDays:
        time_req += "%s Days "%deltaDays
    if deltaHours:
        time_req += "%s Hours "%deltaHours
    if deltaMinutes:
        time_req += "%s Minutes "%deltaMinutes

    if deltaSeconds and not time_req:
        time_req += "1 Minute"
    return time_req

    """
    return "%s"%difference
    if difference >= timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(difference).split(', ')[0]}
    """

