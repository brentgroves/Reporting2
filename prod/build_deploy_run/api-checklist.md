# deploy mysql instance first
pushd ~/src/Reporting/mysql/k8s/mysql-reports/mysql-install.md for help

# port mappings
 <!-- The range of valid ports is 30000-32767 -->

10.1.0.116      reports01   30001
10.1.0.117      reports02   30002
10.1.0.118      reports03   30003
10.1.0.110      reports11   30011
10.1.0.111      reports12   30012
10.1.0.112      reports13   30013
172.20.88.61    reports31   30031
172.20.88.62    reports32   30032
172.20.88.63    reports33   30033
10.1.0.120      alb-ubu     30101
172.20.88.16    avi-ubu     30102
172.20.1.190    frt-ubu     30103
10.1.1.83       moto        31008

# remove docker container
docker container ls -a
<!-- https://docs.docker.com/engine/reference/commandline/ps/#formatting -->
docker rm -f $(docker ps -a --format "{{.ID}}|{{.Image}}|{{.CreatedAt}}.{{.Names}}" | grep "reports" | awk -F'|' '{print$1}')
I don't think you need xargs
docker rm -f $(docker ps -a --format "{{.ID}}|{{.Image}}|{{.CreatedAt}}.{{.Names}}" | grep "reports" | grep "$(date +%Y-%m-%d)" | awk -F'|' '{print$1}' | xargs)

docker container rm --force 3fd46398ff65

# remove docker image
# remove all images associated with a label
docker image prune
docker rmi $(docker image ls --format '{{.Repository}} {{.ID}}' | grep hello | awk '{ print $2}')
docker rmi $(docker images brentgroves/reporting:3 -q)
docker rmi 3f49118314d0  

# build docker image
pushd ~/src/Reporting/prod

./build.sh app node ver 
./build.sh etl reports31 1 reports31 30031 0

# start a container in the background
docker run -p 5000:5000 --name reporting -d brentgroves/reporting:3
docker container ls -a

# Next, execute an interactive bash shell on the container.
docker exec -it reporting bash

# is cron running? YES
pgrep cron


# view the cron log
tail /var/log/cron.log
# empy the cron log
cat /dev/null > /var/log/cron.log

# can we see the mobex mail server? 
dig mobexglobal-com.mail.protection.outlook.com
# can we send an email?
echo "Testing msmtp from ${HOSTNAME} with mail command" | mail -s "test mail from cron-test pod" bgroves@buschegroup.com

# activate the email job.
crontab /etc/cron.d/email-cron
crontab -l
# wait to see if email is sent

# activate the log-email job.
crontab /etc/cron.d/log-email-cron
crontab -l
# empy the cron log
cat /dev/null > /var/log/cron.log
# view the cron log
tail /var/log/cron.log

# a# wait to see if /var/log/cron.log is being populate and email is sent

# deactivate them email job
crontab -r
crontab -l

# send email from python script
python send_email.py
# wait to see if email is sent

# Test web service etl script 
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





