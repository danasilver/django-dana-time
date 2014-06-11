from __future__ import unicode_literals
from django import template
from django.utils.translation import pgettext, ungettext, ugettext as _
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def danatime(value):
    if not isinstance(value, datetime):
        # Check if the given value is of form datetime
        return value

    now = timezone.now()
    if value > now:
        return value

    delta = now - value
    if delta.days < 1:
        # Fewer than a 24 hours ago (potentially different days)
        if delta.seconds < 10:
            # Fewer than 10 seconds ago
            return _('now')
        elif delta.seconds < 60:
            # 1 or multiple seconds
            # \u00a0 is a nonbreaking space
            return ungettext(
                'a second ago', '%(count)d\u00a0seconds ago', delta.seconds
                ) % {'count': delta.seconds}
        elif delta.seconds // 60 < 60:
            # 1 or multiple minutes
            count = delta.seconds // 60
            return ungettext(
                'a minute ago', '%(count)s\u00a0minutes ago', count
                ) % {'count': count}
        elif delta.seconds // (60 * 60) <= 6:
            # 1 to 6 hours
            count = delta.seconds // (60 * 60)
            return ungettext(
                'an hour ago', '%(count)d\u00a0hours ago', count
                ) % {'count': count}
        elif value.date() == datetime.today().date():
            # 6 to 24 hours ago on the same day
            return value.strftime('%-I:%M%p').lower()
        else:
            # 6 to 24 hours ago yesterday
            return value.strftime('%-I:%M%p yesterday').lower()
    elif value.date().year == datetime.today().year:
        # Same year
        return _(value.strftime("%b %-d"))
    else:
        # Previous year
        return _("%(day)d/%(month)d/%(year)d"
            ) % {'day': value.date().day,
            'month': value.date().month,
            'year': int(str(value.date().year)[2:])}
