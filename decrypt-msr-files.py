#!/usr/bin/env python2

# Code written by https://github.com/dfirfpi (https://twitter.com/dfirfpi)

from __future__ import print_function
from Crypto.Cipher import AES
import sys

CHUNK_SIZE = 4096
HEADER_SIZE = 16384
# AES key, for different crypto algorithms, different keys.
HEADER_KEY = '\x06\x42\x21\x98\x03\x69\x5E\xB1\x5F\x40\x60\x8C\x2E\x36\x00\x06'

def main():
    if len(sys.argv) != 3:
        print('No output file specified, giving up...')
        sys.exit(0)

    with open(sys.argv[1], 'rb') as input_file:
        header_enc = input_file.read(HEADER_SIZE)
        decryptor = AES.new(HEADER_KEY, AES.MODE_CBC, 16 * '\x00')
        header_dec = decryptor.decrypt(header_enc)
        body_decryption_key = header_dec[0x203c:0x204C]
        print('Decoding key: {}'.format(body_decryption_key.encode('hex')))

        decryptor = AES.new(body_decryption_key, AES.MODE_ECB, 16 * '\00')

        with open(sys.argv[2], 'wb') as output_file:
            while True:
                chunk_enc = input_file.read(CHUNK_SIZE)
                if len(chunk_enc) == 0:
                    break
                chunk_dec = decryptor.decrypt(chunk_enc)
                output_file.write(chunk_dec)
                sys.stdout.write('.')
                sys.stdout.flush()

if __name__ == "__main__":
    main()
