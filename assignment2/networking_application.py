#!/usr/bin/python

"""
Deployment script for Networked Application from ACE-REPO/examples/Cloud-292-Assignment-4-Application
"""
import re, sys, time, select, os, subprocess, threading, errno
from mininet.net import Mininet
from mininet.node import Controller, Host, CPULimitedHost
from mininet.cli import CLI
from subprocess import call,check_output, Popen, PIPE, STDOUT
from mininet.log import setLogLevel, info, debug
from optparse import OptionParser
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.util import isShellBuiltin, dumpNodeConnections


"global variables"
h1=0  #server1
h2=0  #server2
h3=0  #server3
h4=0  #client1
h5=0  #client2
s1=0  #switch1
s2=0  #switch2
s3=0  #switch3


"logging"

net = Mininet( controller=Controller, link=TCLink )
net.addController( 'c0' )
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
silentremove("/vagrant/server_h1.log")
silentremove("/vagrant/server_h2.log")
silentremove("/vagrant/server_h3.log")
silentremove("/vagrant/client_h4.log")
silentremove("/vagrant/client_h5.log")
silentremove("/vagrant/output.log")
output = open("output.log", "w+")



class DockerHost( Host ):
    def __init__( self, name, image='myace:v1', dargs=None, startString=None, **kwargs ):
        self.image = image
        self.dargs = dargs
        if startString is None:
            self.startString = "/bin/bash"
            self.dargs = "-ti"
        else:
            self.startString = startString
        Host.__init__( self, name, **kwargs )
    def sendCmd( self, *args, **kwargs ):
        assert not self.waiting
        printPid = kwargs.get( 'printPid', True )
        if len( args ) == 1 and type( args[ 0 ] ) is list:
            cmd = args[ 0 ]
        elif len( args ) > 0:
            cmd = args
        if not isinstance( cmd, str ):
            cmd = ' '.join( [ str( c ) for c in cmd ] )
        if not re.search( r'\w', cmd ):
            cmd = 'echo -n'
        self.lastCmd = cmd
        printPid = printPid and not isShellBuiltin( cmd )
        if len( cmd ) > 0 and cmd[ -1 ] == '&':
            cmd += ' printf "\\001%d\n\\177" $! \n'
        else:
            cmd += '; printf "\\177"'
        self.write( cmd + '\n' )
        self.lastPid = None
        self.waiting = True
        #print "command to %s = %s" %(self.name, cmd)
    def popen( self, *args, **kwargs ):
        mncmd = [ 'docker', 'attach', ""+self.name ]
        return Host.popen( self, *args, mncmd=mncmd, **kwargs )
    def terminate( self ):
        #if self.shell:
            #subprocess.call(["docker rm -f "+self.name], shell=True, stdout=output)
        self.cleanup()
    def startShell( self ):
        if self.shell:
            error( "%s: shell is already running" )
            return
        subprocess.call(["docker stop "+self.name], shell=True, stdout=output)
        subprocess.call(["docker rm -f "+self.name], shell=True, stdout=output)

        cmd = ["docker","run","--privileged","-h",self.name ,"--name="+self.name,"-v", "/vagrant:/home/ubuntu"]
        if self.dargs is not None:
            cmd.extend([self.dargs])
        cmd.extend(["--net='none'",self.image, self.startString])

        self.shell = Popen( cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True )
        self.stdin = self.shell.stdin
        self.stdout = self.shell.stdout
        self.pid = self.shell.pid
        self.pollOut = select.poll()
        self.pollOut.register( self.stdout )
        self.outToNode[ self.stdout.fileno() ] = self
        self.inToNode[ self.stdin.fileno() ] = self
        self.execed = False
        self.lastCmd = None
        self.lastPid = None
        self.readbuf = ''
        self.waiting = False
        call("sleep 1", shell=True)
        pid_cmd = ["docker","inspect","--format='{{ .State.Pid }}'",""+self.name]
        pidp = Popen( pid_cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False )
        ps_out = pidp.stdout.readlines()
        self.pid = int(ps_out[0])



def addHosts():
    global h1, h2, h3, h4, h5


    "1. Add five hosts h1, h2, h3, h4, h5 to the network"
    "2. Provide DockerHost class as the base host for all these hosts (h1..h5)"
    "3. DockerHost class is defined above for you. Dockerhost class is derived from the default Host class of mininet. Dockerclass creates containers like this sudo docker run -i -t -d --name $host --hostname $host -v /vagrant:/home/ubuntu myace:v1 /bin/bash"
    "4. so basically container will have its /home/ubuntu folder shared with VM's /vagrant folder"
    "5. You just need to pass DockerHost class as a parameter to addHost command"
    "6. Provide ips like: 10.0.0.x where x is 1 for h1 and so on till 5 for h5"
    "7. You need to write something like this h1 = net.addHost(<parameters>)"
    "8. e.g h1 = net.addHost('h1', ip='x.x.x.x', cls=HostClass)"
    "9. When you add host using addHost command, DockerHost class will first try to remove it if exits. So first time you will see some warnings/errors in red saying that there is no such container named h1. Ignore them"

    info( '\nadding host h1\n' )
    h1 = net.addHost('h1', ip='10.0.0.1', cls=DockerHost)

    info( '\nadding host h2\n' )
    h2 = net.addHost('h2', ip='10.0.0.2', cls=DockerHost)

    info( '\nadding host h3\n' )
    h3 = net.addHost('h3', ip='10.0.0.3', cls=DockerHost)

    info( '\nadding host h4\n' )
    h4 = net.addHost('h4', ip='10.0.0.4', cls=DockerHost)

    info( '\nadding host h5\n' )
    h5 = net.addHost('h5', ip='10.0.0.5', cls=DockerHost)


