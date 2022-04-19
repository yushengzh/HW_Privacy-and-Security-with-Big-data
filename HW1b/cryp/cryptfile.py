'''
1、对原文件加密，返回加密文件
2、对加密文件解密，返回解密文件
'''

import os
import sys
sys.path.append('./')
from cryp.cryption import AES128

class EncryptionFile:
    def __init__(self, filepath, roundkeys):
        self.filepath = filepath
        self.cipherbuffer = []
        self.roundkeys = roundkeys

    def encrpt_file(self):
        path = self.filepath
        aes128 = AES128()
        with open(path, "rb") as file:
            while True:
                _16byte_block = file.read(16)
                if _16byte_block == b'': break
                cipherblock = aes128.encryption(aes128.bytes2num(_16byte_block), self.roundkeys)
                self.cipherbuffer.append(cipherblock)
            file.close()

        encrypt_filepath = "ciphertext"
        if not os.path.exists(encrypt_filepath):
            file = open(encrypt_filepath, 'w')
        with open(encrypt_filepath, "rb+") as file:
            for block in self.cipherbuffer:
                file.write(bytes(block))
            file.close()

class DecryptionFile:
    def __init__(self, filepath, roundkeys):
        self.filepath = filepath # 加密文件路径
        self.plainbuffer = []
        self.roundkeys = roundkeys

    def decrypt_file(self, format): # format 文件格式
        path = self.filepath # 加密文件路径
        aes128 = AES128()
        with open(path, "rb") as file:
            while True:
                _16byte_block = file.read(16)
                if _16byte_block == b'': break
                plainblock = aes128.decryption(_16byte_block, self.roundkeys)
                plainblock = bytes(plainblock)
                self.plainbuffer.append(plainblock.decode())
            file.close()

        decrypt_filepath =  "decrypt." + format
        if not os.path.exists(decrypt_filepath):
            file = open(decrypt_filepath, 'w')

        with open(decrypt_filepath, "wt") as file:
            for i in self.plainbuffer:
                i = i.replace('\0', '')
                file.write(i)
            file.close()

