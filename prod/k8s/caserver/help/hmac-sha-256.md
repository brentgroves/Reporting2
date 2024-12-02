https://en.wikipedia.org/wiki/HMAC
https://manpages.ubuntu.com/manpages/jammy/man1/hmac256.1.html
sudo apt install libgcrypt20-dev
       This  is  a standalone HMAC-SHA-256 implementation used to compute an HMAC-SHA-256 message
       authentication code.  The tool has originally been developed as  a  second  implementation
       for  Libgcrypt  to  allow  comparing against the primary implementation and to be used for
       internal consistency checks.  It  should  not  be  used  for  sensitive  data  because  no
       mechanisms to clear the stack etc are used.

       The  code  has  been  written in a highly portable manner and requires only a few standard
       definitions to be provided in a config.h file.

       hmac256 is commonly invoked as

      hmac256 "This is my key" help.txt

       This compute the MAC on the file ‘foo.txt’ using the key given on the command line.
 3a5e97748ea77f3438992661cebf7544e2b6ca0b2278f121906ed5a3aa4db855  help.txt      

In cryptography, an HMAC (sometimes expanded as either keyed-hash message authentication code or hash-based message authentication code) is a specific type of message authentication code (MAC) involving a cryptographic hash function and a secret cryptographic key. As with any MAC, it may be used to simultaneously verify both the data integrity and authenticity of a message.

HMAC can provide authentication using a shared secret instead of using digital signatures with asymmetric cryptography. It trades off the need for a complex public key infrastructure by delegating the key exchange to the communicating parties, who are responsible for establishing and using a trusted channel to agree on the key prior to communication.

https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.hmacsha256?view=net-7.0
HMACSHA256 is a type of keyed hash algorithm that is constructed from the SHA-256 hash function and used as a Hash-based Message Authentication Code (HMAC). The HMAC process mixes a secret key with the message data, hashes the result with the hash function, mixes that hash value with the secret key again, and then applies the hash function a second time. The output hash is 256 bits in length.

An HMAC can be used to determine whether a message sent over an insecure channel has been tampered with, provided that the sender and receiver share a secret key. The sender computes the hash value for the original data and sends both the original data and hash value as a single message. The receiver recalculates the hash value on the received message and checks that the computed HMAC matches the transmitted HMAC.

Any change to the data or the hash value results in a mismatch, because knowledge of the secret key is required to change the message and reproduce the correct hash value. Therefore, if the original and computed hash values match, the message is authenticated.

HMACSHA256 accepts keys of any size, and produces a hash sequence 256 bits in length.

