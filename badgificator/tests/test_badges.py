# -*- coding: utf-8 -*-

try:
    from unittest import mock
except ImportError:
    import mock

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import UserBadge
from utils_for_tests import DummyModelForTest, utils_create_two_badges


class BadgeSimpleConditionTest1(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='user1')
        dummy1 = DummyModelForTest(name=u"Dummy 1", user=self.user)
        dummy1.save()

    def test_dummy_create(self):
        self.assertEqual(1, DummyModelForTest.objects.count())

    def test_simple_condition_greater_than(self):
        utils_create_two_badges(self)
        self.assertEqual(0, UserBadge.objects.all().count())
        dummy2 = DummyModelForTest(name=u"Dummy 2", user=self.user)
        dummy2.save()
        self.assertEqual(2, DummyModelForTest.objects.count())
        self.assertEqual(1, UserBadge.objects.all().count())
        dummy3 = DummyModelForTest(name=u"Dummy 3", user=self.user)
        dummy3.save()
        dummy4 = DummyModelForTest(name=u"Dummy 4", user=self.user)
        dummy4.save()
        self.assertEqual(2, UserBadge.objects.all().count())
