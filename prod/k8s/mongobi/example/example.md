scc.sh reports-aks-admin.yaml mongo
pushd /home/brent/src/Reporting/prod/k8s/mongobi/example
docker build -t brentgroves/bi-connector:1 .
kubectl apply -f deployment.yaml
kubectl describe deployment bi-connector
kubectl get pods -o wide
kubectl exec --stdin --tty bi-connector-75b8966b89-689rp -- /bin/bash
mongosqld --auth \
          --mongo-authenticationSource admin \
          --mongo-authenticationMechanism SCRAM-SHA-256 \
          --mongo-uri "mongodb://reports-mongodb-0.reports-mongodb-svc.mongo.svc.cluster.local:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&directConnection=true"  \
          --addr "0.0.0.0" \
          --defaultAuthMechanism SCRAM-SHA-256 \
          --mongo-username my-user \
          --mongo-password JesusLives1!
kubectl describe pod bi-connector-75b8966b89-689rp
kubectl apply -f loadbalancer.yaml

handshake error: ERROR 1043 (08S01): recv handshake response error
https://learn.microsoft.com/en-us/azure/aks/use-node-public-ips


20.80.66.135
