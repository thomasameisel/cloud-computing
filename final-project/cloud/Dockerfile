############################################################
# Dockerfile to build ACE(Adaptive Communication Environment) container image
# Based on Ubuntu:14.04
############################################################

# Set the base image to Ubuntu 14.04
FROM ubuntu:14.04
MAINTAINER tommy 

RUN sudo apt-get update
RUN sudo apt-get install -y nodejs nodejs-legacy npm
COPY package.json /src/package.json
RUN cd /src; npm install

COPY . /src

# Expose port 27017 from the container to the host
EXPOSE 3000 

CMD nodejs /src/server.js
