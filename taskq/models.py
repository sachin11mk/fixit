from django.db import models

# Create your models here.

FLOOR_CHOICES = (
        ('-1', 'Select Floor (...)'),
        ('0', 'Ground'),
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third'),
        ('4', 'Pantry'),
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
)

STATUS_CHOICES = (
        ('P', 'Pending'),
        ('I', 'In Progress'),
        ('C', 'Complete'),
        ('X', 'Not Possible'),
)

PRIORITY_CHOICES = (
        ('B', 'Blocker/Critical'),
        ('H', 'High'),
        ('M', 'Moderate'),
        ('L', 'Low'),
        ('T', 'Suggestion/Task'),
)

class TaskQ(models.Model):
    floor = models.CharField(max_length=255, choices=FLOOR_CHOICES, \
            default='-1')
    room = models.CharField(max_length=255, choices=ROOM_CHOICES,\
            default='-1')
    desc = models.TextField()
    status = models.CharField(max_length=255, default='P',\
            choices=STATUS_CHOICES)
    priority = models.CharField(max_length=255, null=True, default='M',\
            choices=PRIORITY_CHOICES)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Task-%s"%str(self.id)

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
        task = TaskQ.objects.create(floor=floor,
                room=room, desc=desc, priority=priority)
    except Exception, msg:
        raise
    return task





