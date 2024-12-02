# git my fork of mongodb-kubernetes-operator
git clone git@github.com:brentgroves/mongodb-kubernetes-operator-1.git

https://www.youtube.com/watch?v=VqeTT0NvRR4
https://www.youtube.com/watch?v=VqeTT0NvRR4
https://github.com/mongodb/mongodb-kubernetes-operator

scc.sh reports-aks-mobex.yaml mongo
if mongo ns does not exist
  pushd ~/src/linux-utils/kubectl/namespaces/
  kubectl apply -f mongo.yaml
  <!-- pushd ~/src/Reporting/prod/k8s/mongodb-aks -->
cd ~/src
git clone git@github.com:brentgroves/mongodb-kubernetes-operator-1.git
pushd ~/src/mongodb-kubernetes-operator-1

# Install in a Different Namespace using kubectl
To configure the Operator to watch resources in other namespaces:

For each namespace that you want the Operator to watch, run the following commands to deploy a Role, RoleBinding and ServiceAccount in that namespace:

# update mongodb-kubernetes-operator-1/config/manager/manager.yaml with mongo namespace
        env:
        - name: WATCH_NAMESPACE
          value: "mongo"  
# Modify the clusterRoleBinding namespace value for the serviceAccount mongodb-kubernetes-operator to the namespace in which the operator is deployed.
mongodb-kubernetes-operator-1/deploy/clusterwide/cluster_role_binding.yaml

- kind: ServiceAccount
  namespace: mongo
  name: mongodb-kubernetes-operator

kubectl apply -f deploy/clusterwide
kubectl apply -k config/rbac --namespace mongo

# Install the Custom Resource Definitions.

a. Invoke the following command: Make sure to apply the CRD file from the git tag version of the operator you are attempting to install.

kubectl apply -f config/crd/bases/mongodbcommunity.mongodb.com_mongodbcommunity.yaml

b. Verify that the Custom Resource Definitions installed successfully:

kubectl get crd/mongodbcommunity.mongodbcommunity.mongodb.com

Install the necessary roles and role-bindings:

a. Invoke the following command:
Already did this.
kubectl apply -k config/rbac --namespace mongo

b. Verify that the resources have been created:

kubectl get role mongodb-kubernetes-operator --namespace mongo

kubectl get rolebinding mongodb-kubernetes-operator --namespace mongo

kubectl get serviceaccount mongodb-kubernetes-operator --namespace mongo

Install the Operator.

a. Invoke the following kubectl command to install the Operator in the specified namespace:

kubectl create -f config/manager/manager.yaml --namespace mongo
b. Verify that the Operator installed successsfully:

kubectl get pods --namespace mongo
