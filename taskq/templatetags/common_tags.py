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
    time_req = ""
    if deltaWeeks:
        time_req += "%sw "%deltaWeeks
    if deltaDays:
        time_req += "%sd "%deltaDays
    if deltaHours:
        time_req += "%sh "%deltaHours
    if deltaMinutes:
        time_req += "%sm "%deltaMinutes
    if deltaSeconds and not time_req:
        time_req += "1 minute"
    return time_req


# get timesince value of pending task. (normal task)
@register.simple_tag
def pending_timesince(task_id):
    task = TaskQ.objects.get(id=task_id)
    open_time = task.created
    cur_time = datetime.now()
    try:
        delta = cur_time - open_time
    except:
        return "NA"

    # Do not show negative time.
    if delta.days < 0:
        return "NA"

    deltaMinutes      = delta.seconds // 60
    deltaHours        = delta.seconds // 3600
    deltaMinutes     -= deltaHours * 60
    deltaWeeks        = delta.days    // 7
    deltaSeconds      = delta.seconds - deltaMinutes * 60 - deltaHours * 3600
    deltaDays         = delta.days    - deltaWeeks * 7
    time_req = ""
    if deltaWeeks:
        time_req += "%sw "%deltaWeeks
    if deltaDays:
        time_req += "%sd "%deltaDays
    if deltaHours:
        time_req += "%sh "%deltaHours
    if deltaMinutes:
        time_req += "%sm "%deltaMinutes
    if deltaSeconds and not time_req:
        time_req += "1 minute"
    return time_req


# get timesince value of pending task. (repeatable task)
@register.simple_tag
def repeat_timesince(task_id):
    task = TaskQ.objects.get(id=task_id)
    open_time = task.repeat_time
    #open_time = open_time.replace(hour=0, minute=0, second=0)
    cur_time = datetime.now()
    try:
        delta = cur_time - open_time
    except:
        return "NA"

    # Do not show negative time.
    if delta.days < 0:
        return "NA"

    deltaMinutes      = delta.seconds // 60
    deltaHours        = delta.seconds // 3600
    deltaMinutes     -= deltaHours * 60
    deltaWeeks        = delta.days    // 7
    deltaSeconds      = delta.seconds - deltaMinutes * 60 - deltaHours * 3600
    deltaDays         = delta.days    - deltaWeeks * 7
    time_req = ""
    if deltaWeeks:
        time_req += "%sw "%deltaWeeks
    if deltaDays:
        time_req += "%sd "%deltaDays
    if deltaHours:
        time_req += "%sh "%deltaHours
    if deltaMinutes:
        time_req += "%sm "%deltaMinutes
    if deltaSeconds and not time_req:
        time_req += "1 minute"
    return time_req


@register.simple_tag
def show_task_desc(task_id):
    task = TaskQ.objects.get(id=task_id)
    return task.desc


@register.inclusion_tag("show_pending_cnt.html", takes_context = True)
def show_pending_cnt(context):
    try:
        request = context['request']
    except Exception, msg:
        request = None

    tasks = TaskQ.objects.filter(status='P')
    if request:
        if not request.user.is_superuser:
            tasks = tasks.exclude(repeat_time__gt=datetime.now())
    return { 'pending_cnt': len(tasks) }


@register.simple_tag
def show_complete_cnt():
    tasks = TaskQ.objects.filter(status='C')
    return len(tasks)


@register.simple_tag
def show_other_cnt():
    i_tasks = TaskQ.objects.filter(status='I')
    x_tasks = TaskQ.objects.filter(status='X')
    return len(i_tasks) + len(x_tasks)

