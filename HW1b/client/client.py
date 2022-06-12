#-*- coding:utf-8 -*-
#!/usr/bin/env python

from socket import *
import time
import sys
sys.path.append("../")
from cryp.cryptfile import DecryptionFile
from cryp.generateprime import PrimeGenerator
from cryp.participant import OneParticipant
from cryp.cryption import AES128
generator = PrimeGenerator(20)
q, alpha = generator.generate_large_prime()
Alice = OneParticipant(q, alpha)
aes128 = AES128()

key = 0
roundkeys = 0

HOST = 'localhost' # 127.0.0.1
PORT = 11567
BUFSIZ = 1024
ADDR = (HOST, PORT)


tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

'''协商密钥'''
sharekey = 0
key = 0
roundkeys = 0
while True:
    mess = (q, alpha)
    tcpCliSock.send(bytes(str((q, alpha)), 'utf-8'))
    time.sleep(2)
    tcpCliSock.send(bytes(str(Alice.get_pubkey()), 'utf-8'))
    time.sleep(2)
    pubkey_from_bob = tcpCliSock.recv(BUFSIZ)
    pubkey_from_bob = int(pubkey_from_bob.decode())
    print("Bob的公钥为" + str(pubkey_from_bob))
    sharekey = Alice.cal_share_key(pubkey_from_bob)
    if sharekey != 0:
        break
print("共享密钥为" + str(sharekey))
key = aes128.num_2_16bytes(sharekey)
roundkeys = aes128.key_expansion(aes128.bytes2num(key))
print("密钥为" + str(key))
while True:
    message = input('> ')
    if not message:
        break
    tcpCliSock.send(bytes(message, 'utf-8'))
    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    if data.decode() == "0001":
        print("Sorr file %s not found"%message)
    else:
        tcpCliSock.send("File size received".encode())
        file_total_size = int(data.decode())
        received_size = 0
        filepath = "new" + message
        f = open("new" + message  , "wb")
        while received_size < file_total_size:
            data = tcpCliSock.recv(BUFSIZ)
            f.write(data)
            received_size += len(data)
            print("已接收:", received_size)
        f.close()
        df = DecryptionFile("newmessage.txt", roundkeys)
        df.decrypt_file('txt')
        print("receive done", file_total_size, " ", received_size)
tcpCliSock.close()