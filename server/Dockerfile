FROM ubuntu:20.04

MAINTANER "bneto@computacao.cua.ufmt.br"

RUN apt-get update -y && \ apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]

CMD["run.py"]