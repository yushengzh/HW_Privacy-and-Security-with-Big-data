import sys
sys.path.append('../')
from numpy import ndarray
from typing import List
from cryp.OPE import simOPE

class KDNode:
    def __init__(self):
        '''
        :param father 父节点 KDNode
        :param left 左子节点 KDNode
        :param right 右子节点 KDNode
        :param feature 特征坐标 (float, float)
        :param split 切分轴 int: 0[x axis]or 1[y axis](2 dimension)
        '''
        self.father = None
        self.left = None
        self.right = None
        self.feature = None
        self.split = None

    def __str__(self):
        return "特征坐标: %s and 切分轴: %s" % (str(self.feature), str(self.split))

    '''二叉树兄弟节点'''
    def get_brother(self):
        if self.father is None:
            return None
        else:
            if self.father.right is self:
                return self.father.left
            else:
                return self.father.right

class KDTree:

    def __init__(self):
        self.root = KDNode()
        self.simope = simOPE()

    def __str__(self):
        tree = [(self.root, -1)]
        i = 0
        rel = []
        while tree:
            kdn, id_dad = tree.pop(0)
            rel.append("%d-->%d:%s" % (id_dad, i, str(kdn)))
            if kdn.left is not None:
                tree.append((kdn.left, i))
            if kdn.right is not None:
                tree.append((kdn.right, i))
            i += 1
        return rel

    def _get_root_kdn_index(self, X:list, idxs:list, feature:int) -> list:
        k = len(idxs) // 2 ## 中间
        col = map(lambda i: (i, X[i][feature]), idxs)
        sortedidxs = map(lambda x: x[0], sorted(col, key=lambda x: x[1]))
        return list(sortedidxs)[k]

    '''方差'''
    def _get_varience(self, X:list, idxs:list, feature:int) -> float:
        col_sum = sqr_col_sum = 0.0
        for idx in idxs:
            xi = X[idx][feature]
            col_sum += float(xi)
            sqr_col_sum += (float(xi) ** 2)
        return sqr_col_sum / len(idxs) - (col_sum / len(idxs)) ** 2     ## D(x) = E(X^2) - E(x)^2

    def choose_feat(self, X:list, idxs:list) -> int:
        varience = map(lambda i:(i ,self._get_varience(X, idxs, i)), range(len(X[0])))
        return max(varience, key=lambda x:x[1])[0]

    def get_eu_distance(self, xi: list, kdn: KDNode) -> float:
        x0 = kdn.split[0]
        return self.get_eu_dist(xi, x0)
        # return (float(x0[0]) - float(xi[0])) ** 2 + (float(x0[1]) - float(xi[1])) ** 2

    def get_eu_dist(self, arr1: List, arr2: List) -> float:
        #for x1, x2 in zip(arr1, arr2): print(x1, x2)
        return sum((float(x1) - float(x2)) ** 2 for x1, x2 in zip(arr1, arr2)) ** 0.5

    def get_euclidean_distance(self, arr1: ndarray, arr2: ndarray) -> float:
        return ((arr1 - arr2) ** 2).sum() ** 0.5


    def _split_feature(self, X: list, idxs: list, feature: int, midian_idx) -> list:
        res = [[],[]]
        split_val = X[midian_idx][feature]
        for idx in idxs:
            if idx == midian_idx: continue
            xi = X[idx][feature]
            if xi < split_val:
                res[0].append(idx)
            else:
                res[1].append(idx)
        return res

    def build_tree(self, X: list, y: list) -> None:
        '''
        :param X: 2 dimension object with float
        :param y: 1 dimension object woth float
        :return: none
        '''

        for i in range(len(X)):
            X[i] = [str(self.simope.encryption(float(X[i][0]))), str(self.simope.encryption(float(X[i][1])))]
        for i in range(len(y)):
            y[i] = str(self.simope.encryption(float(y[i])))
        nd = self.root
        idxs = range(len(X))
        que = [(nd, idxs)]
        print("正在建树，稍后检索……")
        while que:
            nd, idxs = que.pop(0)
            n = len(idxs)
            # Stop split if there is only one element in this node
            if n == 1:
                nd.split = (X[idxs[0]], y[idxs[0]])
                continue
            # Split
            feature = self.choose_feat(X, idxs)
            median_idx = self._get_root_kdn_index(X, idxs, feature)
            idxs_left, idxs_right = self._split_feature(X, idxs, feature, median_idx)
            # Update properties of current node
            nd.feature = feature
            nd.split = (X[median_idx], y[median_idx])
            # Put children of current node in que
            if idxs_left:
                nd.left = KDNode()
                nd.left.father = nd
                que.append((nd.left, idxs_left))
            if idxs_right:
                nd.right = KDNode()
                nd.right.father = nd
                que.append((nd.right, idxs_right))

    def get_hyper_plane_dist(self, Xi: list, nd: KDNode) -> float:
        i = nd.feature
        X0 = nd.split[0]
        return abs(float(Xi[i]) - float(X0[i]))

    def search_new(self, Xi: list, nd) -> KDNode:

        while nd.right or nd.left:
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

    def nearest_neighbour_search(self, Xi: list) -> KDNode:
        Xi = [str(self.simope.encryption(float(Xi[0]))), str(self.simope.encryption(float(Xi[1])))]
        print("加密的密文为：" + str(Xi))
        # The leaf node after searching Xi.
        dist_best = float("inf")
        nd_best = self.search_new(Xi, self.root)
        que = [(self.root, nd_best)]
        while que:
            nd_root, nd_cur = que.pop(0)
            # Calculate distance between Xi and root node
            dist = self.get_eu_distance(Xi, nd_root)
            # Update best node and distance.
            if dist < dist_best:
                dist_best, nd_best = dist, nd_root
            while nd_cur is not nd_root:
                # Calculate distance between Xi and current node
                dist = self.get_eu_distance(Xi, nd_cur)
                # Update best node, distance and visit flag.
                if dist < dist_best:
                    dist_best, nd_best = dist, nd_cur
                # If it's necessary to visit brother node.
                if nd_cur.get_brother and dist_best > \
                        self.get_hyper_plane_dist(Xi, nd_cur.father):
                    _nd_best = self.search_new(Xi, nd_cur.get_brother)
                    que.append((nd_cur.get_brother, _nd_best))
                # Back track.
                nd_cur = nd_cur.father

        return nd_best


    def Decrption_res(self, nd_best):
        plain = []
        for i in range(len(nd_best)):
            plain.append([round(float(self.simope.decryption(float(nd_best[i][0]))), 6), round(float(self.simope.decryption(float(nd_best[i][1]))),0)])
        return  plain



