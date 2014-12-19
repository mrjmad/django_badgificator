# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import (Badge, UserBadge, NUMBER_RELATED_MODEL, NUMBER_CONSECUTIVE_DAYS,
                     NUMBER_DAYS, NUMBER_HIT_FOR_VIEW)


def post_save_check_all(sender, instance):
    ct = ContentType.objects.get_for_model(sender)
    badges = Badge.objects.filter(content_type=ct,
                                  is_active=True,
                                  manual_assignment=False,
                                  simple_condition=NUMBER_RELATED_MODEL)
    for badge in badges:
        try:
            name_field = badge.name_for_check
            user = getattr(instance, name_field)
            related_field_name = instance._meta.get_field(name_field).related.get_accessor_name()
            count_related = getattr(user, related_field_name).count()
            if count_related > badge.value_for_valid:
                user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    user_badge.date = timezone.now()
                    user_badge.save()
        except Exception as e:
            logging.warn("Error in post_save_check_all with badge %s : %s " % (badge, e))


def post_save_check_data_presence(sender, instance):

    def _check_value_for_badge(value, badge):
        if value > badge.value_for_valid:
            user_badge, created = UserBadge.objects.get_or_create(user=data_presence.user,
                                                                  badge=badge)
            if created:
                user_badge.date = timezone.now()
                user_badge.save()

    data_presence = instance
    badges_consecutive_days = Badge.objects.filter(is_active=True,
                                                   manual_assignment=False,
                                                   simple_condition=NUMBER_CONSECUTIVE_DAYS)

    for badge in badges_consecutive_days:
        try:
            _check_value_for_badge(data_presence.consecutive_days, badge)
        except Exception as e:
            logging.warn("Error in post_save_check_data_presence with badge %s : %s " % (badge, e))

    badges_number_days = Badge.objects.filter(is_active=True,
                                              manual_assignment=False,
                                              simple_condition=NUMBER_DAYS)

    for badge in badges_number_days:
        try:
            _check_value_for_badge(data_presence.number_days, badge)
        except Exception as e:
            logging.warn("Error in post_save_check_data_presence with badge %s : %s " % (badge, e))


def post_save_check_hit_view(sender, instance):
    hit_view_by_user = instance
    badges_consecutive_days = Badge.objects.filter(is_active=True,
                                                   manual_assignment=False,
                                                   name_for_check=hit_view_by_user.view_name,
                                                   simple_condition=NUMBER_HIT_FOR_VIEW)
    for badge in badges_consecutive_days:
        try:
            if hit_view_by_user.hits > badge.value_for_valid:
                user_badge, created = UserBadge.objects.get_or_create(user=hit_view_by_user.user,
                                                                      badge=badge)
                if created:
                    user_badge.date = timezone.now()
                    user_badge.save()
        except Exception as e:
            logging.warn("Error in post_save_check_data_presence with badge %s : %s " % (badge, e))
