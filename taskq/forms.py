from django import forms
import re
from models import TaskQ
from models import FLOOR_CHOICES, ROOM_CHOICES
from models import STATUS_CHOICES, PRIORITY_CHOICES
from datetime import datetime

ground_val = "Invalid Room. Valid options are WC, Accounts, Common Passage, Stairwell, Lift and Conference."
first_val = "Invalid Room. Valid options are First, Second, Third, WC, Common Passage, Stairwell, Lift and Conference"
second_val = third_val = first_val
pantry_val = "Invalid Room. Valid options are Lunch area and Server."
all_val = "Invalid Room. Valid options are WC, Common Passage, Stairwell, Lift and Conference."

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

    repeatable = forms.BooleanField(label='Repeatable Task',
                required=False,
                widget=forms.CheckboxInput(attrs={'class': 'checkbox',
                'title': 'Check for repeatable tasks',
                'placeholder': 'Is task repeatable?'},
                ))

    repeat_time = forms.CharField(label='Repeat Task at',
                required=False, max_length=255,
                widget=forms.TextInput(attrs={'class': 'form-control', \
                'placeholder': 'Schedule Task @'}),
                error_messages={})
                    #'required': 'Repeat time field can not be empty'} )

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

            # If Floor==Ground then valid Room options are WC, Accounts and
            # Conference
            if self.cleaned_data['floor'] == '0':
                if self.cleaned_data['room'] not in ['0', '4', '5', '8', '9', '10']:
                    raise forms.ValidationError(ground_val)

            # If Floor==First then valid Room options are WC, First, Second,
            # Third and Conference.
            if self.cleaned_data['floor'] == '1':
                if self.cleaned_data['room'] not in ['0', '1', '2', '3', '4', '8', '9', '10']:
                    raise forms.ValidationError(first_val)

            # If Floor==Second then valid Room options are WC, First, Second,
            # Third and Conference.
            if self.cleaned_data['floor'] == '2':
                if self.cleaned_data['room'] not in ['0', '1', '2', '3', '4', '8', '9', '10']:
                    raise forms.ValidationError(second_val)

            # If Floor==Third then valid Room options are WC, First, Second,
            # Third and Conference.
            if self.cleaned_data['floor'] == '3':
                if self.cleaned_data['room'] not in ['0', '1', '2', '3', '4', '8', '9', '10']:
                    raise forms.ValidationError(third_val)

            # If Floor==Pantry then valid Room options are Lunch area and
            # Server room.
            if self.cleaned_data['floor'] == '4':
                if self.cleaned_data['room'] not in ['6', '7']:
                    raise forms.ValidationError(pantry_val)

            # If Floor==All then valid Room options are WC and Conference.
            if self.cleaned_data['floor'] == '5':
                if self.cleaned_data['room'] not in ['0', '4', '8', '9', '10']:
                    raise forms.ValidationError(all_val)

        return self.cleaned_data['room']

    def clean_desc(self):
        if self.cleaned_data['desc']:
            if self.cleaned_data['desc'].strip() == '':
                raise forms.ValidationError('Description field is required.')
        return self.cleaned_data['desc']

    def clean_repeat_time(self):
        if not self.cleaned_data['repeatable']:
            return self.cleaned_data['repeat_time']
        else:
            temp_time = self.cleaned_data['repeat_time']
            if not temp_time:
                raise forms.ValidationError('Repeat time field is required.')
            else:
                if ' ' in temp_time:
                    time_str = temp_time.split()[1]
                else:
                    time_str = "%s:00"%temp_time
                date_str = datetime.now().strftime("%Y-%m-%d ")
                datetime_str = "%s %s"%(date_str, time_str)
                date_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                return date_obj
        #self.cleaned_data['repeat_time']

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

            # If Floor==Ground then valid Room options are WC, Accounts and
            # Conference
            if self.cleaned_data['floor'] == '0':
                if self.cleaned_data['room'] not in ['0', '4', '5', '8', '9', '10']:
                    raise forms.ValidationError(ground_val)

            # If Floor==First then valid Room options are WC, First, Second,
            # Third and Conference.
            if self.cleaned_data['floor'] == '1':
                if self.cleaned_data['room'] not in ['0', '1', '2', '3', '4', '8', '9', '10']:
                    raise forms.ValidationError(first_val)

            # If Floor==Second then valid Room options are WC, First, Second,
            # Third and Conference.
            if self.cleaned_data['floor'] == '2':
                if self.cleaned_data['room'] not in ['0', '1', '2', '3', '4', '8', '9', '10']:
                    raise forms.ValidationError(second_val)

            # If Floor==Third then valid Room options are WC, First, Second,
            # Third and Conference.
            if self.cleaned_data['floor'] == '3':
                if self.cleaned_data['room'] not in ['0', '1', '2', '3', '4', '8', '9', '10']:
                    raise forms.ValidationError(third_val)

            # If Floor==Pantry then valid Room options are Lunch area and
            # Server room.
            if self.cleaned_data['floor'] == '4':
                if self.cleaned_data['room'] not in ['6', '7']:
                    raise forms.ValidationError(pantry_val)

            # If Floor==All then valid Room options are WC and Conference.
            if self.cleaned_data['floor'] == '5':
                if self.cleaned_data['room'] not in ['0', '4', '8', '9', '10']:
                    raise forms.ValidationError(all_val)

        return self.cleaned_data['room']

    def clean_desc(self):
        if self.cleaned_data['desc']:
            if self.cleaned_data['desc'].strip() == '':
                raise forms.ValidationError('Description field is required.')
        return self.cleaned_data['desc']

    def clean_repeat_time(self):

        temp_time = self.cleaned_data['repeat_time']

        if not self.cleaned_data['repeatable']:
            return self.cleaned_data['repeat_time']
        else:
            temp_time = self.cleaned_data['repeat_time']
            if not temp_time:
                raise forms.ValidationError('Repeat time field is required.')
            else:
                if ' ' in temp_time:
                    time_str = temp_time.split()[1]
                else:
                    time_str = "%s:00"%temp_time
                date_str = datetime.now().strftime("%Y-%m-%d ")
                datetime_str = "%s %s"%(date_str, time_str)
                date_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                return date_obj


    def clean(self):
        return self.cleaned_data


