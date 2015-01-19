# system
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain

# custom
from models import TaskQ, save_task, update_task
from forms import TaskForm, TaskAdminForm
from django.contrib.auth.models import User
from subprocess import Popen, PIPE
from django.db.models import Q

def send_postfix_mail(body, sub, to):
    try:
        cmd = "echo '%s' | mail -s '%s' '%s'"%(body, sub, to)
        sp = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        sp.wait()
        if sp.returncode == 0:
            print "New task mail sent to admin user."
        else:
            print sp.stderr.readlines()
            print "Error : Failed to send postfix mail"
    except Exception, msg:
        print msg
        pass


# Create your views here.

@csrf_protect
def add_task(request):
    """
    GET : Render add task form.
    POST : Validate add task form and save the changes to DB.
    """
    template = loader.get_template('add_task.html')
    form = TaskForm()
    if request.user.is_superuser or request.user.is_staff:
        form = TaskAdminForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if request.user.is_superuser or request.user.is_staff:
            form = TaskAdminForm(request.POST)
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

            superusers = User.objects.filter(Q(is_superuser=1) \
                    | Q(is_staff=1))

            email_list = superusers.values_list('email')
            for to in email_list:
                sub = "Fixit: New Task @ Floor-%s"%task.floor
                # commented out automated mails.
                ### send_postfix_mail(task.desc, sub, to[0])
            return HttpResponseRedirect(reverse('task_list'))
        else:
            task = None
            print form.errors
            for err in form.errors.values():
                messages.add_message(request, messages.ERROR, err[0])
    else:
        task = None
    context = RequestContext(request, {'task': task, 'form': form,
            'active': 'addtask'})
    return HttpResponse(template.render(context))


def edit_task(request, task_id):
    template = loader.get_template('edit_task.html')
    task = TaskQ.objects.get(id=task_id)

    task_dict = {
        'floor': task.floor,
        'room': task.room,
        'desc': task.desc,
        'priority': task.priority,
        'status': task.status,
    }
    form = TaskAdminForm(initial=task_dict)
    if request.method == "POST":
        form = TaskAdminForm(request.POST)
        if form.is_valid():
            data = {}
            data['floor'] = form.cleaned_data['floor']
            data['room'] = form.cleaned_data['room']
            data['desc'] = form.cleaned_data['desc']
            data['priority'] = form.cleaned_data['priority']
            data['status'] = form.cleaned_data['status']
            task = update_task(task, form_data=data)
            success_msg = "Task updated successfully."
            messages.add_message(request, messages.SUCCESS, success_msg)
            return HttpResponseRedirect(reverse('task_list'))
        else:
            print form.errors
            for err in form.errors.values():
                messages.add_message(request, messages.ERROR, err[0])
            return HttpResponseRedirect(reverse('edit_task', args=(task.id,)))
            #return HttpResponseRedirect(reverse('task_list'))
    context = RequestContext(request, {'form': form})
    return HttpResponse(template.render(context))



def mark_task_complete(request, task_id):
    task = TaskQ.objects.get(id=task_id)
    task.status = 'C'
    task.save()
    success_msg = "Task marked as complete."
    messages.add_message(request, messages.SUCCESS, success_msg)
    return HttpResponseRedirect(reverse('task_list'))


def mark_task_pending(request, task_id):
    task = TaskQ.objects.get(id=task_id)
    task.status = 'P'
    task.save()
    success_msg = "Task marked as pending."
    messages.add_message(request, messages.SUCCESS, success_msg)
    return HttpResponseRedirect(reverse('task_list'))



def delete_task(request, task_id):
    template = loader.get_template('task_list.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def task_list(request):
    template = loader.get_template('task_list.html')
    p_tasks =  i_tasks = n_tasks = c_tasks = []
    tasks = TaskQ.objects.all()

    tasks = tasks.order_by('priority')

    p_tasks = tasks.filter(status='P')

    #
    # Pending tasks
    #
    t1 = p_tasks.filter(priority='B')
    t2 = p_tasks.filter(priority='H')
    t3 = p_tasks.filter(priority='M')
    t4 = p_tasks.filter(priority='L')
    t5 = p_tasks.filter(priority='T')
    p_tasks = list(chain(t1, t2, t3, t4, t5))
    # Paginate pages with 10 records / page.
    paginator = Paginator(p_tasks, 10)
    page = request.GET.get('page', '1')
    try:
        ptask_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ptask_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999),
        # deliver last page of results.
        ptask_list = paginator.page(paginator.num_pages)

    #
    # Complete tasks
    #
    c_tasks = tasks.filter(status='C')
    # Paginate pages with 10 records / page.
    paginator = Paginator(c_tasks, 5)
    page = request.GET.get('page', '1')
    try:
        ctask_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ctask_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999),
        # deliver last page of results.
        ctask_list = paginator.page(paginator.num_pages)


    #
    # In-progress tasks
    #
    i_tasks = tasks.filter(status='I')
    # Paginate pages with 10 records / page.
    paginator = Paginator(i_tasks, 5)
    page = request.GET.get('page', '1')
    try:
        itask_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        itask_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999),
        # deliver last page of results.
        itask_list = paginator.page(paginator.num_pages)


    #
    # Not possible tasks
    #
    n_tasks = tasks.filter(status='N')
    # Paginate pages with 10 records / page.
    paginator = Paginator(n_tasks, 5)
    page = request.GET.get('page', '1')
    try:
        ntask_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ntask_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999),
        # deliver last page of results.
        ntask_list = paginator.page(paginator.num_pages)

    task_cnt = len(tasks)
    pending_cnt = len(p_tasks)
    complete_cnt = len(c_tasks)
    progress_cnt = len(i_tasks)
    impossible_cnt = len(n_tasks)
    other_cnt = progress_cnt + impossible_cnt

    context = RequestContext(request, {
                'tasks':tasks,\
                'itask_list':itask_list, 'ntask_list':ntask_list, \
                'ctask_list':ctask_list, 'ptask_list': ptask_list, \
                'task_cnt': task_cnt, 'pending_cnt': pending_cnt,\
                'complete_cnt': complete_cnt, 'progress_cnt':progress_cnt,\
                'impossible_cnt':impossible_cnt, 'other_cnt': other_cnt,\
                'active': 'tasklist',})
    return HttpResponse(template.render(context))

