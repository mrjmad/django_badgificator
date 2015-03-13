# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals)

from django.utils import timezone

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import UserBadge, DataPresence, HitViewByUser
from .utils_for_tests import DummyModelForTest, utils_create_six_badges


class BadgeSimpleConditionTest1(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='user1')
        dummy1 = DummyModelForTest(name="Dummy 1", user=self.user)
        dummy1.save()

    def test_dummy_create(self):
        self.assertEqual(1, DummyModelForTest.objects.count())

    def test_simple_condition_greater_than(self):
        utils_create_six_badges(self)
        self.assertEqual(0, UserBadge.objects.all().count())
        dummy2 = DummyModelForTest(name="Dummy 2", user=self.user)
        dummy2.save()
        self.assertEqual(2, DummyModelForTest.objects.count())
        self.assertEqual(1, UserBadge.objects.all().count())
        dummy3 = DummyModelForTest(name="Dummy 3", user=self.user)
        dummy3.save()
        dummy4 = DummyModelForTest(name="Dummy 4", user=self.user)
        dummy4.save()
        self.assertEqual(2, UserBadge.objects.all().count())


class BadgeDataPresenceTest1(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='user1')

    def test_greater_than_number_days(self):
        utils_create_six_badges(self)
        self.assertEqual(0, UserBadge.objects.all().count())
        today = timezone.now().date()
        data_presence = DataPresence(user=self.user, last_login=today,
                                     consecutive_days=1,
                                     number_days=1)
        data_presence.save()
        self.assertEqual(0, UserBadge.objects.all().count())
        data_presence.number_days = 5
        data_presence.save()
        self.assertEqual(1, UserBadge.objects.all().count())
        self.assertEqual(self.badge3, UserBadge.objects.all()[0].badge)

    def test_greater_than_consecutive_days(self):
        utils_create_six_badges(self)
        self.assertEqual(0, UserBadge.objects.all().count())
        today = timezone.now().date()
        data_presence = DataPresence(user=self.user, last_login=today,
                                     consecutive_days=1,
                                     number_days=1)
        data_presence.save()
        self.assertEqual(0, UserBadge.objects.all().count())
        data_presence.consecutive_days = 5
        data_presence.save()
        self.assertEqual(1, UserBadge.objects.all().count())
        self.assertEqual(self.badge4, UserBadge.objects.all()[0].badge)


class BadgeHitViewByUserTest1(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='user1')

    def test_greater_than_hits_number01(self):
        utils_create_six_badges(self)
        self.assertEqual(0, UserBadge.objects.all().count())
        today = timezone.now().date()
        hit_view_by_user = HitViewByUser(user=self.user, date_last_hit=today,
                                         hits=1,
                                         view_name="dummy_view")
        hit_view_by_user.save()
        self.assertEqual(0, UserBadge.objects.all().count())
        hit_view_by_user.hits = 5
        hit_view_by_user.save()
        self.assertEqual(1, UserBadge.objects.all().count())
        self.assertEqual(self.badge5, UserBadge.objects.all()[0].badge)

    def test_greater_than_hits_number02(self):
        utils_create_six_badges(self)
        self.assertEqual(0, UserBadge.objects.all().count())
        today = timezone.now().date()
        hit_view_by_user = HitViewByUser(user=self.user, date_last_hit=today,
                                         hits=1,
                                         view_name="dummy_view")
        hit_view_by_user.save()
        self.assertEqual(0, UserBadge.objects.all().count())
        hit_view_by_user_bis = HitViewByUser(user=self.user, date_last_hit=today,
                                         hits=5,
                                         view_name="dummy_viewbis")
        hit_view_by_user_bis.save()
        self.assertEqual(0, UserBadge.objects.all().count())
        hit_view_by_user.hits = 5
        hit_view_by_user.save()
        self.assertEqual(1, UserBadge.objects.all().count())
        self.assertEqual(self.badge5, UserBadge.objects.all()[0].badge)
