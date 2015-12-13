In order to run the Dockerfile, first create the database Docker
container by navigating to the "model" directory then running the
command "docker build -t db .". Next run that container by running the
command "docker run -d --name db db". Create an index on mongo by
running the command "sudo docker exec db mongo --eval
"db.messages.createIndex({'location':'2d'})"". Next build the node container by
navigating to the "cloud" directory then running the command "docker
build -t node .". Next run and link that container by running the
command "docker run -p 3000:3000 -t -i --name node1 --link db:db node
/bin/bash". 
To run the node server you are able to navigate to the "/src" directory then run "node server.js".
