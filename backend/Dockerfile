FROM python:3.10

COPY ./requirements.txt /usr/src/star-burger/
RUN pip install --no-cache-dir -r /usr/src/star-burger/requirements.txt

WORKDIR /usr/src/star-burger

COPY . .

RUN python3 manage.py collectstatic --noinput

CMD [ "gunicorn", "-w", "3", "-b", "0.0.0.0:8080", "star_burger.wsgi:application" ]
