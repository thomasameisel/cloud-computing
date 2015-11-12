#!/usr/bin/env bash


# installing required packages for compiling mininet and docker
result="$(
)"
printf "%s\n" " $result"



# installing mininet
result="$(
if cd mininet; then 
   printf "mininet and docker already installed. moving on\n";
   cd ..
else 
   printf "updating repository sources and installing required packages\n";
   sudo apt-get -y update
   sudo apt-get -y upgrade
   sudo apt-get -y install git build-essential make
   printf "cloning mininet\n"
   sudo git clone git://github.com/mininet/mininet mininet; 
   printf "installing mininet\n"
   ./mininet/util/install.sh
   printf "installing docker\n"
   sudo apt-get -y install docker.io
   sudo ln -sf /usr/bin/docker.io /usr/local/bin/docker
   sudo echo "DOCKER="/usr/bin/docker.io" " >> docker.io
   sudo mv docker.io /etc/default/docker.io
fi
)"
printf "%s\n" " $result"

# making sure that docker service is running and accessible
sudo service docker.io restart
sleep 30

# create ace-ubuntu docker image from Dockerfile and name it myace:v1. if image is already created then skip.
result="$(
sudo docker images | grep myace  | grep v1 | wc -l
)"
echo $result
if [ $result -eq 0 ]; then
    cd /vagrant;
    sudo docker build -t myace:v1 .;
else
    printf "myace image already created. Moving on ....\n"
fi


# create the mininet topology and deploy our networking application on it
cd /vagrant
sudo python ./networking_application.py

