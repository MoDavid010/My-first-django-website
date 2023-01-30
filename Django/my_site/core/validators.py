import datetime

from django.core.exceptions import ValidationError


def validate_birth_date(value):
    if value >= (datetime.datetime.now() + datetime.timedelta(days=1)).date(): #or value < (
            #datetime.datetime.now() + datetime.timedelta(weeks=52 * 105)).date():
        raise ValidationError("{} cannot be too young or too old :C".format(value))