FROM python:alpine3.9

WORKDIR /app

RUN apk add --update gcc

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

ENV FLASK_ENV=development

ENTRYPOINT ["python"]

CMD ["run.py"]