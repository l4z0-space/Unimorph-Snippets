FROM python:3.7.7-alpine3.11

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --no-cache build-base postgresql-dev python3-dev musl-dev

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

RUN adduser -D -g '' django && chown -R django:django /usr/src/app

USER django

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
