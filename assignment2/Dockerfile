############################################################
# Dockerfile to build ACE(Adaptive Communication Environment) container image
# Based on Ubuntu:14.04
############################################################

# Set the base image to Ubuntu 14.04
FROM ubuntu:14.04

# Mention Image Author / Maintainer
MAINTAINER cs292

# Update repository sources list and/or Upgrade OS kernel
RUN apt-get -y update
RUN apt-get -y upgrade

# Install required software packages
RUN apt-get install -y build-essential make git gcc g++

# Download ACE Github repository from git clone https://github.com/Cloud-CS-292-Vanderbilt/ACE.git to  /home/ACE
RUN cd /home;  git clone https://github.com/Cloud-CS-292-Vanderbilt/ACE.git

# compile and install ACE sources
RUN cd /home/ACE; sudo chmod 777 environment.sh;  . ./environment.sh; mwc.pl -type gnuace ACE.mwc; make

# (optional) provide default entrypoint for container
#ENTRYPOINT /bin/bash