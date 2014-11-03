# -*- coding: utf-8 -*-
from __future__ import unicode_literals


try:
    from unittest import mock
except ImportError:
    import mock

from datetime import timedelta

from django.utils import timezone

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory

from ..models import DataPresence
from ..decorators import bdg_data_presence


class DecoratorDataLoginTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create(username='user1')

    def test_create_data_presence(self):
        request = self.factory.get('/dummyview')
        request.user = self.user
        view = mock.MagicMock(return_value='dummy response')
        self.assertEqual(0, DataPresence.objects.count())
        decorated = bdg_data_presence(view)
        decorated(request)
        view.assert_called_once_with(request)
        self.assertEqual(1, DataPresence.objects.count())
        data = DataPresence.objects.all()[0]
        self.assertEqual(self.user, data.user)
        self.assertEqual(timezone.now().date(), data.last_login)
        self.assertEqual(1, data.consecutive_days)
        self.assertEqual(1, data.number_days)

    def test_multiple_call_data_presence(self):
        request = self.factory.get('/dummyview')
        request.user = self.user
        view = mock.MagicMock(return_value='dummy response')
        decorated = bdg_data_presence(view)
        decorated(request)
        decorated(request)
        data = DataPresence.objects.all()[0]
        self.assertEqual(self.user, data.user)
        self.assertEqual(timezone.now().date(), data.last_login)
        self.assertEqual(1, data.consecutive_days)
        self.assertEqual(1, data.number_days)

    def test_data_presence01(self):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        DataPresence.objects.create(user=self.user,
                                    last_login=yesterday,
                                    consecutive_days=1,
                                    number_days=1)
        request = self.factory.get('/dummyview')
        request.user = self.user
        view = mock.MagicMock(return_value='dummy response')
        decorated = bdg_data_presence(view)
        decorated(request)
        data = DataPresence.objects.all()[0]
        self.assertEqual(self.user, data.user)
        self.assertEqual(timezone.now().date(), data.last_login)
        self.assertEqual(2, data.consecutive_days)
        self.assertEqual(2, data.number_days)

    def test_data_presence02(self):
        today = timezone.now().date()
        old_days = today - timedelta(days=2)
        DataPresence.objects.create(user=self.user,
                                    last_login=old_days,
                                    consecutive_days=1,
                                    number_days=1)
        request = self.factory.get('/dummyview')
        request.user = self.user
        view = mock.MagicMock(return_value='dummy response')
        decorated = bdg_data_presence(view)
        decorated(request)
        data = DataPresence.objects.all()[0]
        self.assertEqual(self.user, data.user)
        self.assertEqual(timezone.now().date(), data.last_login)
        self.assertEqual(1, data.consecutive_days)
        self.assertEqual(2, data.number_days)
