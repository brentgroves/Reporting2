service_name=$1 
app=$2
ver=$3

./sed-updates.sh reports11-etl reports11-etl 1   
kubectl kustomize overlays/reports11 > output/deployment.yaml

./sed-updates.sh reports31-etl reports31-etl 1   
kubectl kustomize overlays/reports11 > output/deployment.yaml
