# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib.contenttypes.models import ContentType

from .models import (Badge, NUMBER_RELATED_MODEL, NUMBER_CONSECUTIVE_DAYS,
                     NUMBER_DAYS, NUMBER_HIT_FOR_VIEW, FUNCTION_WITH_RELATED_MODEL)


def post_save_check_badge_related_model(sender, instance):

    ct = ContentType.objects.get_for_model(sender)
    badges = Badge.objects.filter(content_type=ct,
                                  is_active=True,
                                  manual_assignment=False)
    badges_simple_condition = badges.filter(condition_type=NUMBER_RELATED_MODEL)
    badges_function_condition = badges.filter(condition_type=FUNCTION_WITH_RELATED_MODEL)
    for badge in badges_simple_condition:
        try:
            badge.check_badge_simple_related_model(instance)

        except Exception as e:
            logging.warn("Error in post_save_check_badge_related_model with badge simple condition %s : %s " % (badge, e))

    for badge in badges_function_condition:
        try:
            badge.check_badge_function_related_model(instance)
        except Exception as e:
            logging.warn("Error in post_save_check_badge_related_model with badge function condition %s : %s " % (badge, e))


def post_save_check_data_presence(sender, instance):

    data_presence = instance
    badges_consecutive_days = Badge.objects.filter(is_active=True,
                                                   manual_assignment=False,
                                                   condition_type=NUMBER_CONSECUTIVE_DAYS)

    for badge in badges_consecutive_days:
        try:
            badge.check_badge_consecutive_days(data_presence)
        except Exception as e:
            logging.warn("Error in post_save_check_data_presence with badge %s : %s " % (badge, e))

    badges_number_days = Badge.objects.filter(is_active=True,
                                              manual_assignment=False,
                                              condition_type=NUMBER_DAYS)

    for badge in badges_number_days:
        try:
            badge.check_badge_number_days(data_presence)
        except Exception as e:
            logging.warn("Error in post_save_check_data_presence with badge %s : %s " % (badge, e))


def post_save_check_hit_view(sender, instance):
    hit_view_by_user = instance
    badges_consecutive_days = Badge.objects.filter(is_active=True,
                                                   manual_assignment=False,
                                                   name_for_check=hit_view_by_user.view_name,
                                                   condition_type=NUMBER_HIT_FOR_VIEW)
    for badge in badges_consecutive_days:
        try:
            badge.check_badge_hit_view(hit_view_by_user)
        except Exception as e:
            logging.warn("Error in post_save_check_data_presence with badge %s : %s " % (badge, e))
