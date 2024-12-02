
# start the server on the port 8080.
pushd /home/brent/src/Reporting/prod/k8s/caserver/certificates/ca
cfssl serve -address=0.0.0.0 -port=8080 -config=../certs/ca-config.json -ca=./ca.pem -ca-key=./ca-key.pem

# open a new terminal
pushd /home/brent/src/Reporting/prod/k8s/caserver/certificates/test

# get certificate containing public key
You can make the following POST request to retrieve the certificate containing the public key of the CA. This will be the content of the ca.pem file.

curl -d '{}' -H "Content-Type: application/json" -X POST localhost:8080/api/v1/cfssl/info

# To get a certificate signed by the CA you can run the following command.
cfssl gencert -config=../certs/ca-config.json -profile=server -remote=localhost:8080 ../certs/server.json | cfssljson -bare server
