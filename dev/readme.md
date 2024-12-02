docker build --tag brentgroves/api1:1
https://blog.devgenius.io/how-to-deploy-rest-api-application-using-mysql-on-the-kubernetes-cluster-4c806de1a48
# https://medium.com/bb-tutorials-and-thoughts/how-to-dockerize-the-python-rest-api-with-flask-library-d2b51dd4a0ae

// run the container
docker run -d -p 5000:5000 --name api1 brentgroves/api1:1

docker push brentgroves/api1:1

// list the container
docker ps
// logs
docker logs python-restapi
// exec into running container
docker exec -it api1 /bin/sh

Use config-map.yaml to define values of environment variables that will be used in the API application

You should add the correct value for MYSQL_ROOT_HOST
Use the output of the following command

kubectl apply -f config-map.yaml

To deploy an application use web-application-deployment.yaml Add your image-name:image-tag — value that was used in the docker build command

To create deployment
kubectl apply -f web-application-deployment.yaml

To verify creation
kubectl get deployment
kubectl delete deployment web-application

To create service for this deployment run
The pod ip address may change because it is determined by the deployment, but the service IP address will stay the same. And 
the service controller scans for all the pods with the selector condition and chooses one to pass traffic to.
Added service definition to deployment so the following create service is not needed.
kubectl create service clusterip web-application --tcp=80:5000
kubectl get services
kubectl delete service web-application

These apps are now available at their internal pod IP address.
kubectl get pods -o wide
or 
# internal ip of primary pod
export primaryPodIP=$(kubectl get pods -l app=web-application -o=jsonpath="{.items[0].status.podIPs[0].ip}")

To verify all setup run
1st use the pod ip address in the curl command.
# check pod using internal IP
curl https://reports01/myhello/
https://reports11/myhello/

curl http://${primaryPodIP}:5000/hotels

curl http://${primaryPodIP}:5000/hotel -H 'Content-Type: application/json' -d '{"id":"1","name":"name1","state":"state1","rooms":"1"}'
curl -X POST http://10.1.210.65:5000/hotel -H 'Content-Type: application/json' -d '{"id":"1","name":"name1","state":"state1","rooms":"1"}'
curl -X POST http://10.1.210.65:5000/hotel -H 'Content-Type: application/json' -d '{"id":"2","name":"name2","state":"state1","rooms":"2"}'
curl http://10.1.210.65:5000/hotel
curl https://microk8s.local/hotel
curl -k https://microk8s.local/hotel


kubectl get services
# IP of primary service
export primaryServiceIP=$(kubectl get service/web-application-service -o=jsonpath="{.spec.clusterIP}")
# check primary service
curl http://${primaryServiceIP}:5000/hotel

Next use the service ip address in the curl command except with the port mapping 80.
curl -X POST http://10.152.183.234:5000/hotel -H 'Content-Type: application/json' -d '{"id":"3","name":"name3","state":"state3","rooms":"3"}'
curl http://10.152.183.234:5000/hotel


These validations proved out the pod and service independent of the NGINX ingress controller.  Notice all these were using insecure HTTP on port 8080, because the Ingress controller step in the following step is where TLS is layered on.

# IP of primary service
primaryServiceIP=$(microk8s kubectl get service/golang-hello-world-web-service -o=jsonpath="{.spec.clusterIP}")

Create TLS key and certificate
Before we expose these services via Ingress, we must create the TLS keys and certificates that will be used when serving traffic.

Primary ingress will use TLS with CN=microk8s.local
Secondary ingress will use TLS with CN=microk8s-secondary.local
The best way to do this is with either a commercial certificate, or creating your own custom CA and SAN certificates.  But this article is striving for simplicity, so we will simply generate self-signed certificates using a simple script I wrote.

# download and change script to executable
wget https://raw.githubusercontent.com/fabianlee/microk8s-nginx-istio/main/roles/cert-with-ca/files/microk8s-self-signed.sh

chmod +x microk8s-self-signed.sh

# run openssl commands that generate our key + certs in /tmp
./microk8s-self-signed.sh

# change permissions so they can be read by normal user
sudo chmod go+r /tmp/*.{key,crt}

# show key and certs created
ls -l /tmp/microk8s*


# create primary tls secret for 'microk8s.local'
microk8s kubectl create -n default secret tls tls-credential --key=/tmp/microk8s.local.key --cert=/tmp/microk8s.local.crt

# create secondary tls secret for 'microk8s-secondary.local'
microk8s kubectl create -n default secret tls tls-secondary-credential --key=/tmp/microk8s-secondary.local.key --cert=/tmp/microk8s-secondary.local.crt

# shows both tls secrets
microk8s kubectl get secrets --namespace default


# create secured ingress
kubectl apply -f web-application-ingress.yaml

# show primary and secondary Ingress objects
# primary available at 'microk8s.local'
kubectl get ingress --namespace default

# create unsecured ingress
kubectl apply -f web-application-ingress-unsecure.yaml


# shows primary and secondary ingress objects tied to MetalLB IP
microk8s kubectl get services --namespace ingress

NAME                TYPE           CLUSTER-IP       EXTERNAL-IP    PORT(S)                      AGE
ingress             LoadBalancer   10.152.183.28    172.20.88.16   80:30191/TCP,443:31891/TCP   93d
ingress-secondary   LoadBalancer   10.152.183.131   172.20.1.190   80:31139/TCP,443:31697/TCP   93d


Validate URL endpoints
The Ingress requires that the proper FQDN headers be sent by your browser, so it is not sufficient to do a GET against the MetalLB IP addresses.  You have two options:

add the ‘microk8s.local’ and ‘microk8s-secondary.local’ entries to your local /etc/hosts file
OR use the curl ‘–resolve’ flag to specify the FQDN to IP mapping which will send the host header correctly
Here is an example of pulling from the primary and secondary Ingress using entries in the /etc/hosts file.

# validate you have entries to 192.168.1.141 and .142
grep microk8s /etc/hosts

# check secured ingress
-k means that curl wont verify TLS certificate with the host that 
issued it.

curl -k https://microk8s.local/hotel
curl -k -X POST https://microk8s.local/hotel -H 'Content-Type: application/json' -d '{"id":"4","name":"name4","state":"state4","rooms":"4"}'


# check unsecure ingress
curl http://172.20.88.16/hotel
curl -X POST http://172.20.88.16/hotel -H 'Content-Type: application/json' -d '{"id":"5","name":"name5","state":"state5","rooms":"5"}'


Trouble-shooting:
kubectl exec --stdin --tty web-application-6f5578748f-zl67w  -- /bin/bash