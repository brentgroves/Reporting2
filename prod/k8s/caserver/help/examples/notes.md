https://blog.cloudflare.com/how-to-build-your-own-public-key-infrastructure/

With these two configuration files set, you can create your certificate.
$ cfssl gencert -config config_client.json csr_client.json | cfssljson -bare db

This results in three files:

db-key.pem: your private key
db.pem: your certificate
db.csr: your CSR