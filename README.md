# django-dana-time
*Updated 8-10-13*


### Use

Save `danatime.py` in your Django project.

Load the filter:

    {% load danatime %}

Use the filter:

    {{ mytime|danatime }}


### Formatting

| timedelta              | danatime           |
|------------------------|--------------------|
| 0 seconds              | now                |
| 1 second               | a second ago       |
| 2 - 60 seconds         | 2 - 60 seconds ago |
| 1 minute               | a minute ago       |
| 2 - 60 minutes         | 2 - 60 minutes ago |
| 1 hour, same day       | an hour ago        |
| 2 - 6 hours, same day  | 2 - 6 hours ago    |
| 6 - 24 hours, same day | 4:26 pm (12 hour)  |
| \> 24 hours, same year | Aug 10             |
| previous year          | 8/10/12            |
