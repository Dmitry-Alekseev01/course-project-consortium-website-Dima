
FROM tiangolo/uwsgi-nginx-flask:python3.12

# COPY ./prestart.sh /app/prestart.sh
# RUN chmod +x /app/prestart.sh

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt


COPY ./ ./
