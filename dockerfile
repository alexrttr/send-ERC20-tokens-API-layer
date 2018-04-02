FROM python:3.4
ADD requirements/base.txt /app/requirements.txt
ADD ./btc_transfer/ /app/
WORKDIR /app/
RUN pip install -r requirements.txt
ENTRYPOINT celery -A btc_transfer  worker --concurrency=4 --loglevel=info
