# system
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

# custom
from models import TaskQ, save_task
from forms import TaskForm, TaskAdminForm

# Create your views here.

@csrf_protect
def add_task(request):
    """
    GET : Render add task form.
    POST : Validate add task form and save the changes to DB.
    """
    template = loader.get_template('add_task.html')
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            data = {}
            data['floor'] = form.cleaned_data['floor']
            data['room'] = form.cleaned_data['room']
            data['desc'] = form.cleaned_data['desc']
            data['priority'] = form.cleaned_data['priority']
            task = save_task(form_data=data)
            if task:
                success_msg = "Task added successfully."
                messages.add_message(request, messages.SUCCESS, success_msg)
            else:
                error_msg = "Failed to save task to database."
                messages.add_message(request, messages.ERROR, error_msg)

            return HttpResponseRedirect(reverse('task_list'))
        else:
            task = None
            print form.errors
            for err in form.errors.values():
                messages.add_message(request, messages.ERROR, err[0])
    else:
        task = None
    context = RequestContext(request, {'task': task, 'form': form})
    return HttpResponse(template.render(context))


def edit_task(request, task_id):
    template = loader.get_template('edit_task.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def delete_task(request, task_id):
    pass
    template = loader.get_template('task_list.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def task_list(request):
    template = loader.get_template('task_list.html')
    tasks = TaskQ.objects.all()
    context = RequestContext(request, {'tasks':tasks})
    return HttpResponse(template.render(context))

