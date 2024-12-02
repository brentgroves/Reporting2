login into that node shown in the nodeAffinity matchExpressions kubernetes.io/hostname key.
# login to the node to install mysql 
ssh brent@reports12
# make the database and backup directory
sudo mkdir /mnt/data
sudo chmod 777 /mnt/data
mkdir ~/backups

# ftp a current dw backup onto the node
lftp brent@reports11
mirror -c /home/brent/backups /home/brent/backups
mirror -c source_dir target_dir

clean-up
substitute node id for xxx:
kubectl delete deployment,svc mysql-reports32
kubectl delete pvc mysql-reports32-pv-claim
kubectl delete pv mysql-reports32-pv-volume

# goto the volume directory
pushd ~/src/Reporting/mysql/k8s/mysql-reports/volume
./sed-updates.sh volume_name claim_name    
./sed-volume.sh volume_name  
./sed-claim.sh claim_name  

./sed-updates.sh reports31 mysql-reports31 mysql-reports31
kubectl kustomize overlay > output/volume.yaml

Deploy the PV and PVC of the YAML file:
https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/


# goto the output directory to deploy the volume
pushd ~/src/Reporting/mysql/k8s/mysql-reports/volume/output

cat volume.yaml

<!-- https://medium.com/@bingorabbit/tmux-propagate-to-all-panes-9d2bfb969f01 -->
# create persistent volume
kubectl apply -f volume.yaml
kubectl describe pv mysql-reports31-pv-volume
kubectl describe pvc mysql-reports31-pv-claim

# apply deployment and service

# update yaml files with templating
pushd ~/src/Reporting/mysql/k8s/mysql-reports/deployment
./sed-updates.sh node_name node_port service_name app_name    
./sed-deployment.sh node_name app_name  
./sed-service.sh node_name node_port service_name app_name 

./sed-updates.sh reports32 30032 mysql-reports32 mysql-reports32
kubectl kustomize overlay > output/deployment.yaml

Deploy the contents of the YAML file:
cd output
cat deployment.yaml
kubectl apply -f deployment.yaml

Display information about the Deployment:
kubectl describe deployment mysql-reports31

List the pods created by the Deployment:
kubectl get pods -l app=mysql-reports31 -o wide

Inspect the PersistentVolumeClaim:
kubectl describe pvc mysql-reports31-pv-claim

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










