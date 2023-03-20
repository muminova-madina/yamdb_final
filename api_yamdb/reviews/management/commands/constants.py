ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the {} data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

HELP_MESSAGE = 'Импорт данных из csv в модель '
WARNING_MESSAGE = '{} data already loaded...exiting.'
