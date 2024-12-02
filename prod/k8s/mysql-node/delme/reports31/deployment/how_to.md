./sed-updates.sh service_name app_name    
./sed-deployment.sh app_name  
./sed-service.sh service_name app_name 

pushd ~/src/Reporting/mysql/k8s/mysql-reports/%cluster_dir%/%node%/deployment
./sed-updates.sh mysql-reports31 mysql-reports31
kubectl kustomize overlays > output/deployment.yaml

clean-up
substitute node id for xxx:
kubectl delete deployment,svc mysql-reports31
<!-- kubectl delete pvc mysql-reports31-pv-claim
kubectl delete pv mysql-reports31-pv-volume -->


Deploy the contents of the YAML file:
kubectl apply -f deployment.yaml

Display information about the Deployment:
kubectl describe deployment mysql-reports31

List the pods created by the Deployment:
kubectl get pods -l app=mysql-reports31 -o wide

Inspect the PersistentVolumeClaim:
kubectl describe pvc mysql-reports31-pv-claim

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
mysql -u root -p -h reports11 --port=31008 < ~/backups/db/2022-10-18-06:10:01.sql.bak
mysql -u root -p -h reports12 --port=31009 < ~/backups/db/2022-10-18-06:10:01.sql.bak

mysql -u root -p -h alb-ubu --port=30101 < ~/backups/db/2022-10-18-06:10:01.sql.bak

mysql -u root -p -h avi-ubu --port=30102 < ~/backups/db/2022-10-18-06:10:01.sql.bak

mysql -u root -p -h frt-ubu --port=30103 < ~/backups/db/2022-10-18-06:10:01.sql.bak

