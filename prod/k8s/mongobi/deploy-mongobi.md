https://www.youtube.com/watch?v=VqeTT0NvRR4

scc.sh reports-aks-admin.yaml mongo 
pushd ~/src/Reporting/prod/k8s/mongobi
kubectl apply -f stateful-set.yaml --namespace mongo
<!-- kubectl apply -f config/samples/mongodb.com_v1_mayastor.yaml --namespace mongo -->
# verify
kubectl get statefulset -n mongo
kubectl get pods --namespace mongo

# try to connect to pod
kubectl -n mongo exec --stdin --tty mongobi-0 -- /bin/bash
kubectl exec --stdin --tty hit-counter-app-6fccf86fc5-dgqmq -- /bin/bash

pgrep mongosqld
tail -f -n 25 /logs/mongosqld.log

# deploy loadbalancer
kubectl apply -f loadbalancer-service.yaml
kubectl get svc
13.86.101.2

kubectl -n mongo exec --stdin --tty mongobi-0 -- /bin/bash
pgrep mongosqld
tail -f -n 25 /logs/mongosqld.log

handshake error: ERROR 1043 (08S01): recv handshake response error: read tcp 10.244.0.17:3307->10.244.0.1:34036: read: connection reset by peer
2023-03-02T00:18:18.777+0000 I NETWORK    [conn39] end connection 10.244.0.1:34036 (0 connections now open)

kubectl get svc
kubectl delete svc mongobi-0 

CREATE A headless SVC BEFORE THE LOADBALANCER
Try a higher port number in loadbalance.

# Test ODBC connection from alb-utl4

# Test from Power BI
Get data source.

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

kubectl get svc
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
IP:                       10.0.49.54
IPs:                      10.0.49.54
LoadBalancer Ingress:     20.221.103.132
Port:                     reports-mongodb-0  30351/TCP
TargetPort:               27017/TCP
NodePort:                 reports-mongodb-0  32499/TCP
Endpoints:                10.244.0.14:27017
Session Affinity:         None
External Traffic Policy:  Cluster
Events:
  Type    Reason                Age    From                Message
  ----    ------                ----   ----                -------
  Normal  EnsuringLoadBalancer  7m20s  service-controller  Ensuring load balancer
  Normal  EnsuredLoadBalancer   7m12s  service-controller  Ensured load balancer

  kubectl get pods -o wide          
NAME                                           READY   STATUS    RESTARTS   AGE   IP            NODE                              NOMINATED NODE   READINESS GATES
mongodb-kubernetes-operator-596c586b7d-g4jtm   1/1     Running   0          24h   10.244.0.13   aks-default-28895758-vmss000000   <none>           <none>
reports-mongodb-0                              2/2     Running   0          24h   10.244.0.14   aks-default-28895758-vmss000000   <none>           <none>

20.221.103.132   30351

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



