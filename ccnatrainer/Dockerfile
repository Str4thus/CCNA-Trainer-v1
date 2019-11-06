FROM python:3.7

COPY . /code
WORKDIR /code

RUN pip install -r requirements.txt

CMD ["gunicorn", "ccnatrainer.wgsi", "-b 0.0.0.0:8000"]