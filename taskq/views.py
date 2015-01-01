from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from models import TaskQ
from forms import TaskForm
# Create your views here.

def create_task(request):
    template = loader.get_template('create_task.html')
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            data = {}
            data['floor_no'] = form.cleaned_data['floor_no']
            data['room'] = form.cleaned_data['room']
            data['desc'] = form.cleaned_data['desc']
            data['level'] = form.cleaned_data['level']
            task = save_task(data=data)
            return HttpResponseRedirect('task/list')
        else:
            task = None
    else:
        task = None
    context = RequestContext(request, {'task': task, 'form': form})
    return HttpResponse(template.render(context))


def edit_task(request, task_id):
    template = loader.get_template('edit_task.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def list_task(request):
    template = loader.get_template('list_task.html')
    tasks = TaskQ.objects.all()
    context = RequestContext(request, {'tasks':tasks})
    return HttpResponse(template.render(context))

