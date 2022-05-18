
'''
阶梯一 简易关系型数据的k匿名处理
1. 数据集：成绩数据.xlsx；
2. 采用半自动化方法生成5匿名发布数据；
3. 能够形象展示出5匿名数据发布结果。

阶梯二 智能k匿名处理
1. 数据集： Adult Data Set；
2. 编程自动化程序， 根据输入参数k，自动生成k匿名结果；
3. 能够形象展示出k匿名数据发布结果

阶梯三 数据差分隐私处理
1. 数据集： Adult Data Set；
2. 数据发布内容：平均年龄；
3. 针对阶梯二， 计算数据集内的平均年龄与真实年龄进行对比， 分析k匿名后平均年龄的可用性；
4. 针对数据集的年龄进行差分隐私发布，分析差分隐私后发布的平均年龄的可用性；
5. 尝试在删除某条数据后，k匿名发布的平均年龄、真实发布平均年龄、差分隐私平均年龄对用户隐私信息(年龄) 泄露的可能性


'''
import sys
import os
sys.path.append('./')
from utils.filereader import txt_Reader

filename = "adult.data.txt"
title_column = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
                'marital-status', 'occupation','relationship', 'race', 'sex',
                'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'class']
data = txt_Reader(filename).read_txt('./Adult Data Set/', title_column)
print(data)