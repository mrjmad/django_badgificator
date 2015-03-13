# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals)

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..badge_registry import check_function_registry, NotRegistered


def dummy_check_function(instance, badge):
    return True


class FunctionRegisryTest1(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='user1')
        self.FUNCTION_NAME = 'dummy_check_function'
        self.INVALID_FUNCTION_NAME = 'invalid_dummy_check_function'

    def test_register_function01(self):
        check_function_registry.register_function(self.FUNCTION_NAME, dummy_check_function)
        check_function_registry.get_function('dummy_check_function')
        with self.assertRaises(NotRegistered):
            check_function_registry.get_function(self.INVALID_FUNCTION_NAME)

    def test_exec_dummy_function(self):
        check_function_registry.register_function(self.FUNCTION_NAME, dummy_check_function)
        self.assertTrue(check_function_registry.exec_function(self.FUNCTION_NAME, None, None))
        with self.assertRaises(NotRegistered):
            self.assertTrue(check_function_registry.exec_function(self.INVALID_FUNCTION_NAME,
                                                                  None, None))
