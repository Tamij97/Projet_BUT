FROM python:3.12

WORKDIR /code

RUN chmod 777 /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:7860", "main:app"]