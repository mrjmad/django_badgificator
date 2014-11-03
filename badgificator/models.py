# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from django.conf import settings
from django.contrib.contenttypes.models import ContentType


NUMBER_RELATED_MODEL = "NRM"
NUMBER_CONSECUTIVE_DAYS = "NCD"
NUMBER_DAYS = "ND"
NUMBER_HIT_FOR_VIEW = "NHFV"

CONDITIONS = (
    (NUMBER_RELATED_MODEL, "Number of models related to a user"),
    (NUMBER_CONSECUTIVE_DAYS, "Number of consecutive days of presence"),
    (NUMBER_DAYS, "Number of days of presence"),
    (NUMBER_HIT_FOR_VIEW, "Number of hits for a view"),
)


@python_2_unicode_compatible
class Badge(models.Model):
    name = models.CharField(_("Badge's Name"), max_length=150)
    content_type = models.ForeignKey(ContentType, verbose_name=_("Content Type"))
    condition = models.CharField(_("Badge's Condition displayed"), max_length=350, blank=True, null=True)
    # if assignment is manual, conditions were not check by automatic mechanism of the app
    manual_assignment = models.BooleanField(_("Manuel Assignment ?"), default=False)
    condition_function_name = models.CharField(_("Name of Function for Condition"), max_length=80,
                                               blank=True, null=True)
    condition_function_args = models.CharField(_("Args of Function for Condition"), max_length=350,
                                               blank=True, null=True)

    simple_condition = models.CharField(_("Simple condition for the badge"), blank=True,
                                     choices=CONDITIONS, max_length=10)
    name_field = models.CharField(_("Name of Field for check for simple condition"), blank=True, max_length=100)
    value_for_valid = models.PositiveIntegerField(_("Value validating the simple condition "), blank=True,
                                                  null=True)

    name_is_visible = models.BooleanField(_("Name is visible ?"), default=True)
    condition_is_visible = models.BooleanField(_("Condition is visible ?"), default=True)
    is_active = models.BooleanField(_("Is active ?"), default=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u"user"))
    badge = models.ForeignKey(Badge, verbose_name=_(u"Name of Badge"))
    date = models.DateTimeField(_(u"Time of badge's acquisition"), null=True)

    def __str__(self):
        return u"%s won %s at %s" % (self.user, self.badge, self.date)


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
