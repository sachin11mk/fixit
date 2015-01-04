# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskq', '0004_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskq',
            name='floor_name',
        ),
        migrations.RemoveField(
            model_name='taskq',
            name='floor_no',
        ),
        migrations.RemoveField(
            model_name='taskq',
            name='level',
        ),
        migrations.AddField(
            model_name='taskq',
            name='floor',
            field=models.CharField(default=b'-1', max_length=255, choices=[(b'0', b'Ground'), (b'1', b'First'), (b'2', b'Second'), (b'3', b'Third'), (b'4', b'Pantry'), (b'-1', b'Select Floor')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskq',
            name='priority',
            field=models.CharField(default=b'M', max_length=255, null=True, choices=[(b'B', b'Blocker/Critical'), (b'H', b'High'), (b'M', b'Moderate'), (b'L', b'Low'), (b'T', b'Suggestion/Task')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taskq',
            name='room',
            field=models.CharField(default=b'-1', max_length=255, choices=[(b'0', b'Conference'), (b'1', b'Room 1'), (b'2', b'Room 2'), (b'3', b'Room 3'), (b'4', b'WC'), (b'-1', b'Select Room')]),
        ),
        migrations.AlterField(
            model_name='taskq',
            name='status',
            field=models.CharField(default=b'P', max_length=255, choices=[(b'P', b'Pending'), (b'I', b'In Progress'), (b'C', b'Complete'), (b'X', b'Not Possible')]),
        ),
    ]
