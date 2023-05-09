python3 manage.py collectstatic --noinput
python3 manage.py migrate
gunicorn LiquidApi.wsgi