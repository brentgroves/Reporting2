https://github.com/mongodb/mongodb-kubernetes-operator
https://github.com/mongodb/mongodb-kubernetes-operator/issues/829
https://www.mongodb.com/blog/post/run-secure-containerized-mongodb-deployments-using-the-mongo-db-community-kubernetes-oper
kubectl logs -f deployment.apps/mongodb-kubernetes-operator
https://github.com/mongodb/mongodb-kubernetes-operator/issues/904
kubectl exec statefulset/mongodb-reports31 -it -- /bin/bash
kubectl exec mongodb-replica-set-0 -it -- /bin/bash
kubectl exec statefulset.apps/mongodb-replica-set -it -- /bin/bash
Connecting to the Replica Set
Once the resource has been successfully created, we can connect and authenticate to the MongoDB replica set as the user we defined in the resource specification.

Now you can connect to the replica set from your application using the following connection string:

export USERNAME_DB="my-user"
export PASSWORD="$(kubectl get secret my-user-password -o  jsonpath='{.data.password}' | base64 -d)"

export CONNECTION_STRING="mongodb://${USERNAME_DB}:${PASSWORD}@mongodb-replica-set-0.mongodb-replica-set-svc.mongodb.svc.cluster.local:27017,mongodb-replica-set-1.mongodb-replica-set-svc.mongodb.svc.cluster.local:27017,mongodb-replica-set-2.mongodb-replica-set-svc.mongodb.svc.cluster.local:27017"

We can also connect directly through the mongo shell.

export MONGO_URI="$(kubectl get mdbc mongodb-replica-set -o jsonpath='{.status.mongoUri}')"

kubectl exec -it mongodb-replica-set-0 -c mongod -- mongo ${MONGO_URI} --username "${USERNAME_DB}" --password "${PASSWORD}"

kubectl exec -it mongodb-replica-set-0 -c mongod -- bash
mongo mongodb://mongodb-replica-set-0.mongodb-replica-set-svc.default.svc.cluster.local:27017,mongodb-replica-set-1.mongodb-replica-set-svc.default.svc.cluster.local:27017,mongodb-replica-set-2.mongodb-replica-set-svc.default.svc.cluster.local:27017/?replicaSet=mongodb-replica-set --username "sysadmin" --password "password123"

https://github.com/mongodb/mongodb-kubernetes-operator/issues/267
https://www.mongodb.com/docs/kubernetes-operator/master/connect/#k8s-connect-resources
mongosh --host reports01 --port 30007 -u sysadmin -p password123 --authenticationDatabase admin
mongodb://sysadmin:password123@reports01:30007/?directConnection=true&authSource=admin&appName=mongosh+1.6.1

use myDB

❯ kubectl describe pvc -n mongodb data-volume-mongodb-replica-set-0
Name:          data-volume-mongodb-replica-set-0
Namespace:     mongodb
StorageClass:  csi-rbd-sc
Status:        Pending
Volume:
Labels:        app=mongodb-replica-set-svc
Annotations:   volume.beta.kubernetes.io/storage-provisioner: rbd.csi.ceph.com
               volume.kubernetes.io/storage-provisioner: rbd.csi.ceph.com
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:
Access Modes:
VolumeMode:    Filesystem
Used By:       mongodb-replica-set-0
Events:
  Type     Reason                Age                   From                                                                                              Message
  ----     ------                ----                  ----                                                                                              -------
  Normal   Provisioning          72s (x10 over 5m26s)  rbd.csi.ceph.com_csi-rbdplugin-provisioner-6946bb54bb-bnb7s_879b3695-07bb-4b8d-b5b3-dc034bab5447  External provisioner is provisioning volume for claim "mongodb/data-volume-mongodb-replica-set-0"
  Warning  ProvisioningFailed    72s (x10 over 5m26s)  rbd.csi.ceph.com_csi-rbdplugin-provisioner-6946bb54bb-bnb7s_879b3695-07bb-4b8d-b5b3-dc034bab5447  failed to provision volume with StorageClass "csi-rbd-sc": claim Selector is not supported
  Normal   ExternalProvisioning  7s (x24 over 5m26s)   persistentvolume-controller                                                                       waiting for a volume to be created, either by external provisioner "rbd.csi.ceph.com" or manually created by system administrator

