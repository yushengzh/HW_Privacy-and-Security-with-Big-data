# -*- coding: utf-8 -*-

import sys
import os
import time
sys.path.append('./')
from misc.util import get_eu_dist
from cryp.OPE import simOPE

class Node(object):
    def __init__(self):
        self.father = None
        self.left = None
        self.right = None
        self.feature = None
        self.split = None

    def __str__(self):
        return "切分轴: %s, 特征坐标: %s" % (str(self.feature), str(self.split[0]))

    @property
    def brother(self):

        if not self.father:
            ret = None
        else:
            if self.father.left is self:
                ret = self.father.right
            else:
                ret = self.father.left
        return ret


class KDTree(object):
    def __init__(self):

        self.root = Node()
        self.simope = simOPE()

    def __str__(self):
        ret = []
        i = 0
        que = [(self.root, -1)]
        while que:
            nd, idx_father = que.pop(0)
            ret.append("%d -> %d: %s" % (idx_father, i, str(nd)))
            if nd.left:
                que.append((nd.left, i))
            if nd.right:
                que.append((nd.right, i))
            i += 1
        return "\n".join(ret)

    def _get_median_idx(self, X, idxs, feature):
        n = len(idxs)
        # Ignoring the number of column elements is odd and even.
        k = n // 2
        # Get all the indexes and elements of column j as tuples.
        col = map(lambda i: (i, X[i][feature]), idxs)
        # Sort the tuples by the elements' values
        # and get the corresponding indexes.
        sorted_idxs = map(lambda x: x[0], sorted(col, key=lambda x: x[1]))
        # Search the median value.
        median_idx = list(sorted_idxs)[k]
        return median_idx

    def _get_variance(self, X, idxs, feature):
        n = len(idxs)
        col_sum = col_sum_sqr = 0
        for idx in idxs:
            xi = X[idx][feature]
            col_sum += xi
            col_sum_sqr += xi ** 2
        # D(X) = E{[X-E(X)]^2} = E(X^2)-[E(X)]^2
        return col_sum_sqr / n - (col_sum / n) ** 2

    def _choose_feature(self, X, idxs):
        m = len(X[0])
        variances = map(lambda j: (
            j, self._get_variance(X, idxs, j)), range(m))
        return max(variances, key=lambda x: x[1])[0]

    def _split_feature(self, X, idxs, feature, median_idx):
        idxs_split = [[], []]
        split_val = X[median_idx][feature]
        for idx in idxs:
            # Keep the split point in current node.
            if idx == median_idx:
                continue
            # Split
            xi = X[idx][feature]
            if xi < split_val:
                idxs_split[0].append(idx)
            else:
                idxs_split[1].append(idx)
        return idxs_split

    def build_tree(self, X, y):
        print("正在加密,稍后建树……")
        for i in range(len(X)):
            X[i] = [float(self.simope.encryption(float(X[i][0]))), float(self.simope.encryption(float(X[i][1])))]
        for i in range(len(y)):
            y[i] = float(self.simope.encryption(float(y[i])))
        # Initialize with node, indexes
        nd = self.root
        idxs = range(len(X))
        que = [(nd, idxs)]
        print("加密完成!")
        time.sleep(2)
        print("正在建树，稍后检索……")
        while que:
            nd, idxs = que.pop(0)
            n = len(idxs)
            # Stop split if there is only one element in this node
            if n == 1:
                nd.split = (X[idxs[0]], y[idxs[0]])
                continue
            # Split
            feature = self._choose_feature(X, idxs)
            median_idx = self._get_median_idx(X, idxs, feature)
            idxs_left, idxs_right = self._split_feature(
                X, idxs, feature, median_idx)
            # Update properties of current node
            nd.feature = feature
            nd.split = (X[median_idx], y[median_idx])
            # Put children of current node in que
            if idxs_left != []:
                nd.left = Node()
                nd.left.father = nd
                que.append((nd.left, idxs_left))
            if idxs_right != []:
                nd.right = Node()
                nd.right.father = nd
                que.append((nd.right, idxs_right))

    def _search(self, Xi, nd):

        while nd.left or nd.right:
            if not nd.left:
                nd = nd.right
            elif not nd.right:
                nd = nd.left
            else:
                if Xi[nd.feature] < nd.split[0][nd.feature]:
                    nd = nd.left
                else:
                    nd = nd.right
        return nd

    def _get_eu_dist(self, Xi, nd):
        X0 = nd.split[0]
        return get_eu_dist(Xi, X0)

    def _get_hyper_plane_dist(self, Xi, nd):
        j = nd.feature
        X0 = nd.split[0]
        return abs(Xi[j] - X0[j])

    def nearest_neighbour_search(self, Xi):
        # The leaf node after searching Xi.
        dist_best = float("inf")
        nd_best = self._search(Xi, self.root)
        que = [(self.root, nd_best)]
        while que:
            nd_root, nd_cur = que.pop(0)
            # Calculate distance between Xi and root node
            dist = self._get_eu_dist(Xi, nd_root)
            # Update best node and distance.
            if dist < dist_best:
                dist_best, nd_best = dist, nd_root
            while nd_cur is not nd_root:
                # Calculate distance between Xi and current node
                dist = self._get_eu_dist(Xi, nd_cur)
                # Update best node, distance and visit flag.
                if dist < dist_best:
                    dist_best, nd_best = dist, nd_cur
                # If it's necessary to visit brother node.
                if nd_cur.brother and dist_best > \
                        self._get_hyper_plane_dist(Xi, nd_cur.father):
                    _nd_best = self._search(Xi, nd_cur.brother)
                    que.append((nd_cur.brother, _nd_best))
                # Back track.
                nd_cur = nd_cur.father

        return nd_best