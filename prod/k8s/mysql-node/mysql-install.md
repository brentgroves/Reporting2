<https://livebook.manning.com/book/kubernetes-in-action/chapter-10/7>
<https://www.howtoforge.com/create-a-statefulset-in-kubernetes/>

kubectl delete svc mysql-reports31-svc
kubectl delete statefulset mysql-reports31
kubectl delete pvc mysql-reports11-pvc
kubectl delete pv mysql-reports31-pv

# login to the node to install mysql

ssh brent@reports31

# make the database and backup directory

sudo mkdir /mnt/data
sudo chmod 777 /mnt/data

sudo mkdir /mnt/mysql
sudo chmod 777 /mnt/mysql
mkdir ~/backups
sudo chmod 777 ~/backups

# ftp a current dw backup onto the node

lftp brent@alb-ubu
mirror -c /home/brent/backups /home/brent/backups
mirror -c server/source_dir client/target_dir
exit

# configure mysql client from host node

mysql_config_editor print --all
setw synchronize-panes on
setw synchronize-panes off
mysql_config_editor set --login-path=client --host=reports41 --port=30011 --user=root --password

# backup all databases

mysqldump -u root -p -h reports31 --port=30031 --column-statistics=0 --add-drop-table --routines --all-databases > /home/brent/backups/db/$(/bin/date +\%Y-\%m-\%d-\%R:\%S).sql.bak

# restore datbases from a backup

mysql -u root -p -h reports31 --port=30031 < ~/backups/db/2022-11-29-13:47:12.sql.bak
mysql -u root -p -h reports31 --port=30031 < ~/backups/reports31/mysql/2023-10-19-17:29:22.sql.bak
pushd ~/src/Reporting/prod/k8s/mysql-node/

# Create a StorageClass

StorageClass helps pods provision persistent volume claims on the node.
kubectl apply -f mysql-storage-class.yaml
kubectl get storageclass

# create persistent volume and persistent volume claim using sed and kustomization

pushd ~/src/Reporting/prod/k8s/mysql-node/volume
This is for the actual database files
./sed-mysql-vol-updates.sh mysql reports41
kubectl kustomize overlay > output/volume.yaml

Deploy the PV and PVC of the YAML file:
<https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/>

# goto the output directory to deploy the volume

pushd ~/src/Reporting/prod/k8s/mysql-node/volume/output
cat volume.yaml

<!-- https://medium.com/@bingorabbit/tmux-propagate-to-all-panes-9d2bfb969f01 -->
# create persistent volume

kubectl apply -f volume.yaml
kubectl describe pv mysql-reports31-pv
kubectl describe pvc mysql-reports31-pvc

# Look at storage summary

used to be msp but in version 2 it is diskpool
kc get msp -n mayastor

pushd ~/src/Reporting/prod/k8s/mysql-node/stateful-set

app=$1
node=$2
node_port=$3
target_port=$4
target_port_name=$5
ver=$6
./sed-mysql-stateful-set-updates.sh mysql reports31 30031 3306 mysql 8.0
kubectl kustomize overlay > output/stateful-set.yaml

# deploy the stateful-set

pushd ~/src/Reporting/prod/k8s/mysql-node/stateful-set/output
kubectl apply -f stateful-set.yaml
kubectl describe svc mysql-reports31-svc
kubectl describe statefulset mysql-reports31

# validation

kubectl exec statefulset/mysql-reports31 -it -- /bin/bash
mysql -u root -ppassword
mysql -u root -p -h reports31 --port=30031 < ~/backups/db/

# configure mysql client from host node

setw synchronize-panes on
setw synchronize-panes off

mysql_config_editor print --all
mysql_config_editor set --login-path=client --host=reports11 --port=30011 --user=root --password
mysql_config_editor set --login-path=client --host=reports12 --port=30012 --user=root --password
mysql_config_editor set --login-path=client --host=reports13 --port=30013 --user=root --password

mysql_config_editor set --login-path=client --host=reports31 --port=30031 --user=root --password

mysql_config_editor set --login-path=client --host=alb-ubu --port=30101 --user=root --password
mysql_config_editor set --login-path=client --host=avi-ubu --port=30102 --user=root --password
mysql_config_editor set --login-path=client --host=frt-ubu --port=30103 --user=root --password

mysql_config_editor set --login-path=client --host=moto --port=31008 --user=root --password

mysql -u root -p -h 10.1.0.118 --port=31008
mysql

# restore datbases from a backup

mysql -u root -p -h reports11 --port=30011 < ~/backups/db/2022-10-18-06:10:01.sql.bak

mysql -u root -p -h reports31 --port=30031 < ~/backups/db/2022-10-18-06:10:01.sql.bak

mysql -u root -p -h reports12 --port=31009 < ~/backups/db/2022-10-18-06:10:01.sql.bak

mysql -u root -p -h alb-ubu --port=30101 < ~/backups/db/2022-10-18-06:10:01.sql.bak

mysql -u root -p -h avi-ubu --port=30102 < ~/backups/db/2022-10-18-06:10:01.sql.bak

mysql -u root -p -h frt-ubu --port=30103 < ~/backups/db/2022-10-18-06:10:01.sql.bak
