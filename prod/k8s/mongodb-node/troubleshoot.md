# Questions
Why can I login locally but not remotely in mongodb 
mongod --config /shared/config/config.conf
cat /var/log/syslog | grep 'mongo' | grep 'Nov 24' | grep 'err'

# authentication failed
If I just create the stateful set from scratch then
the admin database has no users
so I create the database from a docker image
and copy the database to the new node with user and collections 
mongosh 127.0.0.1:27017/admin -u sysadmin -p password123
mongosh 127.0.0.1:27017
show databases
use admin
db.system.users.find()
use reports
db.createUser({user:"user1", pwd:"user1", roles:[{role:"dbOwner", db: "reports"}]})

mongosh 127.0.0.1:27017/reports -u user1 -p user1

from k8s node
mongosh 10.152.183.250:27017/admin -u sysadmin -p password123
mongosh 192.168.1.2:30331/admin -u sysadmin -p password123

https://stackoverflow.com/questions/37372684/mongodb-3-2-authentication-failed
Well, you'll need to take couple of steps in sequence to create user successfully.

First of all, you need to create an administrator user. I prefer creating super user.

> use admin
> db.createUser({user: "sysadmin", pwd: "password123", roles:["root"]})
Restart your MongoDB server and enable authentication with --auth flag.

> mongod --auth --port 27017 --dbpath /data/db
Once your server is up, connect to it as administrator

mongosh -u "sysadmin" -p "password123" --authenticationDatabase "admin"

> mongosh brent-desktop:2<host:port> -u "sysadmin" -p "password123" --authenticationDatabase "admin"

Once you are connected, create normal user. Assuming your user database name is cd2.

> use cd2
> db.createUser({user: "cd2", pwd: "cd2", roles:["dbOwner"]})
If you see success messsage, disconnect from mongo shell and reconnect with new user credentials.

> mongo <host:port>/cd2 -u "cd2" -p "cd2"
