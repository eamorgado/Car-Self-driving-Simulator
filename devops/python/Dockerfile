FROM ubuntu:16.04
LABEL maintainer="eapmcm@gmail.com"
LABEL version="1.0.0"

RUN apt-get update && apt-get upgrade -y
RUN apt-get install build-essential -y
RUN apt-get install software-properties-common -y
RUN apt-get install curl -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.7

RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get upgrade libstdc++6

FROM carlasim/carla:0.9.10

WORKDIR /python
RUN cp -rf /home/carla/PythonAPI/* /python

CMD "python3.7 /python/util/config.py -x /python/util/opendrive/TownBig.xodr"