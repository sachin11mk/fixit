from django.db import models

# Create your models here.

class TaskQ(models.Model):
    floor = models.CharField(max_length=80)
    floor_name = models.CharField(max_length=255, null=True)
    room = models.CharField(max_length=80)
    desc = models.TextField()
    status = models.CharField(max_length=80)
    level = models.CharField(max_length=80, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Task-%s"%str(self.id)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) \
                for field in self._meta.fields]



