from datetime import date, datetime
from django import template

register = template.Library()


@register.filter(name='age')
def get_age(value):
    if not value:
        return None
    d = map(int, value.split("-"))
    dob = datetime(d[0], d[1], d[2])
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
