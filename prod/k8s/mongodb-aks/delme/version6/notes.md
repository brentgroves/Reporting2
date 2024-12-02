# AKS stateful set
https://blog.risingstack.com/deploying-a-stateful-application-on-azure-kubernetes-service-aks/

# create an Azure resource group
 $ az group create --name ghost-blog-resource --location eastus
 # locations: eastus, westeurope, centralus, canadacentral, canadaeast
 # ------
 # create a cluster
 $ az aks create --resource-group ghost-blog-resource --name ghost-blog-cluster --node-count 1 --generate-ssh-keys
 # this process could take several minutes
 # it will return a JSON with information about the cluster
 # ------
 # pass AKS Cluster credentials to kubectl
 $ az aks get-credentials --resource-group ghost-blog-resource --name ghost-blog-cluster
 # make sure it works
 $ kubectl get node
 

# BACKUP / RESTORE MONGO
https://hevodata.com/learn/install-mongodb-tools/
https://hevodata.com/learn/install-mongodb-tools/

1) Linux: Install MongoDB Tools via DEB package
Step 1: To install MongoDB Tools, download the MongoDB Database Tools .TGZ archive OR use your  Linux distribution’s package manager like apt-get/yum/dpkg/Dandified yum/gentoo etc., to get the appropriate package like .rpm/.deb/.tgz. 

You can use wget or curl to directly download the deb package from MongoDB Command Line Database Tools Download page (https://www.mongodb.com/try/download/database-tools) . 

Step 2: Next, either move the downloaded package to the directory of your choice or navigate to the directory containing the package, and run the following command:

sudo apt install ./mongodb-database-tools-*-100.5.1.deb 
Using “./” will instruct apt to look for the package in the current directory instead of any remote repos. 

Step 3: Include this directory where you just installed mongodb-database-tools, in your PATH directive. You can move the extracted mongodb-database-tools directory to /usr/local/bin. 

One of the above 2 steps will ensure that you can run the tools from any directory on your OS system. 

Step 4: Run the tools from the command line 
https://www.geeksforgeeks.org/how-to-install-and-run-mongodb-on-kubernetes/


https://www.youtube.com/watch?v=MQZ-WXZbU4w&t=207s
https://www.percona.com/blog/2022/09/21/mongodb-6-0-should-you-upgrade-now/
pushd /home/brent/src/Reporting/prod/k8s/mongodb-mayastor

# set context
scc.sh reports1.yaml mongo
or if you are already set to the correct cluster
kubectl config use-context mongo
kubectl config current-context
mongo

# delete previous copy
kubectl delete svc mongo-0
kubectl delete svc mongo
kubectl delete statefulset mongo
kubectl delete pvc mongo-store-mongo-0

kubectl apply -f config-map.yaml
kubectl get configmap
kubectl apply -f headless-service.yaml
kubectl get svc
kubectl apply -f stateful-set.yaml
kubectl get statefulsets
kubectl get pods --show-labels
kubectl get pv,pvc
kubectl apply -f nodeport-service.yaml
kubectl get svc
adminuser/password123
kubectl run -it dnsutils --image=tutum/dnsutils --rm -- /bin/bash 
nslookup mongo
Server:		10.152.183.10
Address:	10.152.183.10#53
Name:	mongo.mongo.svc.cluster.local
Address: 10.1.75.147
kubectl run -it mongo-shell --image=mongo:6.0.3 --rm -- /bin/bash
mongosh mongo.mongo.svc.cluster.local
mongosh mongo.mongo.svc.cluster.local -u adminuser -p password123 --authenticationDatabase admin
db.system.users.find()

docker run -it --rm --entrypoint /bin/sh mongo:6.0.3
mongosh --host 10.1.0.110 --port 30311 
mongosh --host reports01 --port 30007 -u sysadmin -p password123 --authenticationDatabase admin

mongosh mongo.mongo.svc.cluster.local
mongosh "mongo.mongo.svc.cluster.local" --username alice --authenticationDatabase admin

docker run -it --rm -v ${PWD}:/work -w /work --entrypoint /bin/sh mcr.microsoft.com/azure-cli:2.6.0

mongosh "mongo.mongo.svc.cluster.local" --username adminuser --authenticationDatabase admin
adminuser/password123
mongo --host reports11 --port 30311 
mongosh "mongo.mongo.svc.cluster.local" --username adminuser --authenticationDatabase admin
adminuser/password123
mongosh --host reports11 --port 30311 -u adminuser -p password123 --authenticationDatabase admin
const adminDb = db.getSiblingDB('admin');
use admin
db.system.users.find()
db.auth("adminuser", "password123");
const testDb = db.getSiblingDB('test');

https://hevodata.com/learn/install-mongodb-tools/

# insert a document into the collection
testDb.movies.insertOne(
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
# retrieve the document
db.movies.find( { title: "The Favourite" } );


use db1;
db.blogs.insert({name: "devopscube" });
db.blogs.insert({name: "moto" });
db.blogs.find();

# backup
https://www.tutorialspoint.com/mongodb/mongodb_create_backup.htm#:~:text=To%20create%20backup%20of%20database,backup%20of%20your%20remote%20server.

mongodump mongodb://adminuser:password123@reports11:30311 --out /home/brent/backups/mongo

# restore
db.movies.deleteMany({})
mongorestore mongodb://adminuser:password123@reports11:30311 /home/brent/backups/mongo

Display list of DBs

show dbs
Get inside a particular DB.


kubectl delete svc mongo
kubectl delete statefulset mongo
kubectl delete pvc mongo-store-mongo-0

kubectl apply -f nodeport-service.yaml

https://www.fosslinux.com/50317/connection-string-in-mongodb-with-examples.htm
mongodb://mongodb0.example.com:27017
mongodb://reports31:30311
mongodb://reports51:30351

const testDb = db.getSiblingDB('test');

# insert a document into the collection
testDb.movies.insertOne(
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
)
# retrieve the document
testDb.movies.find( { title: "The Favourite" } )
