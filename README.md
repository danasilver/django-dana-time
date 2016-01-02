# Django Dana Time [![Build Status](https://travis-ci.org/danasilver/django-dana-time.svg?branch=master)](https://travis-ci.org/danasilver/django-dana-time)

Short, readable datetime filters.

### Install

### Usage

```python
{% load danatime %}

{{ datetime_instance|danatime:"previous year format" }}
```


### Formatting

Examples are shown with `en` translation/formatting and no arguments to the
template tag.

| timedelta               | danatime                     |
|-------------------------|------------------------------|
| 0 seconds               | now                          |
| 1 second                | a second ago                 |
| 2 - 60 seconds          | 2 - 60 seconds ago           |
| 1 minute                | a minute ago                 |
| 2 - 60 minutes          | 2 - 60 minutes ago           |
| 1 hour                  | an hour ago                  |
| 2 - 6 hours             | 2 - 6 hours ago              |
| 6 - 24 hours, same day  | 4:26 p.m.                    |
| 6 - 24 hours, yesterday | 4:26 p.m. yesterday          |
| \> 24 hours, same year  | Aug 10                       |
| previous year           | 8/10/2012                    |


### Internationalization Notes

All values are internationalized and localized by default using
[Django's internationalization and localization support](https://docs.djangoproject.com/en/1.9/topics/i18n/).

#### 6 - 24 hours (same day/yesterday)

Uses `defaultfilters.time`, which defaults to the localized
`settings.TIME_FORMAT`.

Example: In [en](https://github.com/django/django/blob/master/django/conf/locale/en/formats.py),
`TIME_FORMAT = 'P'`.

#### \> 24 hours, same year

Uses `defaultfilters.date` with an argument of `'MONTH_DAY_FORMAT'`, the
localized `settings.MONTH_DAY_FORMAT`.

Example: In [en](https://github.com/django/django/blob/master/django/conf/locale/en/formats.py),
`MONTH_DAY_FORMAT = 'F j'`.

#### previous year

Uses `defaultfilters.date` with an argument of `'n/j/Y'`.

Example: 10 August 2012 is formatted as `8/10/2012`.

Override this by passing an optional argument with a format to the filter tag.

#### previous year format examples:

Pass `None` to use the default, localized `settings.DATE_FORMAT`:

```
{{ mytime|danatime:None }}
```

Pass `SHORT_DATE_FORMAT` to use the localized `settings.SHORT_DATE_FORMAT`:

```
{{ mytime|danatime:"SHORT_DATE_FORMAT" }}
```

Pass a format string like `"F j, Y"` to use a custom format:

```
{{ mytime|danatime:"F j, Y" }}
```

This particular format yields `August 8, 2012`.

See Django's [available format strings](https://docs.djangoproject.com/en/1.9/ref/templates/builtins/#date)
for help.

### Testing

[![Build Status](https://travis-ci.org/danasilver/django-dana-time.svg?branch=master)](https://travis-ci.org/danasilver/django-dana-time)

Tested with all combinations of the latest versions of Python 2.7 and 3.4 with
Django 1.7, 1.8, and 1.9.

After installing Django, run the tests with:

```sh
$ python runtests.py
```

Install tox and run `tox` to test in all environments. This is what the CI does.
