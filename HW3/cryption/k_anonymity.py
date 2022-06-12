'''
thanks to: https://github.com/qiyuangong/Basic_Mondrian

'''

import pdb
import pandas as pd
from datetime import datetime
import time
from decimal import Decimal
class Partition:
    def __init__(self, data, k, up_bound):
        self.dataset = data[:]
        self.low_bound = list(k)
        self.up_bound = list(up_bound)
        self.QI_LEN = 10 ## 准标识符
        self.allow = [1] * self.QI_LEN

    def add(self, records):
        for r in records:
            self.dataset.append(r)

    def __str__(self):
        return "k is " + str(self.low_bound) + "up bound is " + str(self.up_bound)

    def __len__(self):
        return len(self.dataset)
'''
class KDNode():
    def __init__(self):
        self.value = None
        self.left = None
        self.right = None
        self.split = None
        self.feature = None
        self.father = None
'''

class Anonymity(object):
    def __init__(self, QI_LEN):
        self.QI_LEN = 10
        self.GL_K = 0
        self.RESULT = []
        self.QI_RANGE = []
        self.QI_DICT = []
        self.QI_ORDER = []

    def __trans_value(self, x):
        if isinstance(x, (int, float)): return float(x)
        elif isinstance(x, datetime):
            return time.mktime(x.timetuple())
        else: return float(x)

    def get_norm_width(self, partition, index):
        dorder = self.QI_ORDER[index]
        width = self.__trans_value(dorder[partition.up_bound[index]]) - self.__trans_value(dorder[partition.low_bound[index]])
        if width == self.QI_RANGE[index]: return 1
        else: return float(Decimal(width)/Decimal(self.QI_RANGE[index]))

    def choose_dim(self, partition):
        max_width = -1
        max_dim = -1
        for dim in range(self.QI_LEN):
            if partition.allow[dim] == 0: continue
            norm_width = self.get_norm_width(partition, dim)
            if norm_width > max_width:
                max_width = norm_width
                max_dim = dim
        if max_width > 1:
            pdb.set_trace()
        return max_dim

