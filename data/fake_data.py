import random
from faker import Faker
from data.models import *

fake = Faker()


def random_int_data(column):
    """Return random number between 2 got numbers"""
    return (
        str(random.randint(column.integer_range_from, column.integer_range_to))
    )


def generate_csv(column_id):
    """Generates random data depends which field was chosen"""

    column = DataColumn.objects.get(id=column_id)

    if column.column_type == ColumnChoicesType.INT:
        return random_int_data(column)
    elif column.column_type == ColumnChoicesType.DATE:
        return fake.date()
    elif column.column_type == ColumnChoicesType.JOB:
        return fake.job()
    elif column.column_type == ColumnChoicesType.EMAIL:
        return fake.email()
    elif column.column_type == ColumnChoicesType.PHONE:
        return fake.phone_number()
    elif column.column_type == ColumnChoicesType.NAME:
        return fake.name()
    else:
        return "Unsupported data type"
