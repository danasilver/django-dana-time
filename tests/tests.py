"""Tests for danatime templatetag.

These tests mostly mimic the tests for django.contrib.humanize.naturaltime.
See: https://github.com/django/django/blob/master/tests/humanize_tests/tests.py
"""

from __future__ import unicode_literals

import datetime

from danatime.templatetags import danatime
from django.template import Context, Template
from django.test import SimpleTestCase, modify_settings
from django.utils import translation
from django.utils.html import escape
from django.utils.timezone import utc

# Mock out datetime in some tests so they don't fail occasionally when they
# run too slow. Use a fixed datetime for datetime.now(). DST change in
# America/Chicago (the default time zone) happened on March 11th in 2012.

now = datetime.datetime(2012, 3, 9, 22, 30)


class MockDateTime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        if tz is None or tz.utcoffset(now) is None:
            return now
        else:
            # equals now.replace(tzinfo=utc)
            return now.replace(tzinfo=tz) + tz.utcoffset(now)


@modify_settings(INSTALLED_APPS={'append': 'danatime'})
class DanaTimeTests(SimpleTestCase):
    def danatime_tester(self, test_list, result_list, method, normalize_result_func=escape):
        for test_content, result in zip(test_list, result_list):
            t = Template('{%% load danatime %%}{{ test_content|%s }}' % method)
            rendered = t.render(Context(locals())).strip()
            self.assertEqual(rendered, normalize_result_func(result))

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
            now - datetime.timedelta(days=400),
            now.replace(tzinfo=naive()),
            now.replace(tzinfo=utc),
        ]
        result_list = [
            'now',
            'a second ago',
            '30\xa0seconds ago',
            'a minute ago',
            'a minute ago',
            '30\xa0minutes ago',
            'an hour ago',
            'an hour ago',
            '6\xa0hours ago',
            '6\xa0hours ago',
            '3:30 p.m.',
            '10:31 p.m. yesterday',
            'March 7',
            '2/3/2011',
            'now',
            'now',
        ]

        orig_humanize_datetime, danatime.datetime = danatime.datetime, MockDateTime
        try:
            with translation.override('en'):
                self.danatime_tester(test_list, result_list, 'danatime')
        finally:
            danatime.datetime = orig_humanize_datetime

    def test_danatime_none_argument(self):
        test_list = [
            now - datetime.timedelta(days=400)
        ]
        result_list = [
            'Feb. 3, 2011'
        ]
        orig_humanize_datetime, danatime.datetime = danatime.datetime, MockDateTime
        try:
            with translation.override('en'):
                self.danatime_tester(test_list, result_list, 'danatime:None')
        finally:
            danatime.datetime = orig_humanize_datetime

    def test_danatime_shortdateformat_argument(self):
        test_list = [
            now - datetime.timedelta(days=400)
        ]
        result_list = [
            '02/03/2011'
        ]
        orig_humanize_datetime, danatime.datetime = danatime.datetime, MockDateTime
        try:
            with translation.override('en'):
                self.danatime_tester(test_list, result_list,
                                     'danatime:"SHORT_DATE_FORMAT"')
        finally:
            danatime.datetime = orig_humanize_datetime

    def test_danatime_custom_argument(self):
        test_list = [
            now - datetime.timedelta(days=400)
        ]
        result_list = [
            'February 3, 2011'
        ]
        orig_humanize_datetime, danatime.datetime = danatime.datetime, MockDateTime
        try:
            with translation.override('en'):
                self.danatime_tester(test_list, result_list,
                                     'danatime:"F j, Y"')
        finally:
            danatime.datetime = orig_humanize_datetime
