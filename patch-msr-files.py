#!/usr/bin/env python

import sys
import hashlib
import binascii
from Crypto.Cipher import AES

HEADER_SIZE = 16384
CHUNK_SIZE = 4096

f = open(sys.argv[1], "rb")
data = f.read(HEADER_SIZE)

# hardcoded key and iv
# key_0 = "\xb8\x7e\x60\x08\x53\x42\x75\x65\x43\x18\x75\x25\x3d\x8f\xd9\x41"
key = "\x06\x42\x21\x98\x03\x69\x5e\xb1\x5f\x40\x60\x8c\x2e\x36\x00\x06"
iv = "\x04\xf2\x60\x00\x50\x42\x75\x7c\x68\x9d\x75\x7c\xff\xff\xff\xff"

decryption_suite = AES.new(key, AES.MODE_CBC, iv)
plain_text = decryption_suite.decrypt(data)

replacement_idx = 8228  # password "hash" is stored at this offset

# "openwall" is tranformed to the following,
tpassword = "\x60\x63\x31\x8a\xaa\x64\x80\x44\xce\x34\xbb\xf2\x44\xf0\xad\x1d"
print(plain_text[replacement_idx:replacement_idx+16].encode("hex"))
plain_text = plain_text[0:replacement_idx] + tpassword + plain_text[replacement_idx+len(tpassword):]

encryption_suite = AES.new(key, AES.MODE_CBC, iv)
cipher_text = encryption_suite.encrypt(plain_text)
print(len(cipher_text))

with open(sys.argv[2], 'wb') as output_file:
    output_file.write(cipher_text)
    while True:
        chunk = f.read(CHUNK_SIZE)
        if len(chunk) == 0:
            break
        output_file.write(chunk)
        # sys.stdout.write('.')
        sys.stdout.flush()

f.close()
