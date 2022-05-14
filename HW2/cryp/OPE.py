import os
import random
from misc.util import byte2float, float2byte
from cryp.cryption import AES128
import sys
sys.path.append('../')
from decimal import Decimal
'''
任何保序加密方案均不可能达到IND-CPA安全。
'''

'''
A Boldyreva, N Chenette, A Neill. Order-preserving encryption revisited: /
Improved security analysisand alternative solutions[C]. CRYPTO. 2011: 578–595.
一种利用随机保序函数和超几何分布设计的可证安全的OPE算法，根据语义安全的概念定义了OPE算法的理想安全状态
密文域要比明文域大，密的过程就是，将明文在保证顺序的情况下，随机映射到密文域中。
'''


class Node():
    def __init__(self, index, listvalue, listcipher):
        self.leftnode = None
        self.rightnode = None
        self.code = []
        self.father = None
        self.cipher_value = listcipher[index]
        self.plain_value = listvalue[index]

    def insert(self, index, root, listvalue, listcipher):
        if root == None:
            root = Node(index, listvalue, listcipher)

        elif listvalue[index] < root.plain_value:
            root.leftnode = Node(index, listvalue, listcipher)
            root.leftnode.father = root
            root.leftnode.code = root.code
            root.leftnode.code.append(0)

        elif listvalue[index] > root.plain_value:
            root.rightnode = Node(index, listvalue, listcipher)
            root.rightnode.father = root
            root.rightnode.code = root.code
            root.rightnode.code.append(1)
        return root

class mOPE_Tree():
    def __init__(self):
        self.ope_table = []

    def build_ope_tree(self, listvalue, listcipher):
        root = Node(0, listvalue, listcipher)
        for i in range(1000):
            tempnode = root.insert(i, root, listvalue, listcipher)
            self.ope_table.append([tempnode.code, tempnode.cipher_value])
        return root

class simOPE():
    def __init__(self):
        self.key_a = str(self.__key_generator(4))
        self.key_b = str(self.__key_generator(4))
        self.n = str(self.__noise_generator())


    def __key_generator(self, block_size):

        #random_seq = os.urandom(block_size)
        #key = byte2float(bytes(random_seq))
        #while key == 0.0 and key < 100000 and key > -100000:
        #    random_seq = os.urandom(block_size)
        #    key = byte2float(bytes(random_seq))
        return 1000000 * random.random()
        # return base64.b64encode(random_seq)

    def __noise_generator(self):
        return random.randrange(-10,10,1)

    def encryption(self, plain):
        temp = Decimal(str(plain)) * Decimal(self.key_a)
        temp = temp + Decimal(self.key_b) + Decimal(self.n)
        return temp
        # return plain * self.key_a + self.key_b + self.n

    def decryption(self, cipher):
        temp = Decimal(str(cipher)) - Decimal(self.n) - Decimal(self.key_b)
        temp = temp / Decimal(self.key_a)
        return temp
        #return (cipher - self.n - self.key_b) / self.key_a


