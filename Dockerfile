#FROM tensorflow/tensorflow:2.10.1-jupyter
FROM python:3.9-slim

WORKDIR /nuedgewise

ADD . /nuedgewise

#RUN pip install -r requirements_docker.txt
RUN pip install -r requirements.txt

# Make port 8888 available to the world outside this container
EXPOSE 8888
