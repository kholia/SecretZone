#!/usr/bin/env python2

# Code written by https://github.com/dfirfpi (https://twitter.com/dfirfpi)
#
# Brute-force stuff added by Dhiru Kholia.

from __future__ import print_function
from Crypto.Cipher import AES, Blowfish
import StringIO
import magic
import sys

CHUNK_SIZE = 4096
HEADER_SIZE = 16384
HEADER_KEY = '\x06\x42\x21\x98\x03\x69\x5E\xB1\x5F\x40\x60\x8C\x2E\x36\x00\x06'

def find_algorithm(header_dec, chunk_enc):
    # AES-128
    for i in range(0x2000, len(header_dec)-16):
        body_decryption_key = header_dec[i:i+16]
        decryptor = AES.new(body_decryption_key, AES.MODE_ECB, 16 * '\00')
        chunk_dec = decryptor.decrypt(chunk_enc)
        r = magic.from_buffer(chunk_dec)
        if "MBR" in r and "NTFS" in r:
            return "AES-128", body_decryption_key, hex(i)

    # AES-256
    for i in range(0x2000, len(header_dec)-32):
        body_decryption_key = header_dec[i:i+32]
        decryptor = AES.new(body_decryption_key, AES.MODE_ECB)
        chunk_dec = decryptor.decrypt(chunk_enc)
        r = magic.from_buffer(chunk_dec)
        if "MBR" in r and "NTFS" in r:
            return "AES-256", body_decryption_key, hex(i)

    # BLOWFISH-448 (not functional yet, header decryption stuff works fine)
    for i in range(0x1000, len(header_dec)-56):
        kl = 56
        body_decryption_key = header_dec[i:i+kl]
        decryptor = Blowfish.new(body_decryption_key, Blowfish.MODE_ECB)
        chunk_dec = decryptor.decrypt(chunk_enc)
        r = magic.from_buffer(chunk_dec)
        if "MBR" in r and "NTFS" in r:
            return "Blowfish", body_decryption_key, hex(i)

    return None


def main():
    if len(sys.argv) < 2:
        print('No input file specified, giving up...')
        sys.exit(0)

    with open(sys.argv[1], 'rb') as input_file:
        header_enc = input_file.read(HEADER_SIZE)
        decryptor = AES.new(HEADER_KEY, AES.MODE_CBC, 16 * '\x00')
        header_dec = decryptor.decrypt(header_enc)
        chunk_enc = input_file.read(CHUNK_SIZE)

        result = find_algorithm(header_dec, chunk_enc)

        if result:
            print(result)
            input_file.seek(HEADER_SIZE, 0)
            algo, body_decryption_key, offet = result

            if "AES" in algo:
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
