0


I have installed mongo DB on window server that is accessible on localhost:27017 but not accessible on 35.x.x.x:27017.

I checked:

27017 Port is open. mongoDB is running.

output of: netstat -anb | findstr :27017

TCP    127.0.0.1:27017        0.0.0.0:0              LISTENING
TCP    127.0.0.1:51186        127.0.0.1:27017        TIME_WAIT
my mongos.conf file is

dbpath = d:\MongoDB\Database
logpath = d:\MongoDB\Logs\log.txt
noauth = true # use 'true' for options that don't take an argument
bind_ip=0.0.0.0