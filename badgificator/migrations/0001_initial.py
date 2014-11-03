# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

IS_TEST_DB = settings.DATABASES.get(
    'default', {}).get('NAME', '').startswith('test_')

IS_MEMORY = settings.DATABASES.get(
    'default', {}).get('NAME', '').startswith(':memory:')


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name="Badge's Name")),
                ('condition', models.CharField(max_length=350, null=True, verbose_name="Badge's Condition displayed", blank=True)),
                ('manual_assignment', models.BooleanField(default=False, verbose_name='Manuel Assignment ?')),
                ('condition_function_name', models.CharField(max_length=80, null=True, verbose_name='Name of Function for Condition', blank=True)),
                ('condition_function_args', models.CharField(max_length=350, null=True, verbose_name='Args of Function for Condition', blank=True)),
                ('simple_condition', models.CharField(blank=True, max_length=10, verbose_name='Simple condition for the badge', choices=[('NRM', 'Number of models related to a user'), ('NCD', 'Number of consecutive days of presence'), ('ND', 'Number of days of presence'), ('NHFV', 'Number of hits for a view')])),
                ('name_field', models.CharField(max_length=100, verbose_name='Name of Field for check for simple condition', blank=True)),
                ('value_for_valid', models.PositiveIntegerField(null=True, verbose_name='Value validating the simple condition ', blank=True)),
                ('name_is_visible', models.BooleanField(default=True, verbose_name='Name is visible ?')),
                ('condition_is_visible', models.BooleanField(default=True, verbose_name='Condition is visible ?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active ?')),
                ('content_type', models.ForeignKey(verbose_name='Content Type', to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataPresence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_login', models.DateField(null=True, verbose_name='Last day of presence', blank=True)),
                ('consecutive_days', models.PositiveIntegerField(default=0, verbose_name='Number of consecutive days of presence')),
                ('number_days', models.PositiveIntegerField(default=0, verbose_name='Number of days of presence')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HitViewByUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_last_hit', models.DateField(null=True, verbose_name='Day of the last Hit', blank=True)),
                ('hits', models.PositiveIntegerField(default=0, verbose_name='Hits for a view')),
                ('view_name', models.CharField(max_length=50, verbose_name='Name of View')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserBadge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True, verbose_name="Time of badge's acquisition")),
                ('badge', models.ForeignKey(verbose_name='Name of Badge', to='badgificator.Badge')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

    if IS_TEST_DB or IS_MEMORY:
        operations.extend([
            migrations.CreateModel(
                name='DummyModelForTest',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('name', models.CharField(max_length=150, verbose_name="Badge's Name")),
                    ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
                ],
                options={
                },
                bases=(models.Model,),
            ), ])
