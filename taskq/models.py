from django.db import models

# Create your models here.

FLOOR_CHOICES = (
        ('-1', 'Select Floor (...)'),
        ('0', 'Ground'),
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third'),
        ('4', 'Pantry'),
        ('5', 'All'),
)

ROOM_CHOICES = (
        ('-1', 'Select Room (...)'),
        ('0', 'Conference'),
        ('1', 'Room 1'),
        ('2', 'Room 2'),
        ('3', 'Room 3'),
        ('4', 'WC'),
        ('5', 'Accounts'),
        ('6', 'Server'),
        ('7', 'Lunch area'),
        ('8', 'Common Passage'),
        ('9', 'Stairwell'),
        ('10', 'Lift'),
)

STATUS_CHOICES = (
        ('P', 'Pending'),
        ('I', 'In Progress'),
        ('C', 'Complete'),
        ('X', 'Not Possible'),
)

PRIORITY_CHOICES = (
        ('1', 'Blocker/Critical'),
        ('2', 'High'),
        ('3', 'Moderate'),
        ('4', 'Low'),
        ('5', 'Suggestion/Task'),
)

class TaskQ(models.Model):
    floor = models.CharField(max_length=255, choices=FLOOR_CHOICES, \
            default='-1')
    room = models.CharField(max_length=255, choices=ROOM_CHOICES,\
            default='-1')
    desc = models.TextField()
    status = models.CharField(max_length=255, default='P',\
            choices=STATUS_CHOICES)
    priority = models.CharField(max_length=255, null=True, default='3',\
            choices=PRIORITY_CHOICES)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)
    completed = models.DateTimeField(null=True, blank=True)
    repeatable = models.BooleanField(default=False)
    repeat_time = models.DateTimeField(null=True, blank=True)
    cuser = models.IntegerField(null=True, blank=True)
    euser = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "Task-%s__%s"%(str(self.id), self.desc[:12])

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) \
                for field in self._meta.fields]

def save_task(**kwargs):
    task = None
    try:
        floor = kwargs['form_data']['floor']
        room = kwargs['form_data']['room']
        desc = kwargs['form_data']['desc']
        priority = kwargs['form_data']['priority']
        repeatable = kwargs['form_data']['repeatable']
        repeat_time = kwargs['form_data']['repeat_time']
        task = TaskQ.objects.create(floor=floor, room=room, desc=desc, \
                repeatable=repeatable, repeat_time=repeat_time, \
                priority=priority)
    except Exception, msg:
        raise
    return task


def update_task(instance=None, **kwargs):
    task = TaskQ.objects.get(id=int(instance.id))
    try:
        orig_repeat_time = task.repeat_time

        floor = kwargs['form_data']['floor']
        room = kwargs['form_data']['room']
        desc = kwargs['form_data']['desc']
        priority = kwargs['form_data']['priority']
        if kwargs['form_data'].has_key('status'):
            status = kwargs['form_data']['status']
            task.status = status
        repeatable = kwargs['form_data']['repeatable']
        repeat_time = kwargs['form_data']['repeat_time']
        task.floor = floor
        task.room = room
        task.desc = desc
        task.repeatable = repeatable
        task.repeat_time = repeat_time
        task.priority = priority
        task.save()

        try:
            if task.repeatable:
                if task.repeat_time != orig_repeat_time:
                    RTL = RepeatTaskLog.objects.create(task_id=task.id,\
                        task_repeat_time=task.repeat_time,
                        status=0, comment="Not Done")
                else:
                    if task.status == "C":
                        RTL = RepeatTaskLog.objects.get(task_id=task.id,\
                            task_repeat_time=task.repeat_time)
                        RTL.status = 1
                        RTL.comment ="Complete"
                        RTL.save()
        except Exception, msg:
            print msg

    except Exception, msg:
        raise
    return task


class RepeatTaskLog(models.Model):
    task_id = models.IntegerField()
    task_repeat_time = models.DateTimeField()
    status = models.BooleanField(default=False)
    comment = models.CharField(max_length=155, null=True)

    def __str__(self):
        return "Repeat_Task-%s"%str(self.task_id)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) \
                for field in self._meta.fields]




