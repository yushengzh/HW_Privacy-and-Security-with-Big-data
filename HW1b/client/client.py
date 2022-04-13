#-*- coding:utf-8 -*-
"""
__author__ = BlingBling
"""
#!/usr/bin/env python

from socket import *
from cryptfile import DecryptionFile
from cryption import AES128
aes128 = AES128()
key = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xe9\xf0'
roundkeys = aes128.key_expansion(aes128.bytes2num(key))

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

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
        f = open("new" + message  ,"wb")
        while received_size < file_total_size:
            data = tcpCliSock.recv(BUFSIZ)
            f.write(data)
            received_size += len(data)
            print("已接收:",received_size)
        f.close()
        df = DecryptionFile("newmessage.txt", roundkeys)
        df.decrypt_file('txt')
        print("receive done",file_total_size," ",received_size)
tcpCliSock.close()