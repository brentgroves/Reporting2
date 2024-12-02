https://www.flatcar.org/docs/latest/setup/security/generate-self-signed-certificates/#configure-ca-options

# certificate usages:
from here [certrificate usages](https://comodosslstore.com/blog/what-is-ssl-tls-client-authentication-how-does-it-work.html#:~:text=SSL%2FTLS%20client%20authentication%2C%20as,ahead%20and%20establishes%20a%20connection)

- server verification: the client (browser) verifies the identity of the server.  Only changed the defaults to increase expiration from 1 year to 5.
DON'T HAVE A USE FOR THESE OTHER USAGES:
- client verification: a server (website) makes a client generate a keypair for authentication purpose. Used when even greater security is needed than server verification. One use of client verification is when each IOT device is issued a certificate
- peer verification: when secure two way communication is needed between clients not for websites.
- email verification: from the website https://sectigostore.com/page/what-to-know-about-an-ssl-certificate-for-your-mail-server/ 
"The SSL certificate in your email account serves two purposes – to authenticate the sender’s identity and maintain the integrity of the email. The email certificates are also known as S/MIME or email encryption certificates."

# Need server verification only

Configure CA options
Now we can configure signing options inside the config-default.json config file. Default options contain following preconfigured fields:

profiles: www with server auth (TLS Web Server Authentication) X509 V3 extension and client with client auth (TLS Web Client Authentication) X509 V3 extension.
expiry: with 8760h default value (or 365 days)

