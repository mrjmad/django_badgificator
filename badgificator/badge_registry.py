# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals)


class NotRegistered(Exception):
    pass


class CheckFunctionRegistry(object):
    """Registry for Check's Function of Django-Badgificator"""

    def __init__(self):
        self._function_registry = {}

    def register_function(self, name, function):
        self._function_registry[name] = function

    def get_function(self, name):
        function = self._function_registry.get(name)
        if function is None:
            raise NotRegistered("%s.get_function(): No function registered with name: %s" % (self.__class__, name))
        return function

    def exec_function(self, name, instance, badge):
        function = self._function_registry.get(name)
        if function is None:
            raise NotRegistered("%s.exec_function(): No function registered with name: %s" % (self.__class__, name))
        return function(instance, badge)

check_function_registry = CheckFunctionRegistry()
