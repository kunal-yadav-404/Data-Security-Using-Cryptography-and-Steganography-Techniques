from Crypto import Random
from Crypto.Cipher import AES
import os
import hashlib


class Crypt:
    def __init__(self, key = ""):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        self.key = hashlib.shake_128(input(f"Set password for [{file_name}]: ").encode("utf-8")).hexdigest(16)
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        newF = file_name + ".enc"
        with open(newF, 'wb') as fo:
            fo.write(enc)
        print("\nFile Encrypted!")
        return newF

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        self.key = hashlib.shake_128(input("File password: ").encode("utf-8")).hexdigest(16)
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        op_file = file_name[:-4]
        with open(op_file, 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)
        print("File fully Decrypted!!!")
        print(f"Output available at: {op_file}")

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                dirs.append(dirName + "/" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)
