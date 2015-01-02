# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskq', '0002_taskq_level'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskq',
            old_name='floor',
            new_name='floor_no',
        ),
    ]
