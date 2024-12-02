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
kubectl create -n default secret tls tls-credential --key=/tmp/microk8s.local.key --cert=/tmp/microk8s.local.crt

# create secondary tls secret for 'microk8s-secondary.local'
microk8s kubectl create -n default secret tls tls-secondary-credential --key=/tmp/microk8s-secondary.local.key --cert=/tmp/microk8s-secondary.local.crt

# shows both tls secrets
microk8s kubectl get secrets --namespace default

