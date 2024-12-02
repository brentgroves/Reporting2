# Instructions to setup cfssl on a local system.
I pieced together instructions from the following tutorials:
https://medium.com/@michal.bock/deploy-certificate-authority-service-on-kubernetes-21853c152ade
https://jite.eu/2019/2/6/ca-with-cfssl/
https://jite.eu/2019/2/6/ca-with-cfssl/#adding-your-ca-to-the-computers-certificate-storage
http://www.pkiglobe.org/
https://www.howtoforge.com/tutorial/integration-of-cfssl-with-the-lemur-certificate-manager/
https://www.howtoforge.com/tutorial/integration-of-cfssl-with-the-lemur-certificate-manager/

pushd /home/brent/src/Reporting/prod/k8s/caserver/certificates/ca

# create the root certificate
cfssl gencert -initca ca-csr.json | cfssljson -bare ca -
2023/04/05 16:46:18 [INFO] generating a new CA key and certificate from CSR
2023/04/05 16:46:18 [INFO] generate received request
2023/04/05 16:46:18 [INFO] received CSR
2023/04/05 16:46:18 [INFO] generating key: rsa-2048
2023/04/05 16:46:18 [INFO] encoded CSR
2023/04/05 16:46:18 [INFO] signed certificate with serial number 167520424232095098683353049415478979833012763086

The above command creates a new certificate, a key and a sign request which can be used to cross-sign with other CAs. 

We want to root certificate to not expire or the intermediate certificates signed by it may not be trusted.  I set the expire date for 10 years instead of the default 5 year period.
https://github.com/cloudflare/cfssl/issues/1034

# generate server certificate and private key:
pushd /home/brent/src/Reporting/prod/k8s/caserver/certificates/certs
cfssl gencert -ca=../ca/ca.pem -ca-key=../ca/ca-key.pem -config=../config/config.json -profile=server csr.json | cfssljson -bare reports51
2023/04/07 13:03:01 [INFO] generate received request
2023/04/07 13:03:01 [INFO] received CSR
2023/04/07 13:03:01 [INFO] generating key: rsa-2048
2023/04/07 13:03:01 [INFO] encoded CSR
2023/04/07 13:03:01 [INFO] signed certificate with serial number 285697585922070927416491080960145237296634589026

# bundle the certificate chain
# Have not used this step yet because we don't use intermediate certificates.
pushd /home/brent/src/Reporting/prod/k8s/caserver/certificates/bundles
cfssl bundle -ca-bundle root/root-ca.pem \
  -int-bundle intermediate/intermediate-ca.pem \
  -cert certificates/my-webserver.pem \
| cfssljson -bare my-webserver-fullchain

curl -d '{"domain": "cloudflare.com"}' \
	      ${CFSSL_HOST}/api/v1/cfssl/bundle	 \
	      | python -m json.tool

cfssl bundle -loglevel 0 -cert ../certs/reports51.pem -ca-bundle ../ca/ca.pem | cfssljson -bare reports51-fullchain

cfssl bundle -loglevel 0 -cert ../certs/reports51.pem -ca-bundle ../ca/ca.pem -ca-bundle ../ca/ca.pem | cfssljson -bare reports51-fullchain

cfssl bundle -loglevel 0 -ca-bundle ../ca/ca.pem | cfssljson -bare ca-bun

 
cfssl bundle -cert ../certs/reports51.pem -ca-bundle ../ca/ca.pem \ -flavor ubiquitous > reports51-fullchain
 | cfssljson -bare reports51-fullchain

cfssl bundle -cert reports51.pem [-ca-bundle file] [-int-bundle file] [-int-dir dir] [-metadata file] [-key keyfile] [-flavor optimal|ubiquitous|force] [-password password]

cfssl bundle -cert file [-ca-bundle file] [-int-bundle file] [-int-dir dir] [-metadata file] [-key keyfile] [-flavor optimal|ubiquitous|force] [-password password]

# generate key for config file
hexdump -n 16 -e '4/4 "%08X" 1 "\n"' /dev/random
update ./config/conf-auth.json with the 16 byte hex API key

