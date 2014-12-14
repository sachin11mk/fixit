from django import forms
import re
from models import TaskQ

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskQ
        exclude = ('floor_name', 'created', 'modified', 'status', )

    def clean(self):
        return self.cleaned_data


