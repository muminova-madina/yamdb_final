'''Загрузка в базу данных из csv файлов'
параметры
--path путь к файлу csv: static/data/titles.csv
--model в какую модель загружаем данные: title
--app приложение модели: reviews
не обязательные параметры(если несколько - через запятую)
--fk_key поле модели внешнего ключа в csv файле : category
'''

import sys
from csv import DictReader

import django
from django.core.management.base import BaseCommand

from .constants import (ALREDY_LOADED_ERROR_MESSAGE, HELP_MESSAGE,
                        WARNING_MESSAGE)


class Command(BaseCommand):
    help = HELP_MESSAGE
    fk_keys = []

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Путь к файлу')
        parser.add_argument('--model', type=str, help='Модель для загрузки')
        parser.add_argument('--app', type=str, help='приложение модели')
        parser.add_argument('--fk_key', type=str, help='внешний ключ')

    def make_params(self, options):

        if options['fk_key']:
            self.fk_keys = options['fk_key'].split(',')

    def handle_foreign_keys(self, row):
        params = dict(row)
        for key in self.fk_keys:
            if key[-3:] != '_id':
                value = params.pop(key)
                params[f'{key}_id'] = value

        return params

    def handle(self, *args, **options):
        try:
            entry_cls = django.apps.apps.get_model(
                options['app'], options['model']
            )
        except LookupError:
            self.stdout.write(
                self.style.ERROR(f'Model {options["model"]} not found'),
            )
            sys.exit()
        if entry_cls.objects.exists():
            self.stdout.write(
                self.style.ERROR(WARNING_MESSAGE.format(entry_cls)),
            )
            self.stdout.write(
                self.style.ERROR(
                    ALREDY_LOADED_ERROR_MESSAGE.format(entry_cls)
                ),
            )
            sys.exit()

        file_path = options['path']

        try:
            self.make_params(options)
            params_for_create = []
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                for row in DictReader(csv_file):
                    params_for_create.append(self.handle_foreign_keys(row))

            entry_cls.objects.bulk_create(
                [entry_cls(**parameters) for parameters in params_for_create]
            )

        except Exception as error:
            self.stdout.write(
                self.style.ERROR(
                    f'Error loading model {entry_cls.__name__} {error}'
                ),
            )
            sys.exit()

        self.stdout.write(
            self.style.SUCCESS(
                f'{len(params_for_create)} {entry_cls.__name__}'
                ' Objects Created'
            )
        )
