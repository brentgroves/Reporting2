The Real Goal:
Trust and believe that doing good is what I want of you!
Also trust and believe that I love you and am with you always!

logs:
kubectl logs -f deployment.apps/mongodb-kubernetes-operator
mongosh --host reports01 --port 30007 -u sysadmin -p password123 --authenticationDatabase admin
Next:
https://www.mongodb.com/docs/kubernetes-operator/master/tutorial/multi-cluster-connect-from-outside-k8s/
https://stackoverflow.com/questions/57623894/how-access-mongodb-in-kubernetes-from-outside-the-cluster

just created a config map for moto.
add another persistent volume to /mnt/mongodb/01
try creating a replicaset on reports0 or reports1
with no node affinity but I think there is an infinity somewhere.
https://github.com/allyjunio/microk8s-mongodb-demo

Add another member to replica set.

verify mongosh --eval ping command will work ok?
https://devopscube.com/deploy-mongodb-kubernetes/
https://www.mongodb.com/docs/mongodb-shell/reference/options/
mongosh --quiet \
        --eval 'use moviesDatabase' \
        --eval 'show collections' \
        mongodb://localhost/

Goal:
https://earthly.dev/blog/mongodb-docker/
docker run -d -p 27017:27017 --name test-mongo mongo:latest
docker exec -it test-mongo bash
show dbs


https://github.com/mongodb/mongodb-kubernetes-operator
https://stackoverflow.com/questions/68366456/mongodb-community-kubernetes-operator-and-custom-persistent-volumes
https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/
Try to get 6 to work by modifying conf.orig and attempting to make sure mongo uses it.
https://www.mongodb.com/docs/manual/reference/configuration-options/
mongosh --disableImplicitSessions --eval db.adminCommand('ping')
The story:
Created a k8s deployment and mounted a local drive c:\data\mongo with no files in it and the deployment succeeded and I was able to access it from a nodeport: git@github.com:brentgroves/mongodb-k8s.git
The catch is that only works for mongo:4.0.8
In order to get access via a nodeport with later versions of mongo I first ran a docker image which created the database files and then copied those files to /mnt/mongodb. Only then was I able to get a stateful set to work from a nodeport.
Thanks Father!

# build docker image
We don't use this image I created currently we use the official
Ubuntu image
For Ubuntu image not if your using the official mongodb image
pushd ~/src/Reporting/prod
./build-mongodb.sh mongodb 1 27017
docker run -p 27017:27017 --name mongodb -d brentgroves/mongodb:1
docker push brentgroves/mongodb:1
kubectl delete all --all -n {namespace}
sample flask app
https://earthly.dev/blog/mongodb-docker/ 

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

kubectl delete svc mongodb-moto-svc
kubectl delete statefulset mongodb-moto
kubectl delete pvc mongodb-moto-pvc
kubectl delete pv mongodb-moto-pv
kubectl delete configmap mongodb-configmap

const username=process.env.MONGO_INITDB_ROOT_USERNAME;
const password=process.env.MONGO_INITDB_ROOT_PASSWORD;
const adminDb = db.getSiblingDB('admin');
adminDb.createUser({user: "test2", pwd: "test2", roles:[{role: "userAdminAnyDatabase" , db:"admin"}]});
kubectl logs mongodb-moto-0


const username=process.env.uname;
const password=process.env.pwd;

const adminDb = db.getSiblingDB('admin');
adminDb.auth('test2','test2');
adminDb.createUser({user: username, pwd: password, roles:[{role: "userAdminAnyDatabase" , db:"admin"}]});


adminDb.auth('test', 'test');
sudo rm -rf /mnt/mongodb
sudo mkdir -p /mnt/mongodb
sudo chmod -R 777 /mnt/mongodb

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

# create a config map
pushd ~/src/Reporting/prod/k8s/mongodb-node/config-map
kubectl apply -f config-map.yaml 
kubectl describe configmap/mongodb-configmap

# Create a StorageClass
pushd ~/src/Reporting/prod/k8s/mongodb-node/volume
StorageClass helps pods provision persistent volume claims on the node. 
kubectl apply -f mongodb-storage-class.yaml 


This is for the actual database files
# configure volume using sed and kustomization
./sed-mongodb-vol-updates.sh mongodb reports31
./sed-mongodb-vol-updates.sh mongodb moto
./sed-mongodb-vol-updates.sh mongodb brent-desktop
kubectl kustomize overlay > output/volume.yaml
replace node affinity with moto.busche-cnc.com

