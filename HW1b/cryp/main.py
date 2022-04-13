# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

'''
对称密码技术
1. 任选DES/AES/SM4中的一种对称密码算法并实现；(y)
2. 针对多模式对称密码算法，仅需实现一种模式；(y) [ECB 最简单的密码本模式]
3. 能够对字符串进行正确的加密和解密。(y)

密钥协商技术
1. 模拟实现DH密钥交换协议；(y)
2. 基于大素数进行算法实现；(y)
3. 通过DH密钥协商协议生成会话密钥；(y)
4. 利用会话密钥对字符串进行正确的加密和解密；(y)
5. 相同内容每次发送的密文不同。(y)

远程文件安全传输
1. 真实网络环境实现任意类型文件的远程传输；(y)
2. 网络传输采用Socket或SSL，二选一；(y,Socket)
3. 支持任意类型的文件；(^ binary thus y)
4. 能够实现文件的正确加解密；(y)
5. 相同文件每次发送的加密文件不同(diff roundkeys diff encrypted file)
'''

from generateprime import PrimeGenerator
from participant import OneParticipant
from cryption import AES128
from cryptfile import DecryptionFile
from cryptfile import EncryptionFile

## 阶梯 1 & 2
generator = PrimeGenerator(20)
q, alpha = generator.generate_large_prime()
Alice = OneParticipant(q, alpha)
Bob = OneParticipant(q, alpha)
aes128 = AES128()

print("Alice的公钥：" + str(Alice.get_pubkey()) + "\nBob的公钥：" + str(Bob.get_pubkey()))
skey_fromA = Alice.cal_share_key(Bob.get_pubkey())
skey_fromB = Bob.cal_share_key(Alice.get_pubkey())
if skey_fromA == skey_fromB:
    print("Alice和Bob的会话密钥一致！为：" + str(skey_fromA))
key = aes128.num_2_16bytes(skey_fromA)

print("共享密钥是：" + str(key))
roundkeys = aes128.key_expansion(aes128.bytes2num(key))

plaintext = 0x0f0e0d0c0b0a09080706050403020100
print("\n输入明文:" + str(list(aes128.num_2_16bytes(plaintext))) + "\n")
ciphertext = aes128.encryption(plaintext, roundkeys)

print("\n加密结果：" + str(ciphertext) + "\n")
out = aes128.decryption(ciphertext, roundkeys)
print("\n解密结果:" + str(out) + "\n")


print("==============test cryptfile=================")
ef = EncryptionFile("../server/message.txt", roundkeys)
df = DecryptionFile("ciphertext", roundkeys)
ef.encrpt_file()
df.decrypt_file('txt')

