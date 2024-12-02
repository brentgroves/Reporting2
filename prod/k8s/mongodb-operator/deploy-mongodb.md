https://www.youtube.com/watch?v=VqeTT0NvRR4

https://github.com/mongodb/mongodb-kubernetes-operator/blob/master/docs/deploy-configure.md
kubectl apply -f config/samples/mongodb.com_v1_mayastor.yaml --namespace mongo
# verify
kubectl get mongodbcommunity --namespace mongo

kubectl get secret example-mongodb-admin-my-user -n mongo \
-o json | jq -r '.data | with_entries(.value |= @base64d)'

The Community Kubernetes Operator creates secrets that contains users' connection strings and credentials.

The secrets follow this naming convention: <metadata.name>-<auth-db>-<username>, where:

Variable	Description	Value in Sample
<metadata.name>	Name of the MongoDB database resource.	example-mongodb
<auth-db>	Authentication database where you defined the database user.	admin
<username>	Username of the database user.	my-user

kubectl get secret <connection-string-secret-name> -n <my-namespace> \
-o json | jq -r '.data | with_entries(.value |= @base64d)'

{
  "connectionString.standard": "mongodb://my-user:JesusLives1%21@example-mongodb-0.example-mongodb-svc.mongo.svc.cluster.local:27017,example-mongodb-1.example-mongodb-svc.mongo.svc.cluster.local:27017,example-mongodb-2.example-mongodb-svc.mongo.svc.cluster.local:27017/admin?replicaSet=example-mongodb&ssl=false",
  "connectionString.standardSrv": "mongodb+srv://my-user:JesusLives1%21@example-mongodb-svc.mongo.svc.cluster.local/admin?replicaSet=example-mongodb&ssl=false",
  "password": "JesusLives1!",
  "username": "my-user"
}

# edit delployment
https://www.youtube.com/watch?v=VqeTT0NvRR4
kubectl edit mongodbcommunity.mongodbcommunity.mongodb.com example-mongodb -n mongo

# try to connect to pod
kubectl -n mongo exec --stdin --tty example-mongodb-0 -- /bin/bash
mongo -u adminuser

use admin
db.createUser({user: "adminuser" , pwd: "password123", roles: [  "userAdminAnyDatabase","readWriteAnyDatabase" ]})
https://www.mongodb.com/docs/manual/reference/method/db.grantRolesToUser/
db.createUser({user: "adminuser" , pwd: "password123", 
roles:
[{
  "role" : "clusterAdmin",
  "db" : "admin"
},
{
  "role" : "dbAdminAnyDatabase",
  "db" : "admin"
},
{
  "role" : "readWriteAnyDatabase",
  "db" : "admin"
}]
);

db.getUsers({ showCredentials: true })

db.auth("adminuser", "password123");
use test
db.movies.insertOne(
  {
    title: "The Favourite 5",
    genres: [ "Drama", "History" ],
    runtime: 121,
    rated: "R",
    year: 2018,
    directors: [ "Yorgos Lanthimos" ],
    cast: [ "Olivia Colman", "Emma Stone", "Rachel Weisz" ],
    type: "movie"
  }
);
db.movies.find( { } );

{
  "connectionString.standard": "mongodb://my-user:JesusLives1%21@example-mongodb-0.example-mongodb-svc.mongo.svc.cluster.local:27017,example-mongodb-1.example-mongodb-svc.mongo.svc.cluster.local:27017,example-mongodb-2.example-mongodb-svc.mongo.svc.cluster.local:27017/admin?replicaSet=example-mongodb&ssl=false",
  "connectionString.standardSrv": "mongodb+srv://my-user:JesusLives1%21@example-mongodb-svc.mongo.svc.cluster.local/admin?replicaSet=example-mongodb&ssl=false",
  "password": "JesusLives1!",
  "username": "my-user"
}

kubectl run -it mongo-shell --image=mongo:6.0.3 --rm -- /bin/bash

mongosh example-mongodb-0.example-mongodb-svc.mongo.svc.cluster.local -u adminuser -p
const testDb = db.getSiblingDB('test');
use test;
db.movies.insertOne(
  {
    title: "The Favourite",
    genres: [ "Drama", "History" ],
    runtime: 121,
    rated: "R",
    year: 2018,
    directors: [ "Yorgos Lanthimos" ],
    cast: [ "Olivia Colman", "Emma Stone", "Rachel Weisz" ],
    type: "movie"
  }
);

db.movies.find( { } );
