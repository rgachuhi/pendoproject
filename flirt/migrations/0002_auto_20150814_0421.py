# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150506_0229'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flirt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=600)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChatStream',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20, choices=[('liked', 'liked'), ('matched', 'matched'), ('rejected', 'rejected'), ('chat', 'chat')], default='liked')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('min_age', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(14)], default=20)),
                ('max_age', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(15)], default=50)),
                ('gender_pref', models.CharField(max_length=1, choices=[('f', 'female'), ('m', 'male'), ('b', 'both')], default='f')),
                ('distance', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(10)], default=30)),
                ('hidden', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='source',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='source_user'),
        ),
        migrations.AddField(
            model_name='match',
            name='target',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='target_user'),
        ),
        migrations.AddField(
            model_name='chatstream',
            name='user1',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user1_user'),
        ),
        migrations.AddField(
            model_name='chatstream',
            name='user2',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user2_user'),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='receiver',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='receiver_user'),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='sender',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sender_user'),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='stream',
            field=models.ForeignKey(to='flirt.ChatStream'),
        ),
    ]
