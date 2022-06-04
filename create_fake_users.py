from faker import Faker
from random import choice
import csv

fake = Faker()


def fake_name_and_email(number: int) -> csv:
    with open('list_with_fake_people.csv', 'w') as file:
        header: list = ['Name', 'E-mail']
        writer = csv.DictWriter(file, fieldnames=header)
        list_fake_name_and_email: list = []
        domain_name: list = ['gmail', 'yahoo']
        numbers_in_email = range(100)
        for _ in range(number):
            fake_first_and_last_name: str = fake.first_name()
            name: str = fake_first_and_last_name.lower()
            list_fake_name_and_email += [{"Name": f'<p>{fake_first_and_last_name}: ',
                                          "E-mail": f'{name}_{choice(numbers_in_email)}@{choice(domain_name)}.com</p>'}]
        writer.writeheader()
        for each_fake_name_and_email in list_fake_name_and_email:
            writer.writerow(each_fake_name_and_email)
    with open('list_with_fake_people.csv', 'r') as file:
        read_csv = csv.DictReader(file)
        list_with_fake_data: list = []
        for row in read_csv:
            list_with_fake_data += row['Name'], row['E-mail']
        file.close()
    return " ".join(list_with_fake_data)
