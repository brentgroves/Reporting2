Mobex Global's PKI and CA server:
It is made by using CFSSL's Public Key Infrastructure, PKI tools, and its CA server.
https://blog.cloudflare.com/how-to-build-your-own-public-key-infrastructure/
We can use this software for all sorts of things but it is mainly for browsers to verify our web services and secure connections to our database servers.

# choose 1 of the following 2 options to start the CA server
# Option 1: start the server with authentication
pushd /home/brent/src/Reporting/prod/k8s/caserver/certificates/ca
cfssl serve -address=0.0.0.0 -port=8080 -config=../config/config-auth.json -ca=ca.pem -ca-key=ca-key.pem

# Option 2: start the server with no authentication 
pushd /home/brent/src/Reporting/prod/k8s/caserver/certificates/ca
cfssl serve -address=0.0.0.0 -port=8080 -config=../config/config-no-auth.json -ca=ca.pem -ca-key=ca-key.pem


- Generating TLS Certificates: We do everything but signing the certificate locally.
1. Create the JSON for a CSR request by replacing reports51 with the host name and replace the IP address.
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
cfssl genkey csr.json | cfssljson -bare certificate
This will produce a "certificate.csr" and "certificate-key.pem" file.

3. generate a signed certificate using HMAC256:
To ensure certificate are not able to be signed by anyone with access to our HTTPS API CFSSL uses the HMAC256 hash algorithm and a hex API key to verify the CSR's integrity. 

This process can be done with any programming language that has a crypto library.  Here we use bash.  The trick to getting bash to do what you want is to use pipe the output to the input of many smaller standard programs.  The small programs are used in place of writing your own functions that are used in a typical programming language to accomplish the same task.

hex_encoded_onboarding_key="F8DACFCC00D330F55740D00C87DA8D39"
cn="reports51"
csr=$(cat "reports51.csr")
sans=""
certificate_req=$(jq -n -c -j \
                    --arg csr  "${csr}" \
                    --arg cn   "${cn}" \
                    --arg sans "${sans}" \
                    '{"certificate_request":($csr+"\n"),"profile":"server","hosts":([ $cn ] + ($sans | split(" ")))}')
base64_certificate_req=$(printf '%s' "${certificate_req}" | base64 | tr -d '\n')
base64_token=$(printf '%s' "${certificate_req}" | \
                openssl dgst -sha256 -binary -mac HMAC -macopt "hexkey:${hex_encoded_onboarding_key}" | \
                base64 | tr -d '\n')
auth_req=$(jq -n -c -j \
             --arg token "${base64_token}" \
             --arg req "${base64_certificate_req}" \
             '{"token":$token,"request":$req}')

echo "$auth_req" > reports51_authsign_request.json
curl -k -X POST -d @reports51_authsign_request.json \
    -H "Content-Type: application/json" \
    "localhost:8080/api/v1/cfssl/authsign" \
    | jq -r '.result.certificate' > reports51.crt
openssl x509 -in reports51.crt -text
Note: There is a simple way to do this locally but then anyone with access to our HTTPS API would be able to sign a certificate with our root certificate's private key.

4. Install the certificate on your webserver or NGINX ingress controller.

Expire dates: We want our root certificate to not expire any time soon so I set the expire date for 10 years instead of the default 5 year period.

Other uses for the Mobex Global PKI:
	+ Other Key Usages
		+ signing
		+ digital signature
		+ content commitment
		+ key encipherment
		+ key agreement
		+ data encipherment
		+ cert sign
		+ crl sign
		+ encipher only
		+ decipher only
		
	+ More Key Usages
		+ any
		+ server auth
		+ client auth
		+ code signing
		+ email protection
		+ s/mime
		+ ipsec end system
		+ ipsec tunnel
		+ ipsec user
		+ timestamping
		+ ocsp signing
		+ microsoft sgc
		+ netscape sgc


