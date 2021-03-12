# Stack-Overflow-API (COMP 4350 Assignment 1)

This is a web application that is used to retrieve the top 10 most voted and recent posts for tagged keywords from the popular website StackOverflow using their API.

### The Web Application is available as a Docker Image in Dockerhub

To retrieve the docker image, run the following in your terminal
```
docker pull zidaan/stack-overflow-api
```
To run the docker image, run the following
```
docker run -d -p 80:80 zidaan/stack-overflow-api
```
The Web Application is now ready to use. Please use the following links to use the application.
```
http://localhost:80 or http://127.0.0.1:80
```
### Run the Application without Docker
Run the following in your terminal

```
git clone https://github.com/thzidaan/Stack-Overflow-API
```
```
cd Stack-Overflow-API
```
```
python3 app.py
```

