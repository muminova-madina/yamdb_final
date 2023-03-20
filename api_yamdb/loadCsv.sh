python manage.py ImportCsv --path static/data/users.csv --model user  --app users
python manage.py ImportCsv --path static/data/category.csv --model category  --app reviews
python manage.py ImportCsv --path static/data/genre.csv --model genre  --app reviews
python manage.py ImportCsv --path static/data/titles.csv --model title --app reviews  --fk_key category
python manage.py ImportCsv --path static/data/review.csv --model review --app reviews --fk_key title_id,author
python manage.py ImportCsv --path static/data/genre_title.csv --model titlegenre --app reviews --fk_key title_id,genre_id
python manage.py ImportCsv --path static/data/comments.csv --model comment --app reviews --fk_key review_id,author
