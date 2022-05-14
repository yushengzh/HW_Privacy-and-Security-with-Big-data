import struct
from typing import List

def byte2float(bt: list) -> float:
    #temp = []
    #for i in bt:
    #    temp.append(int(i, 16))
    ft = struct.unpack('<f', struct.pack('4B', *bt))[0]
    ft = round(ft, 6)
    return ft


def float2byte(ft: float) -> list:
    # ['', '', '', '']
    return [int(hex(i), 16) for i in struct.pack('f', ft)]


def get_eu_dist(arr1: List, arr2: List) -> float:
    """Calculate the Euclidean distance of two vectors.
    Arguments:
        arr1 {list} -- 1d list object with int or float
        arr2 {list} -- 1d list object with int or float
    Returns:
        float -- Euclidean distance
    """

    return sum((x1 - x2) ** 2 for x1, x2 in zip(arr1, arr2)) ** 0.5