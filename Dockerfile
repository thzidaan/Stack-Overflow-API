FROM ubuntu:latest

RUN apt-get update -y && apt-get install python3-pip python3.8 -y

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt


ENTRYPOINT [ "gunicorn" ]
CMD ["-b :80","app:app"]