From ubuntu:16.04
MAINTAINER Romel Barrios <lssromel@outlook.com>

EXPOSE 5000

RUN apt-get update && apt-get install -y --no-install-recommends \
	python-dev \ 
	python-pip \
	git \
	vim \
	build-essential
RUN pip install -U pip
RUN pip install django djangorestframework pymongo requests 
RUN pip install setuptools 
RUN pip install import_file pandas
RUN pip install xlrd
RUN pip install tables
WORKDIR /workspace
RUN mkdir -p /data/db
RUN git clone https://github.com/lssromel/send_data_server
RUN git clone https://github.com/lssromel/clientes

WORKDIR /workspace/send_data_server
RUN mkdir /workspace/send_data_server/tmp

