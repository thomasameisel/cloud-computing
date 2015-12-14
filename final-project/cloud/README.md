In order to run the Docker containers, first create the database Docker
image by navigating to the "model" directory then running the
command "docker build -t db .". Next run that container by running the
command "docker run -d --name db db". Create an index on mongo by
running the command "sudo docker exec db mongo --eval
"db.messages.createIndex({'location':'2d'})"". Next build the node container by
navigating to the "cloud" directory then running the command "docker
build -t node .". Next run and link that container by running the
command "docker run -p 3000:3000 -t -i --name node1 --link db:db node
/bin/bash". 
To run the node server you are able to navigate to the "/src" directory then run "node server.js".

The total list of commands to run the server on Docker containers:
<br>
<code>cd final-project/cloud/model</code>
<br>
<code># create the database image</code>
<br>
<code>docker build -t db .</code>
<br>
<code># run the database container in detached mode</code>
<br>
<code>docker run -d --name db db</code>
<br>
<code># create the 2d geospatial index on the database container</code>
<br>
<code>docker exec db mongo --eval "db.messages.createIndex({'location':'2d'})"</code>
<br>
<code>cd ../</code>
<br>
<code># create the node image</code>
<br>
<code>docker build -t node .</code>
<br>
<code># run the node container, expose the 3000 port, and link it to the database container</code>
<br>
<code>docker run -p 3000:3000 -t -i --name node1 --link db:db node /bin/bash</code>
<br>
<code># following commands are to be run on the node container</code>
<br>
<code>cd /src</code>
<br>
<code>node server.js</code>