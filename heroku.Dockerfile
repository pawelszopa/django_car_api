FROM python:3.8

ENV APP_CODE=/app
WORKDIR $APP_CODE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system

COPY . .

RUN python manage.py collectstatic --noinput

# run gunicorn
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
