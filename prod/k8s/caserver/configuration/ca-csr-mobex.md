https://www.flatcar.org/docs/latest/setup/security/generate-self-signed-certificates/#configure-ca-options

You can also modify ca-csr.json Certificate Signing Request (CSR):

{
    "CN": "My own CA",
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "US",
            "L": "CA",
            "O": "My Company Name",
            "ST": "San Francisco",
            "OU": "Org Unit 1",
            "OU": "Org Unit 2"
        }
    ]
}
And generate CA with defined options:

cfssl gencert -initca ca-csr.json | cfssljson -bare ca -
You’ll get following files:

ca-key.pem
ca.csr
ca.pem
Please keep ca-key.pem file in safe. This key allows to create any kind of certificates within your CA.
*.csr files are not used in our example.

