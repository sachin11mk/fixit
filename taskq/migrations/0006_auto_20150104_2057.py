# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskq', '0005_auto_20150104_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskq',
            name='floor',
            field=models.CharField(default=b'-1', max_length=255, choices=[(b'-1', b'Select Floor (...)'), (b'0', b'Ground'), (b'1', b'First'), (b'2', b'Second'), (b'3', b'Third'), (b'4', b'Pantry')]),
        ),
        migrations.AlterField(
            model_name='taskq',
            name='room',
            field=models.CharField(default=b'-1', max_length=255, choices=[(b'-1', b'Select Room (...)'), (b'0', b'Conference'), (b'1', b'Room 1'), (b'2', b'Room 2'), (b'3', b'Room 3'), (b'4', b'WC'), (b'5', b'Accounts'), (b'6', b'Server')]),
        ),
    ]