def addSwitches():
    global s1, s2, s3

    "1. Add three switches s1, s2 and s3"
    "2. You need to write something like this s1 = net.addSwitch(<parameters>)"
    info( '\nadding switch s1:' )
    "write your code here"

    info( '\nadding switch s2:' )
    "write your code here"

    info( '\nadding switch s3:' )
    "write your code here"



def setLinks():
    "1. set links between host and switches as follows"
    "2. s1 is connected to  h1, h2"
    "3. s2 is connected to  h4, h5"
    "4. s3 is connected to  h3"
    "4. s1 and s2 are connected to each other"
    "5. s3 and s2 are connected to each other"
    "6. You need to do something like this: net.addLink(<parameters>)"
    "7. (optional) Set some reasonable properties on all links e.g. b/w, dealy, packet loss"



    info( '\nsetting a link between switch s1 and host h1\n' )
    "write your code here"

    info( '\nsetting a link between switch s1 and host h2\n' )
    "write your code here"

    info( '\nsetting a link between switch s3 and host h3\n' )
    "write your code here"

    info( '\nsetting a link between switch s2 and host h4\n' )
    "write your code here"

    info( '\nsetting a link between switch s2 and host h5\n' )
    "write your code here"

    info( '\nsetting a link between switch s1 and switch s2\n' )
    "write your code here"

    info( '\nsetting a link between switch s3 and switch s2\n' )
    "write your code here"


def networking_application():
    "obtaining the values of hosts from network."
    h1 = net.get('h1')  
    h2 = net.get('h2')  
    h3=  net.get('h3')  
    h4 = net.get('h4')  
    h5 = net.get('h5')  

    "1. Run server on hosts h1, h2 and on h3. Run client on hosts h4 and h5"
    "2  Also make sure to redirect output to a file e.g. ./server &> /home/ubuntu/server_h1.log for h1 and so on for others."
    "3. Since /home/ubuntu of container is shared with /vagrant of VM which in turn shared with current folder where you execute vagrant up, you can view those files in any of the three machines, in host, in guest VM or in container."
    "3. You need to write something like this: server_h2 = h2.sendCmd(<command>)"
    "4. example of <command> is /bin/bash -c 'cd /home/ACE; source environment.sh; cd /home/ACE/examples/Cloud-292-Assignment-4-Application;  ./server &> /home/ubuntu/server_h1.log & /bin/bash' "
    "5. Servers can be run directly like ./server"
    "6. Clients need to be run like ./client --primary <primary-servers-ip> --backup <backup-severs-ip>"
    "  (a) client on h4 will have primary server h1 and backup server h3"
    "  (b) client on h5 will have primary server h2 and backup server h3"
    "7. /home/ACE/examples/Cloud-292-Assignment-4-Application folder has server and client executables"

  
    info( '\nrunning server_h1 i.e. server on h1\n' )
    "write your code here"

    info( '\nrunning server_h2 i.e. server on h2\n' )
    "write your code here"

    info( '\nrunning server_h3 i.e. server on h3\n' )
    "write your code here"

    info( '\nrunning client_h4 i.e. client on h4\n' )
    "write your code here"

    info( '\nrunning client_h5 i.e. client on h5\n' )
    "write your code here"


    "let it run for 20 seconds"
    info( '\nNormal case: when all links are working\n' )
    time.sleep(200);
    info( '\nFault 1: when s1-s2 link is down\n' )
    "write your code here. bring down link between s1 and s2. use net.configLinkStatus command"

    time.sleep(200);#fail over could take 30-40 seconds. be patient.
    "Now you should be able to check the log files and see if clients at h4 and h5 fail over to server at h3 since their link to h1 and h2 is severed as a consequence of bringing down s1-s2 link"
    "(optional)also you can check how link parameters that you set before like bandwidth, delay and packet loss affect this communication."


    "cleanup"
    subprocess.Popen("sudo pkill -9 controller", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':




    setLogLevel( 'info' )
    info( '\n(1) Adding (Docker/LXC) Hosts..(removing first if exists)\n' )
    #addHosts();   # Uncomment this line and implement this function. see above
    info( '\n\n(2) Adding switches..(removing first if exists)\n' )
    #addSwitches(); # Uncomment this line and implement this function. see above
    info( '\n\n(3) Setting Links amongst Hosts and Switches\n')
    #setLinks(); # Uncomment this line and implement this function. see above
    info( '\n\n(4) Starting mininet virtual network\n')
    #net.start() # Uncomment this line
    info( '\n\n(5) Deploying networking_application on this mininet network topology\n' )
    #networking_application(); # Uncomment this line and implement this function. see above
  
