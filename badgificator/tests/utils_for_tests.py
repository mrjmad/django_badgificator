# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class DummyModelForTest(models.Model):
    name = models.CharField("Dummy Name", max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

from ..models import (Badge, DataPresence, HitViewByUser, NUMBER_HIT_FOR_VIEW,
                      NUMBER_RELATED_MODEL, NUMBER_DAYS, NUMBER_CONSECUTIVE_DAYS, FUNCTION_WITH_RELATED_MODEL)


def utils_create_six_badges(test_case):
    ct = ContentType.objects.get_for_model(DummyModelForTest)
    test_case.badge1 = Badge.objects.create(name="badge1", name_is_visible=True,
                                            condition_is_visible=True, is_active=True, content_type=ct,
                                            condition_type=NUMBER_RELATED_MODEL, name_for_check='user',
                                            value_for_valid=1)
    test_case.badge2 = Badge.objects.create(name="badge2", name_is_visible=True,
                                            condition_is_visible=True, is_active=True, content_type=ct,
                                            condition_type=NUMBER_RELATED_MODEL, name_for_check='user',
                                            value_for_valid=3)

    test_case.badge3 = Badge.objects.create(name="badge3", name_is_visible=True,
                                            condition_is_visible=True, is_active=True,
                                            condition_type=NUMBER_DAYS,
                                            value_for_valid=3)

    test_case.badge4 = Badge.objects.create(name="badge4", name_is_visible=True,
                                            condition_is_visible=True, is_active=True,
                                            condition_type=NUMBER_CONSECUTIVE_DAYS,
                                            value_for_valid=3)

    test_case.badge5 = Badge.objects.create(name="badge5", name_is_visible=True,
                                            condition_is_visible=True, is_active=True,
                                            condition_type=NUMBER_HIT_FOR_VIEW,
                                            value_for_valid=3, name_for_check="dummy_view")

    test_case.badge6 = Badge.objects.create(name="badge6", name_is_visible=True,
                                            condition_is_visible=True, is_active=True,
                                            condition_type=FUNCTION_WITH_RELATED_MODEL,
                                            condition_function_name='function_badge6',
                                            condition_parameters=None)

    test_case.BADGES_NUMBER = 6


def utils_create_data_presence(test_case):
    test_case.data_presence = DataPresence(user=test_case.user,
                                           last_login=timezone.now(), consecutive_days=1)
    test_case.data_presence.save()


def utils_create_view_hit_by_user(test_case):
    test_case.hit_view = HitViewByUser(user=test_case.user,
                                       hits=0, view_name='view name')
    test_case.hit_view.save()
