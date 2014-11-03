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

from ..models import HitViewByUser
from ..decorators import calculate_hit_by_user


class DecoratorHitViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create(username='user1')

    def test_create_hit_view(self):
        view_name = 'dummyview1'
        request = self.factory.get('/dummyview')
        request.user = self.user
        view = mock.MagicMock(return_value='dummy response')
        self.assertEqual(0, HitViewByUser.objects.count())
        decorator = calculate_hit_by_user(view_name)
        decorated = decorator(view)
        decorated(request)
        view.assert_called_once_with(request)
        self.assertEqual(1, HitViewByUser.objects.count())
        data = HitViewByUser.objects.all()[0]
        self.assertEqual(self.user, data.user)
        self.assertEqual(timezone.now().date(), data.date_last_hit)
        self.assertEqual(1, data.hits)
        self.assertEqual(view_name, data.view_name)

    def test_multiple_call_hit_view(self):
        view_name = 'dummyview1'
        request = self.factory.get('/dummyview')
        request.user = self.user
        view = mock.MagicMock(return_value='dummy response')
        decorator = calculate_hit_by_user(view_name)
        decorated = decorator(view)
        decorated(request)
        decorated(request)
        data = HitViewByUser.objects.all()[0]
        self.assertEqual(self.user, data.user)
        self.assertEqual(timezone.now().date(), data.date_last_hit)
        self.assertEqual(1, data.hits)
        self.assertEqual(view_name, data.view_name)

    def test_hit_view01(self):
        today = timezone.now().date()
        view_name = 'dummyview1'
        yesterday = today - timedelta(days=1)
        HitViewByUser.objects.create(user=self.user,
                                 date_last_hit=yesterday,
                                 hits=1,
                                 view_name=view_name)
        request = self.factory.get('/dummyview')
        request.user = self.user
        view = mock.MagicMock(return_value='dummy response')
        decorator = calculate_hit_by_user(view_name)
        decorated = decorator(view)
        decorated(request)
        data = HitViewByUser.objects.all()[0]

        self.assertEqual(self.user, data.user)
        self.assertEqual(timezone.now().date(), data.date_last_hit)
        self.assertEqual(2, data.hits)
        self.assertEqual(view_name, data.view_name)

    def test_hit_view02(self):
        view_name1 = 'dummyview1'
        view_name2 = 'dummyview2'
        request1 = self.factory.get('/dummyview1')
        request1.user = self.user
        view1 = mock.MagicMock(return_value='dummy response')
        request2 = self.factory.get('/dummyview2')
        request2.user = self.user
        view2 = mock.MagicMock(return_value='dummy response')

        self.assertEqual(0, HitViewByUser.objects.count())

        decorator1 = calculate_hit_by_user(view_name1)
        decorated1 = decorator1(view1)
        decorated1(request1)
        view1.assert_called_once_with(request1)

        decorator2 = calculate_hit_by_user(view_name2)
        decorated2 = decorator2(view2)
        decorated2(request2)
        view2.assert_called_once_with(request2)

        self.assertEqual(2, HitViewByUser.objects.count())

        data1 = HitViewByUser.objects.filter(view_name=view_name1)[0]
        data2 = HitViewByUser.objects.filter(view_name=view_name2)[0]

        self.assertEqual(1, data1.hits)
        self.assertEqual(1, data2.hits)
