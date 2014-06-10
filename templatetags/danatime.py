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
    if delta.days < 1:
      if delta.seconds == 0:
        # Now
        return _('now')
      elif delta.seconds < 60:
        # One or multiple seconds
        # \u00a0 is a nonbreaking space
        return ungettext(
          'a second ago', '%(count)s\u00a0seconds ago', delta.seconds
          ) % {'count': delta.seconds}
      elif delta.seconds // 60 < 60:
        # One or multiple minutes
        count = delta.seconds // 60
        return ungettext(
          'a minute ago', '%(count)s\u00a0minutes ago', count
          ) % {'count': count}
      elif is_today:
        # Same day
        if delta.seconds // (60 * 60) <= 6:
          # Up to 6 hours ago on the same day
          count = delta.seconds // (60 * 60)
          return ungettext(
            'an hour ago', '%(count)s\u00a0hours ago', count
            ) % {'count': count}
        else:
          # Up to 24 hours ago on the same day
          return _("%(hour)s:%(minute)s "
            ) % {'hour': value.time().hour % 12, 
            'minute': value.time().minute} + value.strftime("%p").lower()
      elif is_this_year:
        return _(value.strftime("%b ")) + "%(date)s" % {'date': value.date().day}
      else:
        return _("%(day)s/%(month)s/%(year)s"
          ) % {'day': value.date().day, 
          'month': value.date().month, 
          'year': int(str(value.date().year)[2:])}