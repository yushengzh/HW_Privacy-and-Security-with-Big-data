import pandas as pd
import numpy as np
from datetime import datetime
import time
import random
import copy
from sklearn import preprocessing

AGE_CONF = './hierarchy/age_hierarchy.txt'
WORKCLASS_CONF = './hierarchy/workclass_hierarchy.txt'
EDU_CONF = './hierarchy/education_hierarchy.txt'
EDUNUM_CONF = './hierarchy/edunum_hierarchy.txt'
MARITAL_CONF = './hierarchy/martial_hierarchy.txt'
RELATIONSHIP_CONF = './hierarchy/relationship_hierarchy.txt'
RACE_CONF = './hierarchy/race_hierarchy.txt'
SEX_CONF = './hierarchy/sex_hierarchy.txt'
HPW_CONF = './hierarchy/hours_per_week_hierarchy.txt'
COUNTRY_CONF = './hierarchy/country_hierarchy.txt'

title_column = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
                'marital-status', 'occupation', 'relationship', 'race', 'sex',
                'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'class']

QI_INDEX = [0, 1, 4, 5, 6, 8, 9, 13]
IS_CAT = [False, True, False, True, True, True, True, True]
SA_INDEX = -1
__DEBUG = False
INTUITIVE_ORDER = None


def preprocess(load_data: pd.DataFrame):
    """
    :param load_data: Raw Data
    :return: Cleaned Data(replace "?" with nan, then drop them all)
    """
    load_data.replace(' ?', np.nan, inplace=True)
    load_data.dropna(axis=0, how='any', inplace=True)

def read_data():

    QI_num = len(QI_INDEX)
    data = []
    intuitive_dict = []
    intuitive_order = []
    intuitive_number = []
    for i in range(QI_num):
        intuitive_dict.append(dict())
        intuitive_number.append(0)
        intuitive_order.append(list())
    data_file = open('Adult Data Set/adult.data.txt', 'rU')
    for line in data_file:
        line = line.strip()
        # remove empty and incomplete lines
        # only 30162 records will be kept
        if len(line) == 0 or '?' in line:
            continue
        # remove double spaces
        line = line.replace(' ', '')
        temp = line.split(',')
        ltemp = []
        for i in range(QI_num):
            index = QI_INDEX[i]
            if IS_CAT[i]:
                try:
                    ltemp.append(intuitive_dict[i][temp[index]])
                except KeyError:
                    intuitive_dict[i][temp[index]] = intuitive_number[i]
                    ltemp.append(intuitive_number[i])
                    intuitive_number[i] += 1
                    intuitive_order[i].append(temp[index])
            else:
                ltemp.append(int(temp[index]))
        ltemp.append(temp[SA_INDEX])
        data.append(ltemp)
    return data, intuitive_order



class txt_Reader():
    def __init__(self, filename):
        self.filename = filename

    def read_txt(self, path: str, title_column: list) -> pd.DataFrame:
        filepath = path + self.filename
        txtlist = []
        with open(filepath, encoding='gbk') as f:
            for line in f:
                txtlist.append(line.strip().split(","))
            f.close()
        return pd.DataFrame(txtlist, columns=title_column)

class xlsx_Reader():
    def __init__(self, filename):
        self.filename = filename

    def read_xlsx(self, path: str) -> pd.DataFrame:
        filepath = path + self.filename
        return pd.read_excel(filepath)


def write_result(result, k):
    with open("res/adult_%d_kanonymity.data" %k, "w") as f:
        for line in result:
            f.write(','.join(line) + '\n')


def df2list(df: pd.DataFrame) -> list:
    data_array = np.array(df)
    new_data_array = []
    for item in data_array:
        line = []
        for i in item:
            line.append(i.strip())
        new_data_array.append(line)
    return new_data_array
    #return data_array.tolist()


def generate_categorical_loss_metric_map(leaves_num, hierarchies):
    loss_metric_map = {attr: {} for attr in hierarchies.keys()}
    print('\nleaves_num:\n', leaves_num)
    for attr, vals in hierarchies.items():
        loss_metric_map[attr]['*'] = 1
        for v in vals:
            if v in leaves_num[attr].keys():
                loss_metric_map[attr][v] = (leaves_num[attr][v] - 1) / (leaves_num[attr]['*'] - 1)
            else:
                loss_metric_map[attr][v] = 0
    return loss_metric_map


def categorical_loss_metric(qi_columns, leaves_num, hierarchies, sup):
    loss_metric_map = generate_categorical_loss_metric_map(leaves_num, hierarchies)
    print('\nloss_metric_map:\n', loss_metric_map)
    loss_metric = 0

    for attr in qi_columns:
        col = qi_columns[attr].tolist()
        # the loss for an attribute is the AVERAGE of the loss for all tuples
        # the loss for the entire data set is the SUM of the losses for each attribute
        sum_attr_lm = sum([loss_metric_map[attr][str(v)] for v in col])
        loss_metric += (sum_attr_lm + sup) / (len(col) + sup)
    return loss_metric


