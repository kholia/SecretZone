#!/usr/bin/env python

import hashlib
from Crypto.Cipher import AES
import binascii

f = open("openwall.msr", "rb")
data = f.read(16384)

# hardcoded key and iv
key = "\x06\x42\x21\x98\x03\x69\x5e\xb1\x5f\x40\x60\x8c\x2e\x36\x00\x06"
iv = "\x04\xf2\x60\x00\x50\x42\x75\x7c\x68\x9d\x75\x7c\xff\xff\xff\xff"

decryption_suite = AES.new(key, AES.MODE_CBC, iv)
plain_text = decryption_suite.decrypt(data)
idx = plain_text.index("\x60\x63\x31")
print(idx)
print(plain_text[idx:idx+16].encode("hex"))
# "openwall" is tranformed to the following,
tpassword = "\x60\x63\x31\x8a\xaa\x64\x80\x44\xce\x34\xbb\xf2\x44\xf0\xad\x1d"
