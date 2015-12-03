############################################################
# Dockerfile to build ACE(Adaptive Communication Environment) container image
# Based on Ubuntu:14.04
############################################################

# Set the base image to Ubuntu 14.04
FROM ubuntu:14.04

# Mention Image Author / Maintainer
MAINTAINER tommy

# Update repository sources list and/or Upgrade OS kernel
RUN apt-get -y update
RUN apt-get -y upgrade

# Install required software packages
RUN apt-get install -y build-essential make git gcc g++ nodejs nodejs-legacy npm

# Download Github repository from git clone https://github.com/thomasameisel/cloud-computing.git
RUN cd /home;  git clone https://github.com/thomasameisel/cloud-computing.git; cd /home/cloud-computing/final-project/cloud; npm install; nodejs start

# (optional) provide default entrypoint for container
#ENTRYPOINT /bin/bash