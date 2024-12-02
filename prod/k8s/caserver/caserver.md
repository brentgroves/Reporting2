https://github.com/cloudflare/cfssl/tree/master/doc
Summary:
I'm not sure which tutorial to follow:

https://www.flatcar.org/docs/latest/setup/security/generate-self-signed-certificates/#configure-ca-options
Flatcar has good explanations about concepts I was unfamiliar with.

https://blog.cloudflare.com/introducing-cfssl/
cloudflare's blog does not have much details.

https://github.com/kelseyhightower/kubernetes-the-hard-way/blob/master/docs/04-certificate-authority.md
Kubernetes the hardway is good but it does not add hostnames to the CSR.


https://medium.com/@michal.bock/deploy-certificate-authority-service-on-kubernetes-21853c152ade
Deploy Certificate Authority Service on Kubernetes
Seems to do exactly what I want but the ca csr does not have very much info in it.

The take away from kubernetes the hard way is:
cfssl print-defaults config 
{
    "signing": {
        "default": {
            "expiry": "168h"
        },
        "profiles": {
            "www": {
                "expiry": "8760h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            },
            "client": {
                "expiry": "8760h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "client auth"
                ]
            }
        }
    }
}

and cfssl print-defaults csr
{
    "CN": "example.net",
    "hosts": [
        "example.net",
        "www.example.net"
    ],
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "ST": "CA",
            "L": "San Francisco"
        }
    ]
}

pushd /home/brent/src/Reporting/prod/k8s/caserver/configuration
# create the root certificate
cfssl gencert -initca ca-csr-mobex.json | cfssljson -bare ca -
2023/04/04 15:33:51 [INFO] generating a new CA key and certificate from CSR
2023/04/04 15:33:51 [INFO] generate received request
2023/04/04 15:33:51 [INFO] received CSR
2023/04/04 15:33:51 [INFO] generating key: rsa-2048
2023/04/04 15:33:51 [INFO] encoded CSR
2023/04/04 15:33:51 [INFO] signed certificate with serial number 441518663624597751657658829490826552362431845261

You’ll get following files:

ca-key.pem
ca.csr
ca.pem
Please keep ca-key.pem file in safe. This key allows to create any kind of certificates within your CA.
*.csr files are not used in our example.

# generate a server certificate
Generate server certificate
cfssl print-defaults csr > server.json
Most important values for server certificate are Common Name (CN) and hosts. We have to substitute them, for example:

...
    "CN": "coreos1",
    "hosts": [
        "192.168.122.68",
        "ext.example.com",
        "coreos1.local",
        "coreos1"
    ],
...
# generate server certificate and private key:
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config-mobex.json -profile=server server-mobex.json | cfssljson -bare server


pushd /home/brent/src/Reporting/prod/k8s/caserver/configuration
# start the server on the port 8080.
cfssl serve -address=0.0.0.0 -port=8080 -config=ca-config-mobex.json -ca=ca.pem -ca-key=ca-key.pem

# open a new terminal
pushd /home/brent/src/Reporting/prod/k8s/caserver/configuration/test

# get certificate containing public key
You can make the following POST request to retrieve the certificate containing the public key of the CA. This will be the content of the ca.pem file.

curl -d '{}' -H "Content-Type: application/json" -X POST localhost:8080/api/v1/cfssl/info

# To get a certificate signed by the CA you can run the following command.
cfssl gencert -config=ca-config-mobex.json -profile=server -remote=localhost:8080 server-mobex.json | cfssljson -bare server

2023/04/04 16:16:03 [INFO] generate received request
2023/04/04 16:16:03 [INFO] received CSR
2023/04/04 16:16:03 [INFO] generating key: rsa-2048
2023/04/04 16:16:04 [INFO] encoded CSR

https://github.com/cloudflare/cfssl/tree/master/doc

https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
https://github.com/cloudflare/cfssl/blob/master/doc/cmd/cfssl.txt

# start here
https://medium.com/@michal.bock/deploy-certificate-authority-service-on-kubernetes-21853c152ade
https://github.com/SpeedyCoder/kubernetes-manifests/tree/master/certificate-authority
To create the secrets used in the manifests you can run the following commands.

pushd /home/brent/src/Reporting/prod/k8s/caserver/configuration
scc.sh reports5.yaml microk8s 
kubectl create secret generic ca-certs --from-file=ca.pem --from-file=ca-key.pem
kubectl describe secret ca-certs
Name:         ca-certs
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
ca-key.pem:  1679 bytes
ca.pem:      1391 bytes

kubectl create secret generic ca-auth-key --from-literal=auth.key=$(hexdump -n 16 -e '4/4 "%08X" 1 "\n"' /dev/random)
kubectl describe secret ca-auth-key
Name:         ca-auth-key
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
auth.key:  32 bytes