FROM ubuntu:latest

RUN apt-get update -y && apt-get install python3-pip python3.8 -y

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn


ENTRYPOINT [ "gunicorn" ]
CMD ["-b :8080","app:app"]