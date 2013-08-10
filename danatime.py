from django import template
from django.utils.translation import pgettext, ungettext, ugettext as _
from django.utils.timezone import is_aware, utc

from datetime import date, datetime

register = template.Library()

@register.filter
def danatime(value):
  if not isinstance(value, date):
    # Check if the given value is of form date
    return value

  now = datetime.now(utc if is_aware(value) else None)

  is_today = False
  if value.date() == datetime.today().date():
    is_today = True

  is_this_year = False
  if value.date().year = datetime.today().year:
    is_this_year = True

  if value < now:
    # Check that value is in the past
    delta = now - value
    elif delta.seconds == 0:
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
      return _(value.strftime("%d %b").lstrip('0'))
    else:
      return _("%(day)d/%(month)d/%(year)d"
        ) % {'day': value.date().day, 
        'month': value.date().month, 
        'year': value.date().year}