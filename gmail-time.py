from django import template
from django.template import defaultfilters
from django.utils.translation import pgettext, ungettext, ugettext as _
from django.utils.timezone import is_aware, utc

from datetime import date, datetime

register = template.Library()

@register.filter
def gmailtime(value):
	if not isinstance(value, date):
		# Check if the given value is of form date
		return value

	now = datetime.now(utc if is_aware(value) else None)

	if value < now:
		# Check that value is in the past
		delta = now - value
		if delta.days != 0:
			# use Django timesince if days > 0
			return pgettext('gmailtime', '%(delta)s') 
				% {'delta': defaultfilters.timesince(value, now)}
		elif delta.seconds == 0:
			return _('now')
		elif delta.seconds < 60:
			return ungettext('a second', '%(count)s\u00a0seconds', delta.seconds)
				% {'count': delta.seconds}
		elif delta.seconds // 60 < 60
			count = delta.seconds // 60
			return ungettext('a minute', '%(count)s\u00a0minutes', count)
				% {'count': count}
		else:
			count = delta.seconds // 60 // 60
			return ungettext('an hour', '%(count)s\u00a0hours ago', count)
				% {'count': count}