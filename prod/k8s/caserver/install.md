https://medium.com/@michal.bock/deploy-certificate-authority-service-on-kubernetes-21853c152ade

pushd /home/brent/src/Reporting/prod/k8s/caserver
# set kubectl context
scc.sh reports5.yaml cfssl

#  create sfssl namespace
Don't know if I have to put secrets in the same namespace of if the certmanager can see this namespace.
kubectl apply -f cfssl-namespace.yaml

# create secret for CA certificate
kubectl create secret generic ca-certs --from-file=./certificates/ca/ca.pem --from-file=./certificates/ca/ca-key.pem
kubectl describe secret ca-certs
Name:         ca-certs
Namespace:    cfssl
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
ca-key.pem:  1675 bytes
ca.pem:      1367 bytes

# create secret for authentication key
kubectl create secret generic ca-auth-key --from-literal=auth.key=$(hexdump -n 16 -e '4/4 "%08X" 1 "\n"' /dev/random)
kubectl describe secret ca-auth-key
Name:         ca-auth-key
Namespace:    cfssl
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
auth.key:  32 bytes


https://stackoverflow.com/questions/57398023/using-cfssl-and-multirootca-for-remote-signing-sends-http-instead-of-https

https://github.com/cloudflare/cfssl




