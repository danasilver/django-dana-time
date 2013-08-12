from __future__ import unicode_literals
import datetime

from django.conf import settings
settings.configure(DEBUG = True, 
  DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
    'NAME': 'default.db'}})
from templatetags import danatime
from django.template import Template, Context
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.timezone import utc
from django.utils import tzinfo
from django.utils import translation
#from i18n import TransRealMixin

now = datetime.datetime(2013, 8, 11, 16, 30)

class DanatimeTests(TestCase):

  # def tester(self, test_list, result_list, method):
  #   for test_content, result in zip(test_list, result_list):
  #     t = Template('{%% load danatime %%}{{ test_content|%s }}' % method)
  #     rendered = t.render(Context(locals())).strip()
  #     self.assertEqual(rendered, escape(result),
  #                     msg="%s test dailed, produced '%s', should have produced '%s'" % (method, rendered, result))

  def test_danatime(self):
    class naive(datetime.tzinfo):
      def utcoffset(self, dt):
        return None
    test_list = [
        now,
        now - datetime.timedelta(seconds=1),
        now - datetime.timedelta(seconds=30),
        now - datetime.timedelta(minutes=1),
        now - datetime.timedelta(minutes=1, seconds=30),
        now - datetime.timedelta(minutes=30),
        now - datetime.timedelta(hours=1),
        now - datetime.timedelta(hours=1, minutes=30),
        now - datetime.timedelta(hours=6),
        now - datetime.timedelta(hours=6, minutes=30),
        now - datetime.timedelta(hours=7),
        now - datetime.timedelta(hours=23, minutes=59),
        now - datetime.timedelta(hours=48),
        now - datetime.timedelta(days=500),
        now.replace(tzinfo=naive()),
        now.replace(tzinfo=utc),
    ]
    result_list = [
        'now',
        'a second ago',
        '30\xa0seconds ago',
        'a minute ago',
        'a minutes ago',
        '30\xa0minutes ago',
        'an hour ago',
        'an hour ago',
        '6\xa0hours ago',
        '6\xa0hours ago',
        '11:30 am',
        'Aug 10',
        'Aug 9',
        '3/29/12',
        'now',
        'now',
    ]
    result_list_with_tz_support = result_list[:]
    for i in range(len(test_list)):
      self.assertEqual(danatime.danatime(test_list[i]), result_list[i], "%s, %s" % (danatime.danatime(test_list[i]), result_list[i]))
