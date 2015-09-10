# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='thumbnail',
            field=models.ImageField(max_length=500, upload_to='uploads', blank=True, null=True),
        ),
    ]
