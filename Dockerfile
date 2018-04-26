FROM macpaw/internship

RUN apt-get update && apt-get install -y zip logrotate

# The program to get public ip address is integrated into main.py
# I used flask to make things easier

RUN pip install flask

# To make our page available with internship.macpaw.io address

COPY nginx.conf /etc/nginx/conf.d/nginx.conf

# To fix 500 error

COPY uwsgi.ini /app/uwsgi.ini

# Logrotate

COPY dpkg.conf /etc/logrotate.d/dpkg.conf
COPY supervisord.conf /etc/logrotate.d/supervisor.conf

# Custom server app

COPY main.py /app/main.py

# Not really neccessary

RUN cp /var/log/nginx/old.log /app/old.log

EXPOSE 80