# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='thumbnail',
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=sorl.thumbnail.fields.ImageField(default='defaultuserimage.png', upload_to='uploads'),
        ),
    ]
