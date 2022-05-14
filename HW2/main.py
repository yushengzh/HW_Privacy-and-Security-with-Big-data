
'''
exp2: 数据安全检索
阶梯一：线序数据安全检索
    1.一维乱序数据，自生成数据集
    2.采用任一种保序加密方法加密
    3.可在一维密文上进行范围查询
阶梯二：空间数据安全范围检索
    1.二维乱序数据
    2.采用任一种保序加密方法加密
    3.构建恰当的索引结构，如KD树等
    4.可在二维数据上进行安全范围查询

阶梯三：空间数据安全（近似）近邻检索
    1.二维乱序数据(y)
    2.采用任一种保序加密方法加密
    3.构建恰当的索引结构，如KD树等(y)
    4.可在二维数据上进行安全（近似）近邻查询(y)

'''
import sys
sys.path.append('./')

from misc.readfile import Readfile
from misc.KDTree import KDTree
from misc.KNN_base import KNeighborsBase
import misc.util as util
from misc.KNN import K_Nearest_Neighbor
from misc.util import get_eu_dist
import time

rf = Readfile('NE.txt')
txt = rf.read_txt('./')
runtime = 0
y = []
y1 = []
z = []
z1 = []
crypto_y = []
crypto_z = []
# key = 0x0f0e0d0c0b0a090807060504030201ef
# aes128 = AES128()
# roundkeys = aes128.key_expansion(key)
for pair in txt:
    y.append(util.float2byte(float(pair[0])))
    y1.append(pair[0])
    z1.append(pair[1])
    #cipher = aes128.encryption(aes128.bytes2num(util.float2byte(float(pair[0]))), roundkeys)
    #crypto_y.append(cipher)
    z.append(util.float2byte(float(pair[1])))


# openT = mOPE_Tree()
# openT.build_ope_tree(y, crypto_y)
# print(openT.ope_table)
# print(crypto_y)
'''
simope = simOPE()
key_a, key_b = simope.key_a, simope.key_b
cipher = []
print(key_a, key_b,simope.n)
for i in range(len(y)):
    cipher.append([float(simope.encryption(y1[i])), float(simope.encryption(z1[i]))])
   
    #cipher = aes128.encryption(aes128.bytes2num(i), roundkeys)
    #print("密文：" + str(cipher))
    #plain = aes128.decryption(cipher, roundkeys)
    #numcipher = aes128.bytes2num(cipher)
    #print("明文是" + str(numcipher))
    #print(util.byte2float(plain[-4:]))

print(cipher)
plain = []
for pair in cipher:
    plain.append([round(float(simope.decryption(pair[0])), 6), round(float(simope.decryption(pair[1])), 6)])
print(plain)
print(txt)

plt.figure(figsize=[4, 3], dpi=800)
for pair in txt:
    cnt += 1
    plt.scatter(pair[0], pair[1])
    if cnt == 50: break;
plt.show()
'''


#t1 = KDTree()
#t1.build_tree(txt, z1)
# ['0.424582', '0.410366']
x = input("请输入查询x:")
y = input("请输入近似查询y:")

'''
model = K_Nearest_Neighbor()
model.fit(txt, z1, k)
'''
# pairs_plain = t1.nearest_neighbour_search(['0.431621', '0.431546'])
# print(res)


# Xi = [0.309170, 0.418650]
Xi = [float(x), float(y)]
k = input("请输入近似查询k值:")
model = KNeighborsBase()
model.fit(txt, y1, int(k))

heap = model._knn_search(Xi)
ret1 = [get_eu_dist(Xi, nd.split[0]) for nd in heap.items]




