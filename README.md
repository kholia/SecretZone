### Samsung/Seagate (Un)SecretZone

Note: BACKUP YOUR .MSR FILES BEFORE USING THESE SCRIPTS AGAINST THEM.

Use `patch-msr-files.py` to patch your password protected .msr files. After
patching, they will open with password `openwall`. This scripts works for all
encryption algorithms supported by SecretZone, namely AES-128, AES-256, and
BLOWFISH-448.

Use `decrypt-msr-files.py` to decrypt your password protected .msr files
directly, without requiring any password. This script only works for .msr files
which use AES-128 encryption.

Note: Use QEMU to emulate a SecretZone compatible USB external drive.


### Usage

0. Python 2.7.x is required. PyCrypto and `python-magic` libraries are required
   (`pip install --user pycryptodome python-magic`).

1. Patch the original password protected file.

   ```
   $ python patch-msr-files.py blowfish-12345.msr hello-openwall.msr
   ```

2. The patched output file (`hello-openwall.msr`) will now open with password
   `openwall`.


### Notes

If you don't have the initial password for entering the SecretZone GUI,
overwrite your `ui.dat` file with the one included in this repository.

Next login with either of the following credentials,

* admin -> openwall

* user -> 12345

This hack hasn't been tested much.


### Credits

* Francesco Picasso (https://github.com/dfirfpi, @dfirfpi) - AES-128 direct decryption support

* Dhiru Kholia - Password patching method. Support for all supported algorithms.
