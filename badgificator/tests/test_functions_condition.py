# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals)

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from ..models import Badge, FUNCTION_WITH_RELATED_MODEL, UserBadge
from ..badge_registry import check_function_registry
from .utils_for_tests import DummyModelForTest


def dummy_check_function(instance, badge):
    return True


def check_function_more_than_related_model(instance, badge):
    user = instance.user
    if user.dummymodelfortest_set.count() > int(badge.condition_parameters):
        return user, True
    return user, False


class BadgeWithFunctionConditionTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='user1')
        self.FUNCTION_NAME = 'check_function_more_than_related_model'
        self.INVALID_FUNCTION_NAME = 'invalid_check_function'
        check_function_registry.register_function(self.FUNCTION_NAME,
                                                  check_function_more_than_related_model)

        self.badge_more_three = Badge.objects.create(name="badge_more_three", name_is_visible=True,
                                                     content_type=ContentType.objects.get_for_model(DummyModelForTest),
                                                     condition_is_visible=True, is_active=True,
                                                     condition_type=FUNCTION_WITH_RELATED_MODEL,
                                                     condition_function_name='check_function_more_than_related_model',
                                                     condition_parameters="3")

    def test_simple_condition_greater_than(self):
        self.assertEqual(0, UserBadge.objects.all().count())
        dummy1 = DummyModelForTest(name="Dummy 1", user=self.user)
        dummy1.save()
        dummy2 = DummyModelForTest(name="Dummy 2", user=self.user)
        dummy2.save()
        self.assertEqual(2, DummyModelForTest.objects.count())
        self.assertEqual(0, UserBadge.objects.all().count())
        dummy3 = DummyModelForTest(name="Dummy 3", user=self.user)
        dummy3.save()
        dummy4 = DummyModelForTest(name="Dummy 4", user=self.user)
        dummy4.save()
        self.assertEqual(1, UserBadge.objects.all().count())
