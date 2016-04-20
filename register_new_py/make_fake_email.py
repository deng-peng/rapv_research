from faker import Factory
import random


def make():
    fake = Factory.create()
    years = range(1970, 2015)
    first = fake.first_name()
    last = fake.last_name()
    email = '{0}{1}{2}@{3}'.format(first, last, random.choice(years), fake.domain_name())
    return email, first, last
