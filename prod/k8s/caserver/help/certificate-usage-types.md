certificate usages:
from here [certrificate usages](https://comodosslstore.com/blog/what-is-ssl-tls-client-authentication-how-does-it-work.html#:~:text=SSL%2FTLS%20client%20authentication%2C%20as,ahead%20and%20establishes%20a%20connection)

- server certificates: the client (browser) verifies the identity of the server. Only changed the defaults to increase expiration from 1 year to 5.
DON'T HAVE A USE FOR THESE OTHER USAGES:

What if a server does a client’s verification? Sounds unheard of? Well, it’s a thing. SSL/TLS client authentication works pretty much the same way as SSL server authentication—but in the opposite direction.

In client authentication, a server (website) makes a client generate a keypair for authentication purpose. The private key, the heart of an SSL certificate, is kept with the client instead of the server. It’s stored in the browser. The server confirms the authenticity of the private key and then paves the way for secure communication.

- email verification: from the website https://sectigostore.com/page/what-to-know-about-an-ssl-certificate-for-your-mail-server/ 
"The SSL certificate in your email account serves two purposes – to authenticate the sender’s identity and maintain the integrity of the email. The email certificates are also known as S/MIME or email encryption certificates."



Configure CA options
Now we can configure signing options inside ca-config.json config file. Default options contain following preconfigured fields:

profiles: www with server auth (TLS Web Server Authentication) X509 V3 extension and client with client auth (TLS Web Client Authentication) X509 V3 extension.
expiry: with 8760h default value (or 365 days)
For compliance let’s rename www profile into server, create additional peer profile with both server auth and client auth extensions, and set expiry to 43800h (5 years):

{
    "signing": {
        "default": {
            "expiry": "43800h"
        },
        "profiles": {
            "server": {
                "expiry": "43800h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            },
            "client": {
                "expiry": "43800h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "client auth"
                ]
            },
            "peer": {
                "expiry": "43800h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth",
                    "client auth"
                ]
            }
        }
    }
}

https://www.flatcar.org/docs/latest/setup/security/generate-self-signed-certificates/
client certificate is used to authenticate client by server. For example etcdctl, etcd proxy, or docker clients.
server certificate is used by server and verified by client for server identity. For example docker server or kube-apiserver.
peer certificate is used by etcd cluster members as they communicate with each other in both ways.
