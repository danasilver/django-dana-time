from __future__ import unicode_literals

from django import template
from django.utils.translation import ungettext, ugettext as _
from django.utils.timezone import is_aware, utc
from django.template import defaultfilters
from datetime import date, datetime

register = template.Library()


@register.filter
def danatime(value, arg='n/j/Y'):
    if not isinstance(value, date):  # datetime is a subclass of date
        return value

    now = datetime.now(utc if is_aware(value) else None)
    if value > now:
        return value

    delta = now - value
    if delta.days < 1:
        # Fewer than a 24 hours ago (potentially different days)
        if delta.seconds < 1:
            # Fewer than 1 seconds ago
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
        elif value.date() == datetime.now().date():
            # 6 to 24 hours ago on the same day
            return defaultfilters.time(value)
        else:
            # 6 to 24 hours ago yesterday
            return _('%s yesterday') % defaultfilters.time(value)
    elif value.date().year == datetime.now().year:
        # Same year
        return defaultfilters.date(value, 'MONTH_DAY_FORMAT')
    return defaultfilters.date(value, arg)
