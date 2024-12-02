docker build -t brentgroves/bi-connector:1 .
docker push brentgroves/bi-connector:1 
scc.sh reports-aks-admin.yaml mongo
pushd /home/brent/src/Reporting/prod/k8s/mongobi
kubectl run -it dnsutils --image=tutum/dnsutils --rm -- /bin/bash 
nslookup reports-mongodb-0 
Server:		10.0.0.10
Address:	10.0.0.10#53
      reports-mongodb-0.mongo.svc.cluster.local
Name:	reports-mongodb-0.mongo.svc.cluster.local
Address: 10.0.49.54

nslookup reports-mongodb-svc
cant find this

kubectl run -it mongo-shell --image=mongo:6.0.3 --rm -- /bin/bash

mongosh "reports-mongodb-0.reports-mongodb-svc.mongo.svc.cluster.local:27017/admin?replicaSet=reports-mongodb&ssl=false" --username my-user --authenticationDatabase admin
JesusLives1!

kubectl run -it mongo-shell --image=mongo:4.0.17 --rm -- /bin/bash
mongo "reports-mongodb-0.reports-mongodb-svc.mongo.svc.cluster.local:27017/admin?replicaSet=reports-mongodb&ssl=false" --username my-user --authenticationDatabase admin

https://github.com/mongodb/mongodb-kubernetes-operator/blob/master/docs/deploy-configure.md

kubectl get secret reports-mongodb-admin-my-user -n mongo \
-o json | jq -r '.data | with_entries(.value |= @base64d)'

{
  "connectionString.standard": "mongodb://my-user:JesusLives1%21@reports-mongodb-0.reports-mongodb-svc.mongo.svc.cluster.local:27017/admin?replicaSet=reports-mongodb&ssl=false",
  "connectionString.standardSrv": "mongodb+srv://my-user:JesusLives1%21@reports-mongodb-svc.mongo.svc.cluster.local/admin?replicaSet=reports-mongodb&ssl=false",
  "password": "JesusLives1!",
  "username": "my-user"
}


kubectl get secret <connection-string-secret-name> -n <my-namespace> \
-o json | jq -r '.data | with_entries(.value |= @base64d)'