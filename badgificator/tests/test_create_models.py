# -*- coding: utf-8 -*-

try:
    from unittest import mock
except ImportError:
    import mock


from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Badge, UserBadge, DataPresence, HitViewByUser

from utils_for_tests import (utils_create_view_hit_by_user,
                             utils_create_data_presence, utils_create_two_badges)


class CreateModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='user2')

    def test_create_badge_01(self):
        utils_create_two_badges(self)
        self.assertIsInstance(self.badge2, Badge)
        self.assertEqual(2, Badge.objects.all().count())

    def test_create_badge_02(self):
        utils_create_two_badges(self)

        UserBadge.objects.create(user=self.user, badge=self.badge2, date=timezone.now())
        UserBadge.objects.create(user=self.user, badge=self.badge1, date=timezone.now())
        self.assertEqual(2, self.user.userbadge_set.count())

    def test_create_data_presence(self):
        utils_create_data_presence(self)
        self.assertEqual(1, DataPresence.objects.all().count())

    def test_create_hit_view(self):
        utils_create_view_hit_by_user(self)
        self.assertEqual(1, HitViewByUser.objects.all().count())