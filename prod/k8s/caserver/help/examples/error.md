https://github.com/cloudflare/cfssl/issues/839

 // Sign will only respond for profiles that have no auth provider. 
 // So if all of the profiles require authentication, we return an error. 

 Yeah but - how does one pass the auth_key in the sign call?

You need to use /authsign API endpoint:
cfssl/api/signhandler/signhandler.go

Line 179 in 78c41e6

 func NewAuthHandlerFromSigner(signer signer.Signer) (http.Handler, error) { 
To authenticate you need to compute HMAC for your request and pass it during your API call inside token property as described here: https://github.com/cloudflare/cfssl/blob/master/doc/authentication.txt

Here is how you can calculate HMAC256 (secret is your auth_key, and message is a string that contains JSON message body)

func computeHMAC256(message string, secret string) string {
	s, err := hex.DecodeString(secret)
	if err != nil {
		s = []byte(secret)
	}
	key := s
	h := hmac.New(sha256.New, key)
	h.Write([]byte(message))
	return base64.StdEncoding.EncodeToString(h.Sum(nil))
}


http error with http://localhost:8080/api/v1/cfssl/sign
{"code":7400,"message":"read-only\n"}

https://github.com/cloudflare/cfssl/issues/1178

I did three things to get it "working"

in the config_ca.json file I removed everything from the signing dictionary (this causes cfssl to use default settings in the source code and enables endpoint sign.) following the blog tutorial caused error 5200 invalid or unknown policy.
I made sure the firewall ports were open because it still wasn't issuing certificates
I used localhost instead of a different server name. Using 127.0.0.1 caused an error, I had to use localhost. Now to add settings until I break it again.

i send an answer cause i had the same issue since a long time

i've foud this in the cfssl repo :

https://github.com/cloudflare/cfssl/blob/master/config/testdata/valid_config.json

and if i add

... 
"profiles": {
  "CA": {
    "usages": ["cert sign"],
    "expiry": "720h"
  },
  "email": {
     "usages": ["s/mime"],
     "expiry": "720h"
  }
....
in my config.json

then i have all endpoints working

2022/06/30 15:42:49 [INFO] Initializing signer
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/scan' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/revoke' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/health' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/sign' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/gencrl' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/info' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/scaninfo' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/ocspsign' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/' is enabled
2022/06/30 15:42:49 [INFO] bundler API ready
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/bundle' is enabled
2022/06/30 15:42:49 [INFO] setting up key / CSR generator
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/newkey' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/newcert' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/init_ca' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/certinfo' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/authsign' is enabled
2022/06/30 15:42:49 [INFO] endpoint '/api/v1/cfssl/crl' is enabled
2022/06/30 15:42:49 [INFO] Handler set up complete.
2022/06/30 15:42:49 [INFO] Now listening on 0.0.0.0:8888