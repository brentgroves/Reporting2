https://hub.docker.com/_/eclipse-mosquitto

clean-up
substitute node id for xxx:
kubectl delete svc mosquitto-reports31-svc
kubectl delete statefulset mosquitto-reports31
kubectl delete pvc mosquitto-reports31-pvc
kubectl delete pv mosquitto-reports31-pv


# initialize the mosquitto directories on host that will be on the mosquitto volume.
pushd ~/src/Reporting/prod/k8s/mosquitto-node
sudo mkdir /mnt/mosquitto
sudo chmod 777 /mnt/mosquitto
mkdir /mnt/mosquitto/data
mkdir /mnt/mosquitto/log
mkdir /mnt/mosquitto/config
<!-- http://www.steves-internet-guide.com/mossquitto-conf-file/ -->
cp ./mosquitto.conf /mnt/mosquitto/config/
nvim /mnt/mosquitto/config/mosquitto.conf

# Create a StorageClass
pushd ~/src/Reporting/prod/k8s/mosquitto-node/volume
StorageClass helps pods provision persistent volume claims on the node. 
kubectl apply -f mosquitto-storage-class.yaml 


# goto the volume directory
pushd ~/src/Reporting/prod/k8s/mosquitto-node/volume
./sed-mqtt-vol-updates.sh app node    
./sed-mqtt-vol-updates.sh mosquitto reports31    
kubectl kustomize overlay > output/volume.yaml

# goto the output directory to deploy the volume
pushd ~/src/Reporting/prod/k8s/mosquitto-node/volume/output
cat volume.yaml

<!-- https://medium.com/@bingorabbit/tmux-propagate-to-all-panes-9d2bfb969f01 -->
# create persistent volume
kubectl apply -f volume.yaml
kubectl describe pv mosquitto-reports31-pv
kubectl describe pvc mosquitto-reports31-pv-claim

# configure stateful-set using sed and kustomization
https://www.howtoforge.com/create-a-statefulset-in-kubernetes/
https://phoenixnap.com/kb/kubernetes-mongodb#step-1

Thank you Father for the work you have given us to do!
We do this work with your bodies, minds, and strength and you let us be with you so thank you for everything!

pushd ~/src/Reporting/prod/k8s/mosquitto-node/stateful-set
./sed-mqtt-stateful-set-updates.sh node_name node_port service_name 
app=$1
node=$2
node_port=$3
target_port=$4
target_port_name=$5
ver=$6
./sed-mqtt-stateful-set-updates.sh mosquitto reports31 30231 1883 mqtt 2.0.15
kubectl kustomize overlay > output/stateful-set.yaml

cd output
kubectl apply -f stateful-set.yaml
Display information about the stateful-set:
kubectl describe service mosquitto-reports31-svc
kubectl describe statefulset mosquitto-reports31

# test by running 2 pod shells
kubectl exec --stdin --tty mosquitto-reports31-0 -- sh
mosquitto_sub -t mytopic 
kubectl exec --stdin --tty mosquitto-reports31-0 -- sh
mosquitto_pub -t mytopic -m "Hello World"
# test from outside of k8s pod that mosquitto is running
mosquitto_pub -t mytopic -h reports31 -p 30231 -m "Hello World"
# test nodeport service by connecting to the node ip from outside of the k8s cluster by opening 2 terminals.
mosquitto_sub -h reports31 -p 30231 -t mytopic 
mosquitto_pub -h reports31 -p 30231 -t mytopic -m "Hello World"
# test sending json 
export var1=30
mosquitto_pub -h reports31 -p 30231 -t mytopic -m "{\"value1\":20,\"value2\":$var1}"


mosquitto_pub -h 10.1.59.168 -m "test message" -t house/bulb1 -d
mosquitto_pub -h reports31 -m "test message" -t house/bulb1 -d
# configure mysql client from host node
mysql_config_editor print --all
mysql_config_editor set --login-path=client --host=reports11 --port=30011 --user=root --password 
mysql_config_editor set --login-path=client --host=reports12 --port=30012 --user=root --password 
mysql_config_editor set --login-path=client --host=reports13 --port=30013 --user=root --password 

mysql_config_editor set --login-path=client --host=reports31 --port=30031 --user=root --password 

mysql_config_editor set --login-path=client --host=reports32 --port=30032 --user=root --password 


mysql_config_editor set --login-path=client --host=alb-ubu --port=30101 --user=root --password 
mysql_config_editor set --login-path=client --host=avi-ubu --port=30102 --user=root --password 
mysql_config_editor set --login-path=client --host=frt-ubu --port=30103 --user=root --password 

mysql_config_editor set --login-path=client --host=moto --port=31008 --user=root --password 

mysql -u root -p -h 10.1.0.118 --port=31008
mysql

# restore datbases from a backup
mysql -u root -p -h reports11 --port=31008 < ~/backups/db/2022-10-18-06:10:01.sql.bak
mysql -u root -p -h reports12 --port=31009 < ~/backups/db/2022-10-18-06:10:01.sql.bak

mysql -u root -p -h reports32 --port=30032 < ~/backups/db/2022-10-18-06:10:01.sql.bak
mysql -u root -p -h reports33 --port=30033 < ~/backups/db/2022-10-18-06:10:01.sql.bak

mysql -u root -p -h alb-ubu --port=30101 < ~/backups/db/2022-10-18-06:10:01.sql.bak
mysql -u root -p -h avi-ubu --port=30102 < ~/backups/db/2022-10-18-06:10:01.sql.bak
mysql -u root -p -h frt-ubu --port=30103 < ~/backups/db/2022-10-18-06:10:01.sql.bak


kubectl exec --stdin --tty mysql-7cd567cc69-l9c6j -- /bin/bash










