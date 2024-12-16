from django import template
import datetime

register = template.Library()

@register.filter
def format_date(value):
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.strftime('%d/%m/%Y - %H:%M')
    return value