def compute_numerical_loss_metric(column):
    loss = 0
    # initialize lowest and highest values
    if not isinstance(column[0], int):  # string value, e.g., '35-40'
        current_range = [int(i) for i in list(column[0].replace(' ', '').split('-'))]
        lowest, highest = current_range[0], current_range[1]
    else:  # integer value, e.g., 37
        lowest, highest = column[0], column[0]

    # iterate through column
    for v in column:
        if not isinstance(v, int):  # extract range from table content (string, e.g., '35-40')
            current_range = [int(i) for i in list(v.replace(' ', '').split('-'))]
            loss += current_range[1] - current_range[0]
            # update lowest & highest
            lowest = min(lowest, current_range[0])
            highest = max(highest, current_range[1])
        else:  # integer value, loss is 0 here
            lowest = min(lowest, v)
            highest = max(highest, v)

    max_range = highest - lowest
    return loss / (max_range * len(column))  # average


def numerical_loss_metric(qi_columns):
    loss_metric = 0
    for attr in qi_columns:
        col = qi_columns[attr].tolist()
        # the loss for the entire data set is the SUM of the losses for each attribute
        loss_metric += compute_numerical_loss_metric(col)
    return loss_metric

def cmp(x, y):
    if x > y:
        return 1
    elif x==y:
        return 0
    else:
        return -1


def cmp_str(element1, element2):
    """
    compare number in str format correctley
    """
    try:
        return cmp(int(element1), int(element2))
    except ValueError:
        return cmp(element1, element2)

def cmp_value(element1, element2):
    if isinstance(element1, str):
        return cmp_str(element1, element2)
    else:
        return cmp(element1, element2)


def value(x):
    '''Return the numeric type that supports addition and subtraction'''
    if isinstance(x, (int, float)):
        return float(x)
    elif isinstance(x, datetime):
        return time.mktime(x.timetuple())
        # return x.timestamp() # not supported by python 2.7
    else:
        try:
            return float(x)
        except Exception as e:
            return x


def merge_qi_value(x_left, x_right, connect_str='~'):
    '''Connect the interval boundary value as a generalized interval and return the result as a string
    return:
        result:string
    '''
    if isinstance(x_left, (int, float)):
        if x_left == x_right:
            result = '%d' % (x_left)
        else:
            result = '%d%s%d' % (x_left, connect_str, x_right)
    elif isinstance(x_left, str):
        if x_left == x_right:
            result = x_left
        else:
            result = x_left + connect_str + x_right
    elif isinstance(x_left, datetime):
        # Generalize the datetime type value
        begin_date = x_left.strftime("%Y-%m-%d %H:%M:%S")
        end_date = x_right.strftime("%Y-%m-%d %H:%M:%S")
        result = begin_date + connect_str + end_date
    return result




def write_to_file(result, k):

    with open("res/adult_%d_kanonymity.data" %k, "w") as output:
        for r in result:
            output.write(';'.join(r) + '\n')

def covert_to_raw(result, order, connect_str='~'):

    covert_result = []
    qi_len = len(order)
    for record in result:
        covert_record = []
        for i in range(qi_len):
            if len(order[i]) > 0:
                vtemp = ''
                if connect_str in record[i]:
                    temp = record[i].split(connect_str)
                    raw_list = []
                    for j in range(int(temp[0]), int(temp[1]) + 1):
                        raw_list.append(order[i][j])
                    vtemp = connect_str.join(raw_list)
                else:
                    vtemp = order[i][int(record[i])]
                covert_record.append(vtemp)
            else:
                covert_record.append(record[i])
        if isinstance(record[-1], str):
            covert_result.append(covert_record + [record[-1]])
        else:
            covert_result.append(covert_record + [connect_str.join(record[-1])])
    return covert_result

def split_scale(age: str) -> float:
    pos = age.find("~")
    low = age[0:pos]
    high = age[pos + 1:len(age)]
    return (int(low) + int(high)) / 2.0


def cal_post_ages(post_ages: list) -> float:
    post_sum = 0
    for item in post_ages:
        if "~" in item:
            post_sum += split_scale(item)
        else: post_sum += int(item)*1.0
    return post_sum / len(post_ages)

def avg_ages(ages: list) -> float:
    return sum(ages) / len(ages)


def diff_privacy_add_laplace_noise(ages: list, loc, scale):
    laplace_noise = np.random.laplace(loc, scale, len(ages))
    res = [ages[i] + laplace_noise[i] for i in range(len(ages))]
    return res

