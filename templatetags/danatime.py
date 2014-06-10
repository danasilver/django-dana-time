from __future__ import unicode_literals
from django import template
from django.utils.translation import pgettext, ungettext, ugettext as _
from django.utils import timezone
from datetime import date, datetime

register = template.Library()

@register.filter
def danatime(value):
    if not isinstance(value, datetime):
        return value

    now = timezone.now()
    # TODO: allow for future dates
    if value > now:
        return value

    delta = now - value
    if delta.days < 1: # if less than a 24 hours ago (could be different days).
        if delta.seconds < 10: # if less than 10 seconds ago
            return _('now')
        elif delta.seconds < 60: # if less than 60 seconds ago
            # One or multiple seconds
            # \u00a0 is a nonbreaking space
            return ungettext(
                'a second ago', '%(count)d\u00a0seconds ago', delta.seconds
                ) % {'count': delta.seconds}
        elif delta.seconds // 60 < 60: # if less than an hour ago
            # One or multiple minutes
            count = delta.seconds // 60
            return ungettext(
                'a minute ago', '%(count)s\u00a0minutes ago', count
                ) % {'count': count}
        elif delta.seconds // (60 * 60) <= 6: # up to 6 hours ago
            count = delta.seconds // (60 * 60)
            return ungettext(
                'an hour ago', '%(count)d\u00a0hours ago', count
                ) % {'count': count}
        elif value.date() == datetime.today().date(): # 6-24 hours ago on the same day
            # delta.seconds // (60 * 60) <= 24:
                # 6-24 hours ago on the same day
            return value.strftime('%-I:%M%p').lower()
            # return _("%(hour)d:%(minute)02d"
                # ) % {'hour': value.time().hour % 12,
                # 'minute': value.time().minute} + value.strftime("%p").lower()
        else: # 6-24 hours ago yesterday
            return value.strftime('%-I:%M%p yesterday').lower()
            # return _("yesterday at %(hour)d:%(minute)02d "
                # ) % {'hour': value.time().hour % 12,
                # 'minute': value.time().minute} + value.strftime("%p").lower()
    elif value.date().year == datetime.today().year:
        return _(value.strftime("%b ")) + "%(date)s" % {'date': value.date().day}
    else:
        return _("%(day)d/%(month)d/%(year)d"
            ) % {'day': value.date().day,
            'month': value.date().month,
            'year': int(str(value.date().year)[2:])}
