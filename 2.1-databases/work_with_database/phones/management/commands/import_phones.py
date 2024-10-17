import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            with open('phones.csv', 'r', encoding='utf-8') as file:
                phones = list(csv.DictReader(file, delimiter=';'))

            for phone_data in phones:

                phone = Phone(
                    name=phone_data['name'],
                    price=int(phone_data['price']),
                    image=phone_data['image'],
                    release_date=phone_data['release_date'],
                    lte_exists=phone_data['lte_exists'] == 'True'
                )

                phone.save()
                print(f"Телефон {phone.name} успешно сохранён.")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))