# create the persistent volume
pushd ~/src/Reporting/prod/k8s/mongodb-node/volume/output
kubectl apply -f volume.yaml 
kubectl describe pv mongodb-moto-pv
kubectl describe pv mongodb-reports31-pv
kubectl describe pvc mongodb-reports31-pvc

# configure stateful-set using sed and kustomization
https://www.howtoforge.com/create-a-statefulset-in-kubernetes/
https://phoenixnap.com/kb/kubernetes-mongodb#step-1
# This is for the ubuntu image
pushd ~/src/Reporting/prod/k8s/mongodb-node/stateful-set
app=$1
node=$2
node_port=$3
target_port=$4
target_port_name=$5
ver=$6
./sed-mongodb-stateful-set-updates.sh mongodb moto 30311 27017 mongo 6.0.3
./sed-mongodb-stateful-set-updates.sh mongodb reports11 30311 27017 mongo 6.0.3
./sed-mongodb-stateful-set-updates.sh mongodb brent-desktop 30311 27017 m 6.0.3

kubectl kustomize overlay > output/stateful-set.yaml
replace node affinity with moto.busche-cnc.com
pushd ~/src/Reporting/prod/k8s/mongodb-node/stateful-set/output
kubectl apply -f stateful-set.yaml 
kubectl describe svc mongodb-moto-svc
kubectl describe svc mongodb-reports31-svc
kubectl describe svc mongodb-reports31-svc
kubectl describe svc mongodb-brent-desktop-svc
kubectl describe statefulset mongodb-reports31
kubectl describe statefulset mongodb-moto
kubectl describe statefulset mongodb-brent-desktop
ls /mnt/mongodb | tee >(wc -l)
cat /var/log/syslog | grep 'mongo' | grep 'Nov 29' | grep 'err'

# create config file config map
goal is to create a root user on startup.

    const adminDb = db.getSiblingDB('admin');
    adminDb.createUser({user: "sysadmin", pwd: "password123", roles:["root"]});

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
kubectl exec statefulset/mongodb-moto -it -- /bin/bash
kubectl exec statefulset/mongodb-brent-desktop -it -- /bin/bash
kubectl get secret db-user-pass -o jsonpath='{.data.password11}' | base64 --decode
db.createUser(
{	user: "Guru99",
	pwd: "password",

	roles:[{role: "userAdminAnyDatabase" , db:"admin"}]})
kubectl exec deployment/mongodb-reports31 -it -- /bin/bash
MongoNetworkError: connect ECONNREFUSED 172.20.88.61:30331
mongodb://adminuser:password123@reports31:30331/databaseName?authSource=admin
mongodb://adminuser:password123@reports31:30331/feathers_demo
mongosh --username adminuser --authenticationDatabase admin
mongosh --host 10.1.59.185 --port 27017 -u adminuser -p password123 --authenticationDatabase admin
mongosh --host 172.20.88.61 --port 30331 -u adminuser -p password123 --authenticationDatabase admin
mongosh --host reports31 --port 30331 -u adminuser -p password123 --authenticationDatabase admin
mongosh --host moto.busche-cnc.com --port 30331 -u adminuser -p password123 --authenticationDatabase admin
mongo --host <ip> --port <port of nodeport svc> -u adminuser -p password123
mongosh --host moto --port 32000 -u adminuser -p password123 

mongosh --host brent-desktop --port 30331 -u adminuser -p password123 --authenticationDatabase admin
mongodb://reports31:30331/

mongosh --host mongo-nodeport-svc --port 30331 -u adminuser -p password123
mongosh --host mongo-nodeport-svc --port 27017 -u adminuser -p password123

const adminDb = db.getSiblingDB('admin');
adminDb.auth('username', 'password');

hello-svc.default.svc.cluster.local
https://github.com/kubernetes-sigs/kind/issues/1890
https://hevodata.com/learn/mysql-to-mongodb/

const testDb = db.getSiblingDB('test');
testDb.auth('myTester','password');

use sample_mflix

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
db.movies.find( { title: "The Favourite" } )

use db1;
db.blogs.insert({name: "devopscube" });
db.blogs.insert({name: "moto" });
db.blogs.find();


Display list of DBs

show dbs
Get inside a particular DB.

use db1




