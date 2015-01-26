import os
import django
from fixit import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fixit.settings")
django.setup()
from taskq.models import TaskQ, RepeatTaskLog
from datetime import datetime, timedelta

try:
    tasks = TaskQ.objects.all()
    repeat_tasks = tasks.filter(repeatable=True)
    for rt in repeat_tasks:
        RTL = RepeatTaskLog.objects.get(task_id=rt.id, task_repeat_time=rt.repeat_time)
        if rt.status == "P":
            RTL.status = 0
            RTL.comment = "Not Done"
            print "Repeatable task marked as INCOMPLETE."
        else:
            RTL.status = 1
            RTL.comment = "Complete"
        RTL.save()

        otime = rt.repeat_time
        ntime = otime + timedelta(days=1)
        rt.status = 'P'
        rt.completed = None
        rt.repeat_time = ntime
        rt.save()
        print ntime
        print otime
        print repeat_tasks

except Exception, msg:
    print msg
    pass
