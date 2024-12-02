# add java to dockerfile
https://stackoverflow.com/questions/72128006/connect-to-mssql-using-python-jaydebeapi-from-inside-a-docker-image
ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"

# deploy mysql instance to the node you are deploying
pushd ~/src/Reporting/prod/k8s/mysql-reports/mysql-install.md for help

# complete the reports-volume-init-checklist
code ~/src/Reporting/prod/build_deploy/reports-volume-init-checklist.md

# build reports cron app docker image
pushd ~/src/Reporting/prod
./build-reports-apps.sh app api_port ver
./build-reports-apps.sh cron 1 5000 
To only build image don't run ./build only:
docker build --tag brentgroves/reports-cron:1 --build-arg CACHEBUST=$(date +%s) .

# start a container in the background
docker run --name reports-cron -d brentgroves/reports-cron:1
docker container ls -a

# Next, execute an interactive bash shell on the container.
docker exec -it reports-cron bash

# check for resolv.conf change
# https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/#known-issues
cat /etc/resolv.conf
it should be the same as the deployment node's /run/systemd/resolve/resolv.conf file.

# push brentgroves/reports-etl:1 to docker hub
docker push brentgroves/reports-cron:1

# Start of k8s work
pushd ~/src/Reporting/prod/k8s/reports

node=$1
api_port=$2
mysql_port=$3
azure_dw=$4
ver=$5

./sed-k8s-updates.sh reports31 5000 30031 0 1   
kubectl kustomize overlays > output/deployment.yaml

kubectl apply -f output/deployment.yaml

kubectl describe deployment reports31
kubectl get pods -o wide


# shell to pod
https://www.ibm.com/docs/en/fci/1.1.0?topic=kubernetes-accessing-docker-container-in
kubectl exec --stdin --tty reports31-86d47b76b9-29rlv -c reports31-cron -- /bin/bash

# check container
tree /apps
crontab -l



https://www.spectrocloud.com/blog/how-to-share-data-between-containers-with-k8s-shared-volumes/
https://dev.to/jmarhee/getting-started-with-kubernetes-initcontainers-and-volume-pre-population-j83

# is JDBC working
from dbeaver open DW/Valiation/restrictions2.sql
and DW-MySql/Valiation/restrictions2.sql

TRUNCATE table Validation.restrictions2

cd /apps/bin
./run.sh

Check if restrictions were inserted from Albion's ToolBoss.
select count(*) cnt from Validation.restrictions2

# is cron running? YES
pgrep cron

# can we see the mobex mail server? 
cat /etc/resolv.conf
# https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/#known-issues
should be the same as ./install/resolve/resolv.conf 

https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/
https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/#known-issues
dig mobexglobal-com.mail.protection.outlook.com
# can we send an email?
echo "Testing msmtp from ${HOSTNAME} with mail command" | mail -s "test mail from etl-reports" bgroves@buschegroup.com

# verify the environment variables are correct in the crontab
crontab -l

# to remove the cron tab
crontab -r

# send email from python script
cd ../validation
python send_email.py
# wait to see if email is sent

# Test web service etl script 
# https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16#ubuntu17
<!-- if ! [[ "18.04 20.04 22.04" == *"$(lsb_release -rs)"* ]];
then
    echo "Ubuntu $(lsb_release -rs) is not currently supported.";
    exit;
else 
    echo "Ubuntu $(lsb_release -rs) is supported. TRY DEBIAN";
    exit;
fi -->
# odbc not supported under ubuntu but can use it to contact dw
python ws_to_cm_test.py
python ws_to_dw_test.py
# verify records were inserted into CM and DW
# select * from Validation.Detailed_Production_History dph 
# select * from Detailed_Production_History dph 

# Source code changes for API build
App.py:
uncomment this command.
# os.chdir('/app/etl/PipeLine')
# file_name = './TrialBalance.sh'
All python ETL scripts:
uncomment the the parameter code.
pcn = (sys.argv[1])
username2 = (sys.argv[2])
password2 = (sys.argv[3])
username3 = (sys.argv[4])
password3 = (sys.argv[5])
username4 = (sys.argv[6])
password4 = (sys.argv[7])
mysql_host = (sys.argv[8])
mysql_port = (sys.argv[9])
azure_dw = (sys.argv[10])

TrialBalanceExcel.py
Uncomment  
os.chdir('/app/output')

TrialBalance.sh
Comment out if desired:
  printf "\nPipeline Successful all scripts completed." 1>&4
  printf "Pipeline successful all scripts have completed." | mail -s "MCP Pipeline Success" bgroves@buschegroup.com
TrialBalanceValidate.sh
Comment out all but the AccountingYearCategoryType.sh script if desired.


