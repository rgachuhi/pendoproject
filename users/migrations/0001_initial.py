# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('first_name', models.CharField(null=True, max_length=30, blank=True)),
                ('last_name', models.CharField(null=True, max_length=50, blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('gender', models.CharField(default='u', max_length=1, choices=[('f', 'female'), ('m', 'male'), ('o', 'other'), ('u', 'unknown')])),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('profile_image', models.ImageField(default='/static/images/defaultuserimage.png', upload_to='uploads')),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, related_query_name='user', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', help_text='Specific permissions for this user.', blank=True, related_query_name='user', related_name='user_set')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
