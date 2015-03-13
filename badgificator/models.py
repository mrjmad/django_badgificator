# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from .badge_registry import check_function_registry


NUMBER_RELATED_MODEL = "NRM"
NUMBER_CONSECUTIVE_DAYS = "NCD"
NUMBER_DAYS = "ND"
NUMBER_HIT_FOR_VIEW = "NHFV"
FUNCTION_WITH_RELATED_MODEL = "FWRM"
MANUAL_BADGE = "MBADGE"
ALL_OTHER_FUNCTION_CONDITION = "AOFC"
CONDITIONS = (
    (NUMBER_RELATED_MODEL, "Number of models related to a user"),
    (NUMBER_CONSECUTIVE_DAYS, "Number of consecutive days of presence"),
    (NUMBER_DAYS, "Number of days of presence"),
    (NUMBER_HIT_FOR_VIEW, "Number of hits for a view"),
    (FUNCTION_WITH_RELATED_MODEL, "Use a function who tests things about model"),
    (ALL_OTHER_FUNCTION_CONDITION, "Use a function who tests somethings")
)


@python_2_unicode_compatible
class Badge(models.Model):
    name = models.CharField(_("Badge's Name"), max_length=150)
    content_type = models.ForeignKey(ContentType, verbose_name=_("Content Type"), blank=True, null=True)
    condition = models.CharField(_("Badge's Condition displayed"), max_length=350, blank=True, null=True)
    # if assignment is manual, conditions were not check by automatic mechanism of the app
    manual_assignment = models.BooleanField(_("Manuel Assignment ?"), default=False)
    condition_function_name = models.CharField(_("Name of Function for Condition"), max_length=80,
                                               blank=True, null=True)
    # check's function have two mandatory arguments, instance (the instance argument of signal function) and badge
    # this parameters was not passed to the function such as arguments. But the fonction can use it through
    # the badge argument.
    condition_parameters = models.CharField(_("Parameters for Condition's Function"), max_length=350,
                                               blank=True, null=True)

    condition_type = models.CharField(_("Type of condition for the badge"), blank=True,
                                      choices=CONDITIONS, max_length=10)
    name_for_check = models.CharField(_("Name of Field or View for check for simple condition"), blank=True,
                                      max_length=100)
    value_for_valid = models.PositiveIntegerField(_("Value validating the simple condition "), blank=True,
                                                  null=True)

    name_is_visible = models.BooleanField(_("Name is visible ?"), default=True)
    condition_is_visible = models.BooleanField(_("Condition is visible ?"), default=True)
    is_active = models.BooleanField(_("Is active ?"), default=True)

    dict_check_fonction = {
                    NUMBER_RELATED_MODEL: 'check_badge_simple_related_model',
                    NUMBER_CONSECUTIVE_DAYS: 'check_badge_consecutive_days',
                    NUMBER_DAYS: 'check_badge_number_days',
                    NUMBER_HIT_FOR_VIEW: 'check_badge_hit_view',
                    FUNCTION_WITH_RELATED_MODEL: 'check_badge_function_related_model',
    }

    def __str__(self):
        return self.name

    def get_user_related_for_ct(self, instance):
        name_field = self.name_for_check
        return getattr(instance, name_field)

    def get_user_and_related_field_for_ct(self, instance):
        user = self.get_user_related_for_ct(instance)
        related_field_name = instance._meta.get_field(self.name_for_check).related.get_accessor_name()
        related_field = getattr(user, related_field_name)
        return user, related_field

    def check_badge_simple_related_model(self, instance):
        user, related_field = self.get_user_and_related_field_for_ct(instance)
        if related_field.count() > self.value_for_valid:
            return UserBadge.create_badge_for_user(self, user)
        return False

    def check_badge_function_related_model(self, instance):
        user, ok_for_badge = check_function_registry.get_function(self.condition_function_name)(instance, self)
        if ok_for_badge:
            return UserBadge.create_badge_for_user(self, user)
        return False

    def check_badge_consecutive_days(self, data_presence):
        if data_presence.consecutive_days > self.value_for_valid:
            return UserBadge.create_badge_for_user(self, data_presence.user)
        return False

    def check_badge_number_days(self, data_presence):
        if data_presence.number_days > self.value_for_valid:
            return UserBadge.create_badge_for_user(self, data_presence.user)
        return False

    def check_badge_hit_view(self, data_hit_view):
        if data_hit_view.hits > self.value_for_valid:
            return UserBadge.create_badge_for_user(self, data_hit_view.user)
        return False

    def check_badge(self, data):
        return getattr(self, self.dict_check_fonction[self.condition_type])(data)


@python_2_unicode_compatible
class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u"user"))
    badge = models.ForeignKey(Badge, verbose_name=_(u"Name of Badge"))
    date = models.DateTimeField(_(u"Time of badge's acquisition"), null=True)

    def __str__(self):
        return u"%s won %s at %s" % (self.user, self.badge, self.date)

    @staticmethod
    def create_badge_for_user(badge, user):
        user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
        if created:
            user_badge.date = timezone.now()
            user_badge.save()
            return True
        return False


@python_2_unicode_compatible
class DataPresence(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    last_login = models.DateField(_(u'Last day of presence'), blank=True, null=True)
    consecutive_days = models.PositiveIntegerField(_(u'Number of consecutive days of presence'), default=0)
    number_days = models.PositiveIntegerField(_(u'Number of days of presence'), default=0)

    def __str__(self):
        return u" %s : nb consecutive days : %s , total days %s " % (self.user.username, self.consecutive_days,
                                                                     self.number_days)


@python_2_unicode_compatible
class HitViewByUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    date_last_hit = models.DateField(_(u'Day of the last Hit'), blank=True, null=True)
    hits = models.PositiveIntegerField(_(u'Hits for a view'), default=0)
    view_name = models.CharField(_(u'Name of View'), max_length=50)

    def __str__(self):
        return u" %s : view name : %s , total hit %s " % (self.user.username, self.consecutive_days,
                                                                     self.number_days)
