FROM macpaw/internship

RUN apt-get update && apt-get install -y zip logrotate

COPY nginx.conf /etc/nginx/conf.d/nginx.conf

COPY uwsgi.ini /app/uwsgi.ini

COPY main.py /app/main.py

WORKDIR /app

RUN cp /var/log/nginx/old.log /app/old.log

EXPOSE 80