############################################################
# Dockerfile to build ACE(Adaptive Communication Environment) container image
# Based on Ubuntu:14.04
############################################################

# Set the base image to Ubuntu 14.04
FROM ubuntu:14.04
MAINTAINER lauren <lauren.e.buck.1@vanderbilt.edu>

# Installation: Import MongoDB public GPG key and create a MongoDB list file
RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927 
RUN echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list 

# Update repository sources and install MongoDB
RUN sudo apt-get update 
RUN sudo apt-get install -y mongodb-org

# Create the MongoDB data directory
RUN mkdir -p /data/db

# Expose port 27017 from the container to the host
EXPOSE 27017

# Set usr/bin/mongod as the dockerized entry-point application
ENTRYPOINT ["usr/bin/mongod"]

# Download Github repository from git clone https://github.com/thomasameisel/cloud-computing.git
#RUN cd /home; git clone https://github.com/thomasameisel/cloud-computing.git; cd /home/cloud-computing/final-project/cloud; npm install; sudo mkdir /data; sudo mkdir /data/db; sudo rm /var/lib/mongodb/mongod.lock

