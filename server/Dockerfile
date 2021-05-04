FROM ubuntu:20.04

RUN apt-get update

RUN apt-get -y install python3.8

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]

CMD ["run.py"]