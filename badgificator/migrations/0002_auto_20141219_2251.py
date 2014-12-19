# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badgificator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='content_type',
            field=models.ForeignKey(verbose_name='Content Type', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
    ]
