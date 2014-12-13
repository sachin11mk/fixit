from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from models import TaskQ

# Create your views here.

def create_task(request):
    template = loader.get_template('create_task.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def edit_task(request, task_id):
    template = loader.get_template('edit_task.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def list_task(request):
    template = loader.get_template('list_task.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

