[CloudFlare CFSSL](https://www.genome.gov/)
https://blog.cloudflare.com/introducing-cfssl/

![Certificate Bundle](https://blog.cloudflare.com/content/images/image01_4.png)

# add Mobex CA root certificate to trusted store.
https://www.youtube.com/watch?v=7Jr_x7nuRLk
This certificate is stored in our private Azure repository.

# create a csr
replace reports51 with the web sites host name.
enter this into reports51-csr.json
{
  "CN": "reports51",
  "hosts": [
    "reports51"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "Albion",
      "O": "Mobex",
      "OU": "IS department",
      "ST": "Indiana"
    }
  ]
}

# To get a certificate signed by the Mobex CA you can run the following command.
cfssl gencert -config=ca-config.json -profile=kubernetes -remote=localhost:8080 reportsx-csr.json | cfssljson -bare reportsx

# output
2023/04/03 18:46:18 [INFO] generate received request
2023/04/03 18:46:18 [INFO] received CSR
2023/04/03 18:46:18 [INFO] generating key: rsa-2048
2023/04/03 18:46:18 [INFO] encoded CSR
number 57347907406208553038726593824112756880801423637

client certificate: reportsx.pem
private key: reportsx-key.pem
encoded csr: reportsx.csr

# verify certificate using the ASN website or with the openssl cli:
- https://lapo.it/asn1js/
- openssl x509 -in reportsx.pem -text

# verify issurer
Issuer: C = US, ST = Indiana, L = Albion, O = Mobex, OU = IT department, CN = mobexglobal.local
# verify subject
Subject: C = US, ST = Indiana, L = Albion, O = Mobex, OU = IS department, CN = reports51
# verify valid date range
Not Before: Apr  3 21:35:00 2023 GMT
Not After : Apr  2 21:35:00 2024 GMT


https://www.youtube.com/watch?v=jsD_lAE8Odg
https://medium.com/@michal.bock/deploy-certificate-authority-service-on-kubernetes-21853c152ade

cfssl gencert -remote="localhost:8888" -config ca-config.json -profile kubernetes admin-csr.json | cfssljson -bare admin2