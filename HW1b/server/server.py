#-*- coding:utf-8 -*-

import os
import time
import sys
sys.path.append("../")
from socket import *
from cryp.cryptfile import EncryptionFile
from cryp.participant import OneParticipant
from cryp.cryption import AES128
aes128 = AES128()

HOST = ''  #对bind（）方法的标识，表示可以使用任何可用的地址
PORT = 11567  #设置端口
BUFSIZ = 1024  #设置缓存区的大小
ADDR = (HOST, PORT)
cnt = 0
tcpSerSock = socket(AF_INET, SOCK_STREAM)  #定义了一个套接字
tcpSerSock.bind(ADDR)  #绑定地址
tcpSerSock.listen(5)     #规定传入连接请求的最大数，异步的时候适用

q = 0
alpha = 0
mess = (0, 0)
sharekey = 0
key = 0
roundkeys = 0

def str2list(s):
    qc = 0
    alphac = 0
    for i in range(len(s)):
        if s[i] == '(':
            for j in range(i+1, len(s)):
                if s[j] == ',': break
                qc = qc * 10
                qc = int(s[j]) + qc
        if s[i] == ',':
            for j in range(i+2, len(s)):
                if s[j] == ')': break
                alphac = alphac * 10
                alphac = int(s[j]) + alphac
    return qc, alphac


while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('...connected from:', addr)

    ## 协商密钥
    while True:
        mess = tcpCliSock.recv(BUFSIZ)
        q, alpha = str2list(mess.decode())
        Bob = OneParticipant(q, alpha)
        time.sleep(2)
        pubkey_from_alice = tcpCliSock.recv(BUFSIZ)
        pubkey_from_alice = int(pubkey_from_alice.decode())
        print("Alice的公钥为" + str(pubkey_from_alice))
        sharekey = Bob.cal_share_key(pubkey_from_alice)
        tcpCliSock.send(bytes(str(Bob.get_pubkey()), 'utf-8'))
        if sharekey != 0:
            break
    print("共享密钥为" + str(sharekey))
    key = aes128.num_2_16bytes(sharekey)
    roundkeys = aes128.key_expansion(aes128.bytes2num(key))
    print("密钥为" + str(key))
    while True:
        data = tcpCliSock.recv(BUFSIZ)
        print(data)
        ef = EncryptionFile(data.decode("utf-8"), roundkeys)
        ef.encrpt_file()
        paths = "ciphertext"
        print("recv:", paths) # .decode("utf-8")
        if not paths.encode():
            break
        filename = paths # .decode("utf-8")
        if os.path.exists(filename):
            filesize = str(os.path.getsize(filename))
            print("文件大小为：",filesize)
            tcpCliSock.send(filesize.encode())
            data = tcpCliSock.recv(BUFSIZ)   #挂起服务器发送，确保客户端单独收到文件大小数据，避免粘包
            print("开始发送")
            f = open(filename, "rb")
            for line in f:
                tcpCliSock.send(line)
        else:
            tcpCliSock.send("0001".encode())   #如果文件不存在，那么就返回该代码
        cnt += 1
    tcpCliSock.close()
tcpSerSock.close()