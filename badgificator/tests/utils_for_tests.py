# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class DummyModelForTest(models.Model):
    name = models.CharField("Dummy Name", max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

from ..models import (Badge, DataPresence, HitViewByUser,
                      NUMBER_RELATED_MODEL)


def utils_create_two_badges(test_case):
    ct = ContentType.objects.get_for_model(DummyModelForTest)
    test_case.badge1 = Badge.objects.create(name="badge1", name_is_visible=True,
                                            condition_is_visible=True, is_active=True, content_type=ct,
                                            simple_condition=NUMBER_RELATED_MODEL, name_field='user',
                                            value_for_valid=1)
    test_case.badge2 = Badge.objects.create(name="badge2", name_is_visible=True,
                                            condition_is_visible=True, is_active=True, content_type=ct,
                                            simple_condition=NUMBER_RELATED_MODEL, name_field='user',
                                            value_for_valid=3)
    test_case.badge2.save()


def utils_create_data_presence(test_case):
    test_case.data_presence = DataPresence(user=test_case.user,
                                           last_login=timezone.now(), consecutive_days=1)
    test_case.data_presence.save()


def utils_create_view_hit_by_user(test_case):
    test_case.hit_view = HitViewByUser(user=test_case.user,
                                       hits=0, view_name='view name')
    test_case.hit_view.save()
