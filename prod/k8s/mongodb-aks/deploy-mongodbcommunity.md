https://www.youtube.com/watch?v=VqeTT0NvRR4

https://github.com/mongodb/mongodb-kubernetes-operator/blob/master/docs/deploy-configure.md
https://github.com/mongodb/mongodb-kubernetes-operator/blob/master/docs/deploy-configure.md
pushd ~/src/Reporting/prod/k8s/mongodb-aks
kubectl apply -f mongodbcommunity.yaml --namespace mongo
<!-- kubectl apply -f config/samples/mongodb.com_v1_mayastor.yaml --namespace mongo -->
# verify
kubectl get pods --namespace mongo
kubectl get mongodbcommunity --namespace mongo
kubectl get pvc -n mongo

kubectl get secret reports-mongodb-admin-my-user -n mongo \
-o json | jq -r '.data | with_entries(.value |= @base64d)'
{
  "connectionString.standard": "mongodb://my-user:SmVzdXNMaXZlczEh@reports-mongodb-0.reports-mongodb-svc.mongo.svc.cluster.local:27017/admin?replicaSet=reports-mongodb&ssl=false",
  "connectionString.standardSrv": "mongodb+srv://my-user:SmVzdXNMaXZlczEh@reports-mongodb-svc.mongo.svc.cluster.local/admin?replicaSet=reports-mongodb&ssl=false",
  "password": "SmVzdXNMaXZlczEh",
  "username": "my-user"
}

{
  "connectionString.standard": "mongodb://my-user:JesusLives1%21@reports-mongodb-0.reports-mongodb-svc.mongo.svc.cluster.local:27017/admin?replicaSet=reports-mongodb&ssl=false",
  "connectionString.standardSrv": "mongodb+srv://my-user:JesusLives1%21@reports-mongodb-svc.mongo.svc.cluster.local/admin?replicaSet=reports-mongodb&ssl=false",
  "password": "JesusLives1!",
  "username": "my-user"
}

# edit delployment
https://www.youtube.com/watch?v=VqeTT0NvRR4
kubectl edit mongodbcommunity.mongodbcommunity.mongodb.com reports-mongodb -n mongo

# try to connect to pod
kubectl -n mongo exec --stdin --tty reports-mongodb-0 -- /bin/bash
mongo -u my-user

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

kubectl run -it mongo-shell --image=mongo:6.0.3 --rm -- /bin/bash

mongosh reports-mongodb-0.reports-mongodb-svc.mongo.svc.cluster.local -u my-user -p
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


pushd ~/src/Reporting/prod/k8s/mongodb-aks
kubectl get svc
NAME                  TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)     AGE
reports-mongodb-svc   ClusterIP   None         <none>        27017/TCP   24h

kubectl apply -f loadbalancer-service.yaml

export RESOURCEGROUP=reports-aks
export NODERESOURCEGROUP="MC_reports-aks_reports-aks_centralus"
export VNET="aks-vnet-35600829"
export SUBNET="aks-subnet"
export NSG="aks-agentpool-35600829-nsg"

az network public-ip list -g $NODERESOURCEGROUP
"ipAddress": "20.109.234.112",
  "tags": {
    "aks-managed-cluster-name": "reports-aks",
    "aks-managed-cluster-rg": "reports-aks",
    "aks-managed-type": "aks-slb-managed-outbound-ip"
  },

"ipAddress": "20.221.103.132",
"tags": {
  "k8s-azure-cluster-name": "kubernetes",
  "k8s-azure-service": "mongo/reports-mongodb-0"
},

az vm list -g $NODERESOURCEGROUP
# mobex
kubectl get svc
NAME                  TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)           AGE
reports-mongodb-0     LoadBalancer   10.0.131.165   20.37.141.8   30361:30729/TCP   30s
reports-mongodb-svc   ClusterIP      None           <none>        27017/TCP         53m
# outlook aks
reports-mongodb-0     LoadBalancer   10.0.49.54   20.221.103.132   30351:32499/TCP   5m21s
reports-mongodb-svc   ClusterIP      None         <none>           27017/TCP         24h

kubectl describe svc reports-mongodb-0
Name:                     reports-mongodb-0
Namespace:                mongo
Labels:                   <none>
Annotations:              <none>
Selector:                 statefulset.kubernetes.io/pod-name=reports-mongodb-0
Type:                     LoadBalancer
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.0.131.165
IPs:                      10.0.131.165
LoadBalancer Ingress:     20.37.141.8
Port:                     reports-mongodb-0  30361/TCP
TargetPort:               27017/TCP
NodePort:                 reports-mongodb-0  30729/TCP
Endpoints:                10.244.0.8:27017
Session Affinity:         None
External Traffic Policy:  Cluster
Events:
  Type    Reason                Age   From                Message
  ----    ------                ----  ----                -------
  Normal  EnsuringLoadBalancer  116s  service-controller  Ensuring load balancer
  Normal  EnsuredLoadBalancer   107s  service-controller  Ensured load balancer


  kubectl get pods -o wide          
NAME                                           READY   STATUS    RESTARTS   AGE   IP            NODE                              NOMINATED NODE   READINESS GATES
mongodb-kubernetes-operator-596c586b7d-g4jtm   1/1     Running   0          24h   10.244.0.13   aks-default-28895758-vmss000000   <none>           <none>
reports-mongodb-0                              2/2     Running   0          24h   10.244.0.14   aks-default-28895758-vmss000000   <none>           <none>

20.221.103.132   30351
# mobex
mongosh 20.37.141.8:30361 -u my-user -p
# outlook
mongosh 20.221.103.132:30351 -u my-user -p

mongodb://my-user:JesusLives1%21@20.221.103.132:30351/admin?connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-256&3t.uriVersion=3&3t.connection.name=reports5-mongodb&3t.databases=admin&3t.alwaysShowAuthDB=true&3t.alwaysShowDBFromUserRole=true

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



