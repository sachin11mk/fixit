# system
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from datetime import datetime, timedelta
from django.views.generic import ListView
import math

# custom
from models import TaskQ, save_task, update_task
from models import RepeatTaskLog
from forms import TaskForm, TaskAdminForm
from django.contrib.auth.models import User
from subprocess import Popen, PIPE
from django.db.models import Q

def send_postfix_mail(body, sub, to):
    try:
        cmd = "echo '%s' | mail -s '%s' '%s'"%(body, sub, to)
        print "TTTT"
        print cmd
        sp = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        sp.wait()
        if sp.returncode == 0:
            print "New task mail sent to admin user."
        else:
            print sp.stderr.readlines()
            print "Error : Failed to send postfix mail"
    except Exception, msg:
        print "++++++++++++"
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
            if request.POST.has_key('repeatable'):
                repeatable = True
                data['repeat_time'] = form.cleaned_data['repeat_time']
            else:
                repeatable = False
                data['repeat_time'] = None
            data['repeatable'] = repeatable

            task = save_task(form_data=data)

            if request.user.is_authenticated():
                task.cuser = request.user.id
                task.save()

            if repeatable:
                RTL = RepeatTaskLog.objects.create(task_id=task.id,\
                        task_repeat_time=task.repeat_time,
                        status=0, comment="Not Done")
                RTL.save()

            if task:
                success_msg = "Task added successfully."
                messages.add_message(request, messages.SUCCESS, success_msg)
            else:
                error_msg = "Failed to save task to database."
                messages.add_message(request, messages.ERROR, error_msg)

            superusers = User.objects.filter(Q(is_superuser=0) \
                    & Q(is_staff=1))

            email_list = superusers.values_list('email')
            print "==========="
            email_list = list(set(email_list))
            print email_list
            print "==========="

            for to in email_list:
                sub = "Fixit: New Task @ Floor-%s"%task.floor
                #
                # comment out test automated mails.
                #
                send_postfix_mail(task.desc, sub, to[0])

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


def task_details(request, task_id):
    """
    show task details page.
    """
    template = loader.get_template('task.html')
    task = TaskQ.objects.get(id=task_id)
    heading = ""
    # Which Floor?
    if task.floor == "0":
        heading += "Ground Floor ==>"
    elif task.floor == "1":
        heading += "First Floor ==>"
    elif task.floor == "2":
        heading += "Second Floor ==>"
    elif task.floor == "3":
        heading += "Third Floor ==>"
    else:
        heading += "Pantry Area ==>"

    # Which Room?
    if task.room == "0":
        heading += "Conference Room "
    elif task.room == "1":
        heading += "Room 1 "
    elif task.room == "2":
        heading += "Room 2 "
    elif task.room == "3":
        heading += "Room 3 "
    elif task.room == "4":
        heading += "WC "
    elif task.room == "5":
        heading += "Accounts "
    elif task.room == "6":
        heading += "Server "
    elif task.room == "7":
        heading += "Lunch Area "
    elif task.room == "8":
        heading += "Common Passage "
    elif task.room == "9":
        heading += "Stairwell "
    elif task.room == "10":
        heading += "Lift "

    if task.status == "P":
        status = "Pending"
    elif task.status == "I":
        status = "In Progress"
    elif task.status == "C":
        status = "Complete"
    else:
        status = "Not Possible"

    if task.priority == "B":
        priority = "Blocker"
    elif task.priority == "H":
        priority = "High"
    elif task.priority == "M":
        priority = "Moderate"
    else:
        priority = "Low"

    context = RequestContext(request, {'task': task, 'heading': heading,\
            'status': status, 'priority': priority})
    return HttpResponse(template.render(context))


