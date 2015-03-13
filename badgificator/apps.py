# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from django.db.models.signals import post_save, post_migrate


def post_save_callback_for_badge(sender, instance, created, raw,
                                 using, update_fields, **kwargs):

    from .models import DataPresence, HitViewByUser, Badge, UserBadge
    from .checks_functions import post_save_check_badge_related_model, post_save_check_data_presence, post_save_check_hit_view
    if sender == Badge or sender == UserBadge:
        return
    if sender == DataPresence:
        post_save_check_data_presence(sender, instance)
    if sender == HitViewByUser:
        post_save_check_hit_view(sender, instance)

    post_save_check_badge_related_model(sender, instance)


def post_migrate_badge_app(sender, **kwargs):
    post_save.connect(post_save_callback_for_badge)


class BadgificatorConfig(AppConfig):
    name = 'badgificator'
    verbose_name = "Django Badgificator"

    def ready(self):
        post_migrate.connect(post_migrate_badge_app, sender=self)
