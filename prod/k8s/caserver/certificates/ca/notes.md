config_ca.json
{
  "signing": {
    "default": {
      "auth_key": "key1",
      "expiry": "8760h",
      "usages": [
         "signing",
         "key encipherment",
         "server auth"
       ]
     }
  },
  "auth_keys": {
    "key1": {
      "key": <16 byte hex API key here>,
      "type": "standard"
    }
  }
}