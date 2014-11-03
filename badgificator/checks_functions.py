# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Badge, UserBadge, NUMBER_RELATED_MODEL


def post_save_check_all(sender, instance):
    ct = ContentType.objects.get_for_model(sender)
    badges = Badge.objects.filter(content_type=ct,
                                  manual_assignment=False,
                                  simple_condition=NUMBER_RELATED_MODEL)
    for badge in badges:
        try:
            name_field = badge.name_field
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
    pass


def post_save_check_hit_view(sender, instance):
    pass
