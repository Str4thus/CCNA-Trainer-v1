FROM python:3.7

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "app.wgsi", "-b 0.0.0.0:8000"]