def edit_task(request, task_id):
    """
    Edit task.
    """
    template = loader.get_template('edit_task.html')
    task = TaskQ.objects.get(id=task_id)

    task_dict = {
        'floor': task.floor,
        'room': task.room,
        'desc': task.desc,
        'priority': task.priority,
        'status': task.status,
        'repeatable': task.repeatable,
        'repeat_time': task.repeat_time,
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

            if request.POST.has_key('repeatable'):
                repeatable = True
                data['repeat_time'] = form.cleaned_data['repeat_time']
            else:
                repeatable = False
                data['repeat_time'] = None

            data['repeatable'] = repeatable

            orig_status = task.status
            task = update_task(task, form_data=data)
            new_status = task.status

            if request.user.is_authenticated():
                task.euser = request.user.id
                task.save()

            status_change = ""
            if orig_status == "C" and new_status=="P":
                task.status = 'P'
                task.completed = None
                task.save()
                status_change = "CtoP"

            if orig_status == "P" and new_status=="C":
                ctime = datetime.now()
                task.completed = ctime
                task.status = 'C'
                task.save()
                status_change = "PtoC"

            ####################
            if task.repeatable:
                try:
                    RTL = RepeatTaskLog.objects.get(task_id=task.id,\
                        task_repeat_time=task.repeat_time)
                    if RTL:
                        if status_change == "CtoP":
                            RTL.status = 0
                            RTL.comment = "Not Done"
                        if status_change == "PtoC":
                            RTL.status = 1
                            RTL.comment = "Complete"
                        RTL.save()
                except Exception, msg:
                    if status_change == "CtoP":
                        comment = "Not Done"
                        status = 0
                    elif status_change == "PtoC":
                        comment = "Complete"
                        status = 1
                    else:
                        comment = ""
                        status = 0
                    RTL = RepeatTaskLog.objects.create(task_id=task.id,\
                            task_repeat_time=task.repeat_time,
                            status=status, comment=comment)
                    RTL.save()
            ####################

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
    """
    Logic to mark the task as complete.
    """
    task = TaskQ.objects.get(id=task_id)
    ctime = datetime.now()
    task.completed = ctime
    task.status = 'C'
    task.save()

    try:
        if task.repeatable:
            print RepeatTaskLog.objects.all()
            try:
                RTL = RepeatTaskLog.objects.get(task_id=task.id,\
                    task_repeat_time=task.repeat_time)
                if RTL:
                    RTL.status = 1
                    RTL.comment = "Complete"
                    RTL.save()

            #except ObjectDoesNotExist:
            except Exception, msg:
                RTL = RepeatTaskLog.objects.create(task_id=task.id,\
                        task_repeat_time=task.repeat_time,
                        status=1, comment="Complete")
                RTL.save()
                print msg

    except Exception, msg:
        print msg
        raise
    success_msg = "Task marked as complete."
    messages.add_message(request, messages.SUCCESS, success_msg)
    return HttpResponseRedirect(reverse('task_list'))


def mark_task_pending(request, task_id):
    """
    Logic to mark task as incomplete.
    """
    task = TaskQ.objects.get(id=task_id)
    task.status = 'P'
    task.completed = None
    task.save()
    try:
        if task.repeatable:
            try:
                RTL = RepeatTaskLog.objects.get(task_id=task.id,\
                    task_repeat_time=task.repeat_time)
                if RTL:
                    RTL.status = 0
                    RTL.comment = "Not Done"
                    RTL.save()
            except Exception, msg:
            #except ObjectDoesNotExist:
                RTL = RepeatTaskLog.objects.create(task_id=task.id,\
                        task_repeat_time=task.repeat_time,
                        status=1, comment="Not Done")
                RTL.save()

                print msg
    except Exception, msg:
        print msg
    success_msg = "Task marked as pending."
    messages.add_message(request, messages.SUCCESS, success_msg)
    return HttpResponseRedirect(reverse('task_list'))


def delete_task(request, task_id):
    """
    Delete the task.
    Only superuser can delete the task.
    """
    if request.user.is_superuser:
        template = loader.get_template('task_list.html')
        context = RequestContext(request, {})
        task = TaskQ.objects.get(id=task_id)
        task.delete()
        success_msg = "Task deleted successfully."
        messages.add_message(request, messages.SUCCESS, success_msg)
        return HttpResponseRedirect(reverse('task_list'))
    else:
        error_msg = "Only superuser can delete a task."
        messages.add_message(request, messages.error, error_msg)
        return HttpResponseRedirect(reverse('task_list'))
        #return HttpResponse(template.render(context))


def repeat_task_log(request):
    """
    Show repeat task logs in tabular and modular format.
    Only superuser can access this page.
    """
    if request.user.is_superuser:
        template = loader.get_template('repeat_task_log.html')
        context = RequestContext(request, {})
        RTL = RepeatTaskLog.objects.all()
        rtlog_dict = {}
        rtasks = TaskQ.objects.filter(repeatable=1)
        for rt in rtasks:
            rtl_list =RepeatTaskLog.objects.filter(\
                    task_id=rt.id).order_by('task_repeat_time')
            if not rtl_list:
                continue
            pass_cnt = len(rtl_list.filter(status=1))
            total_cnt = len(rtl_list)
            rtlog_dict.update({'%s'%rt.id: {'rtl_list': rtl_list, \
                    'pass_cnt': pass_cnt, 'total_cnt':total_cnt}})

        context = RequestContext(request, {'RTL': RTL, 'rtasks':rtasks,\
            'rtlog_dict': rtlog_dict,
            'active': 'rtlog'})
        return HttpResponse(template.render(context))
    else:
        error_msg = "Access denied."
        messages.add_message(request, messages.error, error_msg)
        return HttpResponseRedirect(reverse('task_list'))
        #return HttpResponse(template.render(context))



def task_list(request):
    """
    List of all pending tasks.
    This is main landing page. Home page.
    """

    '''
    import random
    i = 0
    while i < 50:
        j = 0
        sss = ''
        while j < 6:
            sss += chr(random.randint(97, 122))
            j += 1
        ttask = TaskQ.objects.create(floor=3, room=2, desc=sss, \
                repeatable=False, repeat_time=None, \
                priority='H')
        ttask.save()
        i += 1
    '''

    template = loader.get_template('task_list.html')
    p_tasks =  i_tasks = n_tasks = c_tasks = []
    tasks = TaskQ.objects.all()
    tasks = tasks.order_by('priority')

    p_tasks = tasks.filter(status='P')
    progress = tasks.filter(status='I')
    if not request.user.is_superuser:
        p_tasks = p_tasks.exclude(repeat_time__gt=datetime.now())

    #
    # Pending tasks
    #
    t1 = p_tasks.filter(priority='B')
    t2 = p_tasks.filter(priority='H')
    t3 = p_tasks.filter(priority='M')
    t4 = p_tasks.filter(priority='L')
    t5 = p_tasks.filter(priority='T')
    tp_tasks = list(chain(t1, t2, t3, t4, t5))

    pending = tp_tasks

    p_tasks = list(chain(progress, pending))

    # Paginate pages with 10 records / page.
    paginator = Paginator(p_tasks, 100)
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


    task_cnt = len(tasks)
    pending_cnt = len(p_tasks)
    progress_cnt = len(i_tasks)

    context = RequestContext(request, {
                'tasks':tasks,\
                'p_tasks': p_tasks,\
                'ptask_list': ptask_list, \
                'active': 'tasklist',})
    return HttpResponse(template.render(context))




def completed_list(request):
    """
    List of all completed tasks.
    """
    template = loader.get_template('completed_list.html')
    p_tasks =  i_tasks = n_tasks = c_tasks = []
    tasks = TaskQ.objects.all()

    tasks = tasks.order_by('priority')
    p_tasks = tasks.filter(status='P')
    c_tasks = tasks.filter(status='C')
    i_tasks = tasks.filter(status='I')
    n_tasks = tasks.filter(status='N')

    pending_cnt = len(p_tasks)
    complete_cnt = len(c_tasks)
    progress_cnt = len(i_tasks)
    impossible_cnt = len(n_tasks)
    other_cnt = progress_cnt + impossible_cnt


    #
    # Complete tasks
    #
    c_tasks = tasks.filter(status='C').order_by('-completed')
    # Paginate pages with 10 records / page.
    paginator = Paginator(c_tasks, 50)
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

    task_cnt = len(tasks)
    complete_cnt = len(c_tasks)

    now = datetime.now()
    last_week = now - timedelta(days=7)
    week_tasks =  tasks.filter(created__range=[last_week, now]).exclude(\
            status='I')
    week_cnt = len(week_tasks)
    week_done_cnt = len(week_tasks.filter(status='C'))

    if len(week_tasks.filter(status='C')):
        #avg_closure_time = float(len(week_tasks)) /\
        #    len(week_tasks.filter(status='C'))
        #avg_closure_time = int(math.ceil(avg_closure_time))
        task_done_rate = round(float(len(week_tasks.filter(status='C'))) * 100 / \
                len(week_tasks), 2)
        task_done_rate = "%s %%"%task_done_rate

    else:
        if len(week_tasks.filter(status='P')):
            #avg_closure_time = 0
            task_done_rate = "0%"
        else:
            #avg_closure_time = "NA"
            task_done_rate = "NA"


    context = RequestContext(request, {
                'tasks':tasks,\
                'c_tasks': c_tasks,
                'ctask_list':ctask_list, \
                'task_cnt': task_cnt, 'pending_cnt': pending_cnt,\
                'complete_cnt': complete_cnt, 'progress_cnt':progress_cnt,\
                #'avg_closure_time': avg_closure_time,
                'week_cnt': week_cnt,
                'week_done_cnt': week_done_cnt,
                'task_done_rate': task_done_rate,
                'active': 'ctasklist',})
    return HttpResponse(template.render(context))




def other_list(request):
    """
    List of tasks marked as incomplete.
    """
    template = loader.get_template('other_list.html')
    tasks = TaskQ.objects.all()
    tasks = tasks.order_by('priority')
    #
    # Complete tasks
    #
    other_tasks =  tasks.filter(status__in=['X'])
    other_tasks = other_tasks.order_by('modified')
    context = RequestContext(request, {
                'xtasks':other_tasks, \
                'active': 'otherlist',})
    return HttpResponse(template.render(context))


class OtherList(ListView):
    model = TaskQ
    template_name = "other_list.html"

    def get_queryset(self):
        objects = TaskQ.objects.filter()
        print objects
        return objects



