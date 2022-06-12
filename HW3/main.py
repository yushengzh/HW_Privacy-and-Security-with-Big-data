
'''
阶梯一 简易关系型数据的k匿名处理
1. 数据集：成绩数据.xlsx；
2. 采用半自动化方法生成5匿名发布数据；
3. 能够形象展示出5匿名数据发布结果。

阶梯二 智能k匿名处理
1. 数据集： Adult Data Set；
2. 编程自动化程序， 根据输入参数k，自动生成k匿名结果；(y)
3. 能够形象展示出k匿名数据发布结果(y)

阶梯三 数据差分隐私处理
1. 数据集： Adult Data Set；
2. 数据发布内容：平均年龄；(y)
3. 针对阶梯二， 计算数据集内的平均年龄与真实年龄进行对比， 分析k匿名后平均年龄的可用性；(y)
4. 针对数据集的年龄进行差分隐私发布，分析差分隐私后发布的平均年龄的可用性；(y)
5. 尝试在删除某条数据后，k匿名发布的平均年龄、真实发布平均年龄、差分隐私平均年龄对用户隐私信息(年龄) 泄露的可能性(y)
'''

import sys
import utils
sys.path.append('./')
from decimal import Decimal
from utils import preprocess, txt_Reader
# from anonymity.datafly import *
# from anonymity.samarati import *
from anonymity.k_anonymity import *
from anonymity.mondrian import *
filename = "adult.data.txt"
title_column = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
                'marital-status', 'occupation', 'relationship', 'race', 'sex',
                'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'class']
QI_list = ['age', 'sex', 'race']
data = txt_Reader(filename).read_txt('./Adult Data Set/', title_column)
data.sort_values(by='age', ascending=True, inplace=True)
rawlen = len(data)
preprocess(data)
print("原有数据有{}行; 清洗后的数据有{}行".format(rawlen, len(data)))
raw_data_list = df2list(data)
pre_ages = [int(item[0]) for item in raw_data_list]
avg_pre_ages = sum(pre_ages) / len(raw_data_list)
k = int(input("需要匿名化的k为"))

'''
ka = KAnonymity(raw_data_list, k=k)
ka.anonymize()

# for column in data:
#    print(column)
'''
DATA, order = utils.read_data()
# print(order)
res, b = mondrian(DATA, k, False)
res = utils.covert_to_raw(res, order)
post_ages = [item[0] for item in res]
avg_post_ages = cal_post_ages(post_ages)
write_result(res, k)
print("原数据的平均年龄为: %f" %avg_pre_ages)
print("%d-匿名后的平均年龄为:"%k, avg_post_ages)

dp_ages = diff_privacy_add_laplace_noise(pre_ages, 0, 1)
avg_dp_ages = avg_ages(dp_ages)
print("差分隐私后的平均年龄为: %f" %avg_dp_ages)


# 尝试在删除某条数据后，k匿名发布的平均年龄、真实发布平均年龄、差分隐私平均年龄对用户隐私信息(年龄) 泄露的可能性

idx = random.randint(0, len(pre_ages))
co_pre_ages = copy.deepcopy(pre_ages)
co_post_ages = copy.deepcopy(post_ages)
co_dp_ages = copy.deepcopy(dp_ages)

co_pre_ages.pop(idx)
co_post_ages.pop(idx)
co_dp_ages = diff_privacy_add_laplace_noise(co_pre_ages, 0, 1)

print("========================================推断攻击========================================")
print("删除的数据为", pre_ages[idx])
avg_pre = avg_ages(co_pre_ages)
avg_post = cal_post_ages(co_post_ages)
avg_dp = avg_ages(co_dp_ages)
print("平均年龄分别为原数据{}、k-匿名后数据{}、差分隐私后数据{}".format(avg_pre, avg_post, avg_dp))
print("敏感度:", avg_pre_ages - (avg_pre_ages *len(pre_ages) - pre_ages[idx])/len(pre_ages))

val_pre = avg_pre_ages * (len(co_pre_ages) + 1) - avg_pre * len(co_pre_ages)
val_post = avg_post_ages * (len(co_post_ages) + 1) - avg_post * len(co_post_ages)
val_dp = avg_dp_ages * (len(co_dp_ages) + 1) - avg_dp * len(co_dp_ages)
print("随机删除的用户隐私信息(年龄)分别为:原数据推断年龄{}、k-匿名后数据推断年龄{}、差分隐私后数据推断年龄{}".format(val_pre, val_post, val_dp))