k8s/secrets:
Make sure k8s cluster contains all key/values pairs in db-user-pass command syntax is in managing_secrets.md 


# remove docker container
docker container ls -a
<!-- https://docs.docker.com/engine/reference/commandline/ps/#formatting -->
docker rm -f $(docker ps -a --format "{{.ID}}|{{.Image}}|{{.CreatedAt}}.{{.Names}}" | grep "reporting" | awk -F'|' '{print$1}')
I don't think you need xargs
docker rm -f $(docker ps -a --format "{{.ID}}|{{.Image}}|{{.CreatedAt}}.{{.Names}}" | grep "reporting" | grep "$(date +%Y-%m-%d)" | awk -F'|' '{print$1}' | xargs)

docker container rm --force 3fd46398ff65

# remove docker image
# remove all images associated with a label
docker rmi $(docker images brentgroves/reporting:3 -q)
docker image ls
docker rmi 3f49118314d0  

# Make updates to dockerfile if needed
# Advance revision if desired
# Advance revision in k8s/reports[0-2]/reports.yaml files 

# build image 
# do this on a 16GB computer if slow.
docker build --tag brentgroves/reporting:3 --build-arg CACHEBUST=$(date +%s) .
docker build --tag brentgroves/reporting:3 .

# start a container in the background
docker run -p 5000:5000 --name reporting -d brentgroves/reporting:3
docker container ls -a

# Next, execute an interactive bash shell on the container.
docker exec -it reporting bash
vim /app/etl/PipeLine/TrialBalance.sh
uncomment the the hard coded params.
If primary DNS servers don't have entries for reports[0-2]
then add entry:
vim /etc/hosts
10.1.0.112      reports13
exit vim and bash.

# test from curl
curl -X POST http://localhost:5000/report -H 'Content-Type: application/json' -d '{"report_name":"trial_balance","email":"bgroves@buschegroup.com","start_period":202209,"end_period":202209}'

# monitor script progress
docker exec -it reporting bash
cd ../etl/PipeLine
cat dbg-msg
cat error-msg

# remove container
<!-- https://docs.docker.com/engine/reference/commandline/ps/#formatting -->
docker rm -f $(docker ps -a --format "{{.ID}}|{{.Image}}|{{.CreatedAt}}.{{.Names}}" | grep "reporting" | awk -F'|' '{print$1}')
I don't think you need xargs
docker rm -f $(docker ps -a --format "{{.ID}}|{{.Image}}|{{.CreatedAt}}.{{.Names}}" | grep "reporting" | grep "$(date +%Y-%m-%d)" | awk -F'|' '{print$1}' | xargs)

# Get ready for k8s deployment
# Source code changes
~/src/Reporting/prod/api/app.py
uncomment this command.
# os.chdir('/app/etl/PipeLine')
# file_name = './TrialBalance.sh'
All python ETL scripts:
uncomment the the parameter code.
pcn = (sys.argv[1])
username2 = (sys.argv[2])
password2 = (sys.argv[3])
username3 = (sys.argv[4])
password3 = (sys.argv[5])
username4 = (sys.argv[6])
password4 = (sys.argv[7])
mysql_host = (sys.argv[8])
mysql_port = (sys.argv[9])
azure_dw = (sys.argv[10])
TrialBalanceExcel.py
Uncomment  
os.chdir('/app/output')

TrialBalance.sh
Comment out if desired:
  printf "\nPipeline Successful all scripts completed." 1>&4
  printf "Pipeline successful all scripts have completed." | mail -s "MCP Pipeline Success" bgroves@buschegroup.com
TrialBalanceValidate.sh
Comment out all but the AccountingYearCategoryType.sh script if desired.

review reports[0-2]-deploy.yaml
review reports[0-2]-ingress.yaml

# push image
docker push brentgroves/reporting:3  

# remove old k8s
kubectl delete ingress,svc reporting-service 
kubectl delete deployment reporting
kubectl get pods -o wide

# Thank you Abba for the work that you have given us all to do!
# May I be a good friend to all people.
# deploy pod and service
cd ~/src/Reporting/prod/k8s/reports0
cd ~/src/Reporting/prod/k8s/reports1
cd ~/src/Reporting/prod/k8s/reports2
cd ~/src/Reporting/prod/k8s/dev

kubectl apply -f reports0-deploy.yaml
kubectl apply -f reports1-deploy.yaml
kubectl apply -f reports2-deploy.yaml
kubectl apply -f dev.yaml-deploy.yaml  

kubectl describe deployment reporting
kubectl get pods -o wide

These apps are now available at their internal pod IP address.
kubectl get pods -o wide





