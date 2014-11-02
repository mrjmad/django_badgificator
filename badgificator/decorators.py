# -*- coding: utf-8 -*-

from functools import wraps
from datetime import timedelta
from .models import DataPresence, HitViewByUser
from django.utils import timezone
from django.utils.decorators import available_attrs


def bdg_data_presence(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def _login_wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            data_presence, created = DataPresence.objects.get_or_create(user=request.user)
            today = timezone.now().date()
            yesterday = today - timedelta(days=1)
            if data_presence.last_login != today:
                data_presence.number_days += 1
                if data_presence.last_login == yesterday:
                    data_presence.consecutive_days += 1
                else:
                    data_presence.consecutive_days = 1
                data_presence.last_login = today
                data_presence.save()
        return view_func(request, *args, **kwargs)
    return _login_wrapped_view


def calculate_hit_by_user(view_name):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _hit_wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                data_view, created = HitViewByUser.objects.get_or_create(user=request.user,
                                                                         view_name=view_name)
                today = timezone.now().date()
                if data_view.date_last_hit != today:
                    data_view.hits += 1
                    data_view.date_last_hit = today
                    data_view.save()
            return view_func(request, *args, **kwargs)
        return _hit_wrapped_view
    return decorator
