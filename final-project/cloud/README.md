In order to run the Dockerfile, first create the database Docker
container by navigating to the "model" directory then running the
command "docker build -t db .". Next run that container by running the
command "docker run -d --name db1 db". Next build the node container by
navigating to the "cloud" directory then running the command "docker
build -t node .". Next run and link that container by running the
command "docker run -p 3000:3000 -t -i --name node1 --link db:db node
/bin/bash".
