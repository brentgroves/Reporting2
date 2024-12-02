# build docker image
For Ubuntu image not if your using the official mongodb alpine image
pushd ~/src/Reporting/prod
./build-mongodb.sh mongodb 1 27017
docker run -p 27017:27017 --name mongodb -d brentgroves/mongodb:1
docker push brentgroves/mongodb:1

https://iamabhishek-dubey.medium.com/mongodb-setup-in-kubernetes-using-mongodb-operator-9a7be44ee70
A stateful set is a Kubernetes object which is preferred when we require each pod to have its own independent state and use its own individual volume.
This is the stateful set instructions.
https://phoenixnap.com/kb/kubernetes-mongodb#step-1
https://phoenixnap.com/kb/best-linux-text-editors-for-coding
https://www.howtoforge.com/create-a-statefulset-in-kubernetes/
# try brackets
This is the deployment instructions
https://devopscube.com/deploy-mongodb-kubernetes/

clean-up
substitute node id for xxx:
kubectl delete svc mongodb-reports31-svc
kubectl delete statefulset mongodb-reports31
kubectl delete pvc mongodb-reports31-pvc
kubectl delete pv mongodb-reports31-pv

# ftp a current dw backup onto the node
lftp brent@reports31
mirror -c /mnt/mongo4 /home/brent/mongo4
mirror -c /mnt/mongo4/.mongodb /home/brent/mongo4/.mongodb
mirror -c source_dir target_dir
exit
sudo cp -rp /home/brent/mongo4 /mnt/mongodb

pushd ~/src/Reporting/prod/k8s/mongodb-node/
# Create a secret
kubectl apply -f mongodb-secrets.yaml
# add user lists and roles
# did not do users-list yet
# this is for debugging on the localhost
sudo mkdir -p /etc/reports/admin
sudo chmod -R 777 /etc/reports
nvim /etc/reports/admin/MONGO_ROOT_USERNAME
adminuser
nvim /etc/reports/admin/MONGO_ROOT_PASSWORD
password123
nvim /etc/reports/MONGO_USERS_LIST


# Create a StorageClass
pushd ~/src/Reporting/prod/k8s/mongodb-node/volume
StorageClass helps pods provision persistent volume claims on the node. 
kubectl apply -f mongodb-storage-class.yaml 

This is for the actual database files
# configure volume using sed and kustomization
./sed-mongodb-vol-updates.sh mongodb reports31
kubectl kustomize overlay > output/volume.yaml

# create the persistent volume
pushd ~/src/Reporting/prod/k8s/mongodb-node/volume/output
kubectl apply -f volume.yaml 
kubectl describe pv mongodb-reports31-pv
kubectl describe pvc mongodb-reports31-pvc

# configure stateful-set using sed and kustomization
https://www.howtoforge.com/create-a-statefulset-in-kubernetes/
https://phoenixnap.com/kb/kubernetes-mongodb#step-1
# This is for the alpine image
pushd ~/src/Reporting/prod/k8s/mongodb-node/stateful-set
app=$1
node=$2
node_port=$3
target_port=$4
target_port_name=$5
ver=$6
./sed-mongodb-stateful-set-updates.sh mongodb reports11 30311 27017 mongo 6.0.3

kubectl kustomize overlay > output/stateful-set.yaml

pushd ~/src/Reporting/prod/k8s/mongodb-node/stateful-set/output
kubectl apply -f stateful-set.yaml 
kubectl describe svc mongodb-reports31-svc
kubectl describe statefulset mongodb-reports31
ls /mnt/mongodb | tee >(wc -l)
cat /var/log/syslog | grep 'mongo' | grep 'Nov 29' | grep 'err'

# create config file config map
Not using this yet only command arguments so far
this url has good example of using javascript in a config file
https://phoenixnap.com/kb/kubernetes-mongodb#step-1
pushd ~/src/Reporting/prod/k8s/mongodb-node/deployment

apiVersion: v1
kind: ConfigMap
metadata:
  name: mongodb-configmap
data:
  mongo.conf: |
    storage:
      dbPath: /data/db

kubectl create configMap mongodb-config-file --from-file=conf=mongodb.conf

https://www.cloudytuts.com/guides/kubernetes/how-to-deploy-mongodb-on-kubernetes/

# Validation

kubectl exec statefulset/mongodb-reports31 -it -- /bin/bash

kubectl exec deployment/mongodb-reports31 -it -- /bin/bash
MongoNetworkError: connect ECONNREFUSED 172.20.88.61:30331
mongodb://adminuser:password123@reports31:30331/databaseName?authSource=admin
mongodb://adminuser:password123@reports31:30331/feathers_demo
mongosh --username adminuser --authenticationDatabase admin
mongosh --host 10.1.59.185 --port 27017 -u adminuser -p password123 --authenticationDatabase admin
mongosh --host 172.20.88.61 --port 30331 -u adminuser -p password123 --authenticationDatabase admin
mongosh --host reports31 --port 30331 -u adminuser -p password123 --authenticationDatabase admin
mongodb://reports31:30331/

mongosh --host mongo-nodeport-svc --port 30331 -u adminuser -p password123
mongosh --host mongo-nodeport-svc --port 27017 -u adminuser -p password123

hello-svc.default.svc.cluster.local
https://github.com/kubernetes-sigs/kind/issues/1890
https://hevodata.com/learn/mysql-to-mongodb/
use sample_mflix
# insert a document into the collection
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
)
# retrieve the document
db.movies.find( { title: "The Favourite" } )

use db1;
db.blogs.insert({name: "devopscube" });
db.blogs.find();


Display list of DBs

show dbs
Get inside a particular DB.

use db1




