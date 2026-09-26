web: gunicorn consultoria.wsgi
web: bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn consultoria.wsgi:application"