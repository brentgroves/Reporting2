Father please guide us in our work today!

https://askubuntu.com/questions/1403837/how-do-i-use-openssl-1-1-1-in-ubuntu-22-04

reports-cron:
This updates the crontab-reports file with Report.crontab records every minute.
Each crontab report job is inserted into the Report.queue at it's scheduled time.


**Steps to deploy all the reporting software to a k8s cluster.**  

question:
Does reports-cron insert jobs into the reports queue?
Does reports-api insert jobs into the reports queue?
Does reports-runner pull jobs from the reports queue and run them?

**setup development system**  
set python interpretter in code.  
```
ctrl-shift-p
select python interpretter at workspace level
select reports
```
create password files.  
```
conda activate reports
cd ~/src/Reporting/prod/k8s/secrets/lastpass
./lastpass.sh
```
set build scripts to prod or dev:  
```
cd ~/src/Reporting/prod/volume
./sed-volume.sh dev reports31 30031 0 reports31 30331 reports
./sed-volume.sh dev reports41 30041 0 reports41 30341 reports
```
TODO:
commit mysql backup.

For each k8s node follow these steps:
1. Follow the instructions in k8s/mysql-node/mysql-install.md to deploy the mysql statefulset to the cluster.
2. Follow the instructions in k8s/mongodb-node/mongodb-install.md to deploy the mongodb statefulset to the cluster.
3. Follow the instructions in k8s/mosquitto-node/mosquitto-install.md to deploy the mosquitto statefulset to the cluster.
4. deploy secrets
```
cd ~/src/Reporting/prod/k8s/secrets/lastpass
kubectl apply -f lastpass.yaml
```

1. follow the reports-cron checklist to deploy the reports-cron image to the k8s cluster.
We have finished the sed_update_crontab and tested dev build in reports-volume-init-checklist
next test ./sed-insert-crontab.sh $build $mysql_host $mysql_port
./sed-insert-queue.sh $build $mysql_host $mysql_port
and add sed-change-build-type to each ETL script and test for dev
before building the volume.