# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='user',
        ),
        migrations.DeleteModel(
            name='Tweet',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
