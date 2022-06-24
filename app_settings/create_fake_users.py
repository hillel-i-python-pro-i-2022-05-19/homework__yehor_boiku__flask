from faker import Faker
from random import choice

fake = Faker()


def fake_name_and_email(number):
    list_fake_name_and_email: list = []
    domain_name: list = ['gmail', 'yahoo']
    numbers_in_email = range(100)
    for _ in range(number):
        fake_first_and_last_name: str = fake.first_name()
        name: str = fake_first_and_last_name.lower()
        list_fake_name_and_email += [
            f'{fake_first_and_last_name}: {name}_{choice(numbers_in_email)}@{choice(domain_name)}.com']
    return list_fake_name_and_email
