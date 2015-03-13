# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badgificator', '0004_auto_20150101_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='condition_function_args',
        ),
        migrations.AddField(
            model_name='badge',
            name='condition_parameters',
            field=models.CharField(max_length=350, null=True, verbose_name="Parameters for Condition's Function", blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='badge',
            name='condition_type',
            field=models.CharField(blank=True, max_length=10, verbose_name='Type of condition for the badge', choices=[('NRM', 'Number of models related to a user'), ('NCD', 'Number of consecutive days of presence'), ('ND', 'Number of days of presence'), ('NHFV', 'Number of hits for a view'), ('FWRM', 'Use a function who tests things about model')]),
            preserve_default=True,
        ),
    ]
