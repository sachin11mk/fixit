from django import forms
import re
from models import TaskQ
from models import FLOOR_CHOICES, ROOM_CHOICES
from models import STATUS_CHOICES, PRIORITY_CHOICES

"""  Radio Fields
class TaskForm(forms.ModelForm):
    floor = forms.ChoiceField(label='Floor',
                required=True,
                widget=forms.RadioSelect(attrs={'class': '',
                'placeholder': 'Select Floor'}), choices=FLOOR_CHOICES )

    room = forms.ChoiceField(label='Room',
                required=True,
                widget=forms.RadioSelect(attrs={'class': '',
                'placeholder': 'Select Room'}), choices=ROOM_CHOICES )

    desc = forms.CharField(label='Description',
                required=True,
                widget=forms.Textarea(attrs={'class': '', 'rows': '5',\
                'cols': '80',
                'placeholder': 'Enter Problem Statement'}), )

    priority = forms.ChoiceField(label='Priority',
                required=True,
                widget=forms.RadioSelect(attrs={'class': '',
                'placeholder': 'Select Task Priority'}), choices=PRIORITY_CHOICES )

    class Meta:
        model = TaskQ
        exclude = ('created', 'modified', 'status',)

    def clean(self):
        return self.cleaned_data



class TaskAdminForm(TaskForm):
    status = forms.ChoiceField(label='Status',
                required=True,
                widget=forms.RadioSelect(attrs={'class': '',
                'placeholder': 'Select Status'}), choices=STATUS_CHOICES )
    class Meta:
        model = TaskQ
        exclude = ('created', 'modified',)

    def clean(self):
        return self.cleaned_data

"""




class TaskForm(forms.ModelForm):

    floor = forms.CharField(label='Floor',
                required=True,
                widget=forms.Select(attrs={'class': 'form-control',
                'placeholder': 'Select Floor'}, choices=FLOOR_CHOICES ))

    room = forms.CharField(label='Room',
                required=True,
                widget=forms.Select(attrs={'class': 'form-control',
                'placeholder': 'Select Room'}, choices=ROOM_CHOICES ))

    desc = forms.CharField(label='Description',
                required=True,
                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5',\
                'cols': '60', 'placeholder': 'Enter Problem Statement'}),
                error_messages={
                    'required': 'Description field can not be empty'} )

    priority = forms.CharField(label='Priority',
                required=True,
                widget=forms.Select(attrs={'class': 'form-control',
                'placeholder': 'Select Task Priority'},
                choices=PRIORITY_CHOICES ))

    class Meta:
        model = TaskQ
        exclude = ('created', 'modified', 'status',)

    def clean_floor(self):
        if self.cleaned_data['floor']:
            if self.cleaned_data['floor'] == '-1':
                raise forms.ValidationError('Floor field is required.')
        return self.cleaned_data['floor']

    def clean_room(self):
        if self.cleaned_data['room']:
            if self.cleaned_data['room'] == '-1':
                raise forms.ValidationError('Room field is required.')
        return self.cleaned_data['room']

    def clean_desc(self):
        if self.cleaned_data['desc']:
            print "AAA", self.cleaned_data['desc'].strip()
            if self.cleaned_data['desc'].strip() == '':
                print "BBB"
                raise forms.ValidationError('Description field is required.')
        return self.cleaned_data['desc']

    def clean(self):
        return self.cleaned_data



class TaskAdminForm(TaskForm):
    status = forms.CharField(label='Status',
                required=True,
                widget=forms.Select(attrs={'class': 'form-control',
                'placeholder': 'Select Status'}, choices=STATUS_CHOICES ))
    class Meta:
        model = TaskQ
        exclude = ('created', 'modified',)

    def clean_floor(self):
        if self.cleaned_data['floor']:
            if self.cleaned_data['floor'] == '-1':
                raise forms.ValidationError('Floor field is required.')
        return self.cleaned_data['floor']

    def clean_room(self):
        if self.cleaned_data['room']:
            if self.cleaned_data['room'] == '-1':
                raise forms.ValidationError('Room field is required.')
        return self.cleaned_data['room']

    def clean_desc(self):
        if self.cleaned_data['desc']:
            if self.cleaned_data['desc'].strip() == '':
                raise forms.ValidationError('Description field is required.')
        return self.cleaned_data['desc']


    def clean(self):
        return self.cleaned_data


