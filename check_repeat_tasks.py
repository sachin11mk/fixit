import os
import django
from fixit import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fixit.settings")
django.setup()
from taskq.models import TaskQ
from datetime import datetime, timedelta

tasks = TaskQ.objects.all()
repeat_tasks = tasks.filter(repeatable=True)
for rt in repeat_tasks:
    if rt.status == "P":
        print "Repeatable task marked as INCOMPLETE."
    otime = rt.repeat_time
    ntime = otime + timedelta(days=1)
    rt.status = 'P'
    rt.completed = None
    rt.repeat_time = ntime
    rt.save()
    print ntime
    print otime
    print repeat_tasks

