
# remove docker container
docker container ls -a
<!-- https://docs.docker.com/engine/reference/commandline/ps/#formatting -->
docker rm -f $(docker ps -a --format "{{.ID}}|{{.Image}}|{{.CreatedAt}}.{{.Names}}" | grep "reports-volume-init\|reports-api\|reports-cron" | awk -F'|' '{print$1}')

# remove docker image
# remove all images associated with a label
docker rmi $(docker image ls --format '{{.Repository}} {{.ID}}' | grep 'reports-cron\|reports-api\|reports-volume-init | awk '{ print $2}')
docker image prune

docker rmi $(docker images brentgroves/reports-cron:1 -q)
docker rmi 3f49118314d0  

# remove old k8s
kubectl delete svc reports31-api
kubectl delete deployment reports31


kubectl delete ingress,svc reporting-service 
kubectl delete deployment reporting
kubectl get pods -o wide

https://dev.to/jmarhee/getting-started-with-kubernetes-initcontainers-and-volume-pre-population-j83