https://github.com/mongodb/mongodb-kubernetes-operator/issues/829
https://www.mongodb.com/blog/post/run-secure-containerized-mongodb-deployments-using-the-mongo-db-community-kubernetes-oper

https://github.com/mongodb/mongodb-kubernetes-operator/blob/master/docs/install-upgrade.md#install-the-operator-using-Helm
https://stackoverflow.com/questions/73154993/mongodb-community-operators-custom-resource-definitions-are-not-recognised-in-v/73186506#73186506
microk8s helm repo add mongodb https://mongodb.github.io/helm-charts

microk8s helm install community-operator mongodb/community-operator
microk8s helm uninstall community-operator
kubectl get all
kubectl delete pvc logs-volume-example-mongodb-0
kubectl delete pvc data-volume-example-mongodb-0

kubectl delete crd
kubectl delete statefulset.apps/example-mongodb
kubectl delete statefulset.apps/example-mongodb-arb
kubectl delete service/example-mongodb-svc
kubectl delete pod/example-mongodb-0
kubectl delete pvc logs-volume-example-mongodb-0
kubectl delete pvc data-volume-example-mongodb-0
kubectl delete pv mongodb-pv-01

kubectl delete statefulset.apps/example-mongodb statefulset.apps/example-mongodb-arb service/example-mongodb-svc pod/example-mongodb-0 

pod/example-mongodb-0

kubectl get deployments.apps
kubectl get role mongodb-kubernetes-operator
kubectl get rolebinding mongodb-kubernetes-operator
kubectl get serviceaccount mongodb-kubernetes-operator
kubectl get pods 
https://stackoverflow.com/questions/68366456/mongodb-community-kubernetes-operator-and-custom-persistent-volumes

First, you create a storage class for the local volumes. Something like the following:

apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

Since it has no-provisioner, it will be usable only if you manually create local PVs. WaitForFirstConsumer instead, will prevent attaching a PV to a PVC of a Pod which cannot be scheduled on the host on which the PV is available.

Second, you create the local PVs. Similarly to how you created them in your example, something like this:

apiVersion: v1
kind: PersistentVolume
metadata:
  name: example-pv
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: /path/on/the/host
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - the-node-hostname-on-which-the-storage-is-located

Notice the definition, it tells the path on the host, the capacity.. and then it explains on which node of the cluster, such PV can be used (with the nodeAffinity). It also link them to the storage class we created early.. so that if someone (a claim template) requires storage with that class, it will now find this PV.

You can create 3 PVs, on 3 different nodes.. or 3 PVs on the same node at different paths, you can organize things as you desire.

sudo rm -rf /mnt/mongo/data
sudo mkdir -p /mnt/mongo/data
ls -alh /mnt/mongo/data

sudo rm -rf /mnt/mongo/logs
sudo mkdir -p /mnt/mongo/logs
sudo chmod -R 777 /mnt/mongo
ls -alh /mnt/mongo/logs

ssh brent@reports01
cd ~/src
git clone git@ssh.dev.azure.com:v3/MobexGlobal/MobexCloudPlatform/Reporting 
pushd ~/src/Reporting/prod/k8s/mongodb-node/replica-set
cat pv-data-reports01.yaml
kubectl apply -f pv-data-reports01.yaml
kubectl describe pv pv-data-reports01

ssh brent@reports02
cd ~/src
git clone git@ssh.dev.azure.com:v3/MobexGlobal/MobexCloudPlatform/Reporting 
pushd ~/src/Reporting/prod/k8s/mongodb-node/replica-set
kubectl apply -f pv-2.yaml
kubectl describe pv mongodb-pv-02


ssh brent@reports03
cd ~/src
git clone git@ssh.dev.azure.com:v3/MobexGlobal/MobexCloudPlatform/Reporting 
pushd ~/src/Reporting/prod/k8s/mongodb-node/replica-set
kubectl apply -f pv-3.yaml
kubectl describe pv mongodb-pv-03

Third, you can now use the local-storage class in claim template. The claim template could be something similar to this:

volumeClaimTemplates:
  - metadata:
      name: mongodb-pvc
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "local-storage"
      resources:
        requests:
          storage: 5Gi