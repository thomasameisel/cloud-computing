############################################################
# Dockerfile to build ACE(Adaptive Communication Environment) container image
# Based on Ubuntu:14.04
############################################################

# Create directory and dockerfile
RUN mkdir sinatra; cd sinatra; touch Dockerfile

# Set the base image to Ubuntu 14.04
FROM ubuntu:14.04

# Mention Image Author / Maintainer
MAINTAINER tommy

# Update repository sources list and/or Upgrade OS kernel
RUN apt-get update && apt-get upgrade && apt-get install -y ruby ruby-dev
RUN gem install sinatra

# Install required software packages
RUN apt-get install -y build-essential make git gcc g++ nodejs nodejs-legacy npm mongodb

# Download Github repository from git clone https://github.com/thomasameisel/cloud-computing.git
RUN cd /home; git clone https://github.com/thomasameisel/cloud-computing.git; cd /home/cloud-computing/final-project/cloud; npm install; sudo mkdir /data; sudo mkdir /data/db; sudo rm /var/lib/mongodb/mongod.lock

# (optional) provide default entrypoint for container
#ENTRYPOINT /bin/bash
