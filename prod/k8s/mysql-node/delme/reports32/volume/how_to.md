./sed-updates.sh volume_name claim_name    
./sed-volume.sh volume_name  
./sed-claim.sh claim_name  

pushd ~/src/Reporting/mysql/k8s/mysql-reports/%cluster_dir%/%node%/volume
./sed-updates.sh mysql-reports32 mysql-reports32
kubectl kustomize overlay > output/volume.yaml

clean-up
substitute node id for xxx:
kubectl delete deployment,svc mysql-reports31
kubectl delete pvc mysql-reports31-pv-claim
kubectl delete pv mysql-reports31-pv-volume

Deploy the PV and PVC of the YAML file:
https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/

# goto mysql directory
pushd ~/src/Reporting/mysql/k8s/mysql-reports
cd reports0 | cd reports1 | cd reports2 | cd reports3 | cd ubu | cd moto
# go to the node volume subdirectory of your choice.
pushd reports31/volume

pushd output
examine volume.yaml
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
exit

<!-- https://medium.com/@bingorabbit/tmux-propagate-to-all-panes-9d2bfb969f01 -->
# create persistent volume
kubectl apply -f volume.yaml
kubectl describe pv mysql-reports31-pv-volume
kubectl describe pvc mysql-reports31-pv-claim







