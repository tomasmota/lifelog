# Run Django dev server
run: 
    python manage.py runserver

# Run via ASGI
uvicorn:
    uvicorn lifelog.asgi:application --reload --port 8000

# Migrations
migrate:
    python manage.py makemigrations
    python manage.py migrate

# Seed default event types
bootstrap:
    python manage.py bootstrap_eventtypes

# Admin user
admin:
    python manage.py createsuperuser

# Quick backup / restore
dump:
    python manage.py dumpdata timeline.EventType timeline.Event --indent 2 > backup.json
load:
    python manage.py loaddata backup.json

shell:
    python manage.py shell
