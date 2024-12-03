# **[debug and test pods](https://medium.com/@shambhand2020/create-the-various-debug-or-test-pod-inside-kubernetes-cluster-e4862c767b96)**

## Run sql client from any host

```bash
sqlcmd -C -S microk8s-vm,31433 -U sa -P  -d mgdw  
```

## create a pod with running mssql client

Apply following gist by clicking on view raw and run kubectl apply -f <gist raw file link> -n <namespace> Once deployment created you can exec into pod and run sqlcmd -S <db-host>,1433 -U <username> -P <password> -d <db-name> -Q "SELECT * FROM <table_name>" After your testing or debugging it can be deleted by kubectl delete -f <gist raw file link> -n <namespace>

```bash
pushd .
cd ~/src/repsys/k8s/sql_server
kubectl apply -f mssql_client.yaml

kubectl exec -it mssql-client-deployment -n mgdw bash

# ~/src/secrets/namespaces/default/credentials.yaml 
sqlcmd -S <db-host>,1433 -U <username> -P <password> -d <db-name> -Q "SELECT * FROM <table_name>"


```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mssql-client-deployment
  labels:
    app: mssql-client
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mssql-client
  template:
    metadata:
      labels:
        app: mssql-client
    spec:
      containers:
      - name: mssql-client
        image: liaisonintl/mssql-server-linux
        ports:
        - containerPort: 1433
        
# kubectl exec -it <mssql-client-deployment-pod> -n <namespace> bash

# sqlcmd -S <db-host>,1433 -U <username> -P <password> -d <db-name> -Q "SELECT * FROM <table_name>"

```

If the above gist did not work — creating pod and exec in did not work then we can follow the instructions for **[microsoft documentation to install mssql-command line tools](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-ver16&tabs=ubuntu2204#tools)**:

**Create a ubuntu pod**\

```bash
kubectl run ubuntu --image=ubuntu:latest --command sleep 604800 -n <namespace>
```

Install the pre requisite tools into ubuntu contains

```bash
kubectl exec -it pods/ubuntu -n <namespace> - sh
apt update -y && apt install curl -y && apt install sudo -y
```

Then run the instructions from the microsoft documentation for ubuntu

Run the sql query on the exec container shell

```bash
sqlcmd -S <DB_HOST>,<DB_PORT e.g. 1433> -U <DB_USER> -P <password> -C -d messaging -Q "<sql query>";
```