# choose 1 of the following 2 options to start the CA server
# Option 1: start the server with authentication
pushd /home/brent/src/Reporting/prod/k8s/caserver/certificates/ca
cfssl serve -address=0.0.0.0 -port=8080 -config=../config/config-auth.json -ca=ca.pem -ca-key=ca-key.pem

# Option 2: start the server with no authentication 
pushd /home/brent/src/Reporting/prod/k8s/caserver/certificates/ca
cfssl serve -address=0.0.0.0 -port=8080 -config=../config/config-no-auth.json -ca=ca.pem -ca-key=ca-key.pem

# open a new terminal
pushd /home/brent/src/Reporting/prod/k8s/caserver/certificates/remote

# get certificate containing public key
You can make the following POST request to retrieve the certificate containing the public key of the CA. This will be the content of the ca.pem file.

curl -d '{}' -H "Content-Type: application/json" -X POST localhost:8080/api/v1/cfssl/info
curl -d '{}' -H "Content-Type: application/json" -X POST localhost:8080/api/v1/cfssl/info | python -m json.tool


# Generating TLS Certificates: We do everything but signing the certificate locally.
1. Create the JSON for a CSR request by replacing reports51 with the host name and replace the IP address.
in ./certificates/certs
csr.json
{
  "CN": "reports51",
  "hosts": [
    "127.0.0.1",
    "172.20.88.65",
    "reports51"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
      {
        "C": "US",
        "L": "Avilla",
        "O": "Mobex Global",
        "ST": "Indiana",
        "OU": "MIS department"
      }
  ]
}
2. generate the CSR 
https://github.com/cloudflare/cfssl/wiki/Creating-a-new-CSR
"A CSR is what you give to a Certificate Authority; they'll sign it and give you back a certificate that you install on your webserver. CFSSL can generate both a private key and certificate request." for you
cfssl genkey ../certs/csr.json | cfssljson -bare certificate
This will produce a "certificate.csr" and "certificate-key.pem" file.
If you need to check the information within a Certificate, CSR or Private Key, use these commands.
# Check a Certificate Signing Request (CSR) 
openssl req -text -noout -verify -in certificate.csr
Check a private key openssl rsa -in certificate-key.pem -check
Check a certificate openssl x509 -in certificate.crt -text -noout.


# Option #1 more secure method
https://github.com/cloudflare/cfssl/issues/864
hex_encoded_onboarding_key="F8DACFCC00D330F55740D00C87DA8D39"
cn="reports51"
csr=$(cat "certificate.csr")
sans=""
certificate_req=$(jq -n -c -j \
                    --arg csr  "${csr}" \
                    --arg cn   "${cn}" \
                    --arg sans "${sans}" \
                    '{"certificate_request":($csr+"\n"),"profile":"server","hosts":([ $cn ] + ($sans | split(" ")))}')
base64_certificate_req=$(printf '%s' "${certificate_req}" | base64 | tr -d '\n')
echo base64_certificate_req
base64_token=$(printf '%s' "${certificate_req}" | \
                openssl dgst -sha256 -binary -mac HMAC -macopt "hexkey:${hex_encoded_onboarding_key}" | \
                base64 | tr -d '\n')
auth_req=$(jq -n -c -j \
             --arg token "${base64_token}" \
             --arg req "${base64_certificate_req}" \
             '{"token":$token,"request":$req}')

echo "$auth_req" > authsign_request.json
curl -k -X POST -d @authsign_request.json \
    -H "Content-Type: application/json" \
    "localhost:8080/api/v1/cfssl/authsign" \
    | jq -r '.result.certificate' > server.crt
openssl x509 -in server.crt -text

# Option #2 easier but less secure way to get a certificate signed by the CA you can run the following command.
cfssl gencert -config=../certs/ca-config.json -profile=server -remote=localhost:8080 ../certs/server.json | cfssljson -bare server

2023/04/06 16:45:07 [INFO] generate received request
2023/04/06 16:45:07 [INFO] received CSR
2023/04/06 16:45:07 [INFO] generating key: rsa-2048
2023/04/06 16:45:07 [INFO] encoded CSR


# Check a Certificate 
Check a certificate openssl x509 -in certificate.crt -text -noout

https://blog.cloudflare.com/how-to-build-your-own-public-key-infrastructure/

