# -*- coding: utf-8 -*-

from misc.newKdTree import KDTree

class MaxHeap(object):
    def __init__(self, max_size, fn):
        """MaxHeap class.

        Arguments:
            max_size {int} -- The maximum size of MaxHeap instance.
            fn {function} -- Function to caculate the values of items
            when comparing items.

        Attributes:
            _items {object} -- The items in the MaxHeap instance.
            size {int} -- The size of MaxHeap instance.
        """

        self.max_size = max_size
        self.fn = fn

        self._items = [None] * max_size
        self.size = 0

    def __str__(self):
        item_values = str([self.fn(x) for x in self.items])
        info = (self.size, self.max_size, self.items, item_values)
        return "Size: %d\nMax size: %d\nItems: %s\nItem_values: %s\n" % info

    @property
    def items(self):
        return self._items[:self.size]

    @property
    def full(self):
        return self.size == self.max_size

    def value(self, idx):
        item = self._items[idx]
        if item is None:
            ret = -float('inf')
        else:
            ret = self.fn(item)
        return ret

    def add(self, item):
        if self.full:
            if self.fn(item) < self.value(0):
                self._items[0] = item
                self._shift_down(0)
        else:
            self._items[self.size] = item
            self.size += 1
            self._shift_up(self.size - 1)

    def pop(self):

        assert self.size > 0, "Cannot pop item! The MaxHeap is empty!"
        ret = self._items[0]
        self._items[0], self._items[self.size - 1] = \
            self._items[self.size - 1], self._items[0]
        self.size -= 1
        self._shift_down(0)
        return ret

    def _shift_up(self, idx):

        assert idx < self.size, \
            "The parameter idx must be less than heap's size!"
        parent = (idx - 1) // 2
        while parent >= 0 and self.value(parent) < self.value(idx):
            self._items[parent], self._items[idx] = \
                self._items[idx], self._items[parent]
            idx = parent
            parent = (idx - 1) // 2

    def _shift_down(self, idx):
        """Shift down item until its children are less than the item.

        Arguments:
            idx {int} -- Heap item's index.
        """

        child = (idx + 1) * 2 - 1
        while child < self.size:
            # Compare the left child and the right child and get the index
            # of the larger one.
            if child + 1 < self.size and \
                    self.value(child + 1) > self.value(child):
                child += 1
            # Swap the items, if the value of father is less than child.
            if self.value(idx) < self.value(child):
                self._items[idx], self._items[child] = \
                    self._items[child], self._items[idx]
                idx = child
                child = (idx + 1) * 2 - 1
            else:
                break

    def _is_valid(self):
        """Validate a MaxHeap by comparing all the parents and its children.

        Returns:
            bool
        """

        ret = []
        for i in range(1, self.size):
            parent = (i - 1) // 2
            ret.append(self.value(parent) >= self.value(i))
        return all(ret)


class KNeighborsBase(object):

    def __init__(self):
        self.k_neighbors = None
        self.tree = None

    def fit(self, X:list, y:list, k_neighbors:int):
        self.k_neighbors = k_neighbors
        self.tree = KDTree()
        self.tree.build_tree(X, y)

    def _knn_search(self, Xi:list) -> list:
        tree = self.tree
        simope = tree.simope
        print("????????????????????????"+str(Xi))
        Xi = [float(simope.encryption(float(Xi[0]))), float(simope.encryption(float(Xi[1])))]
        print("simOPE?????????"+str(Xi))
        heap = MaxHeap(self.k_neighbors, lambda x: x.dist)
        nd = tree._search(Xi, tree.root)
        que = [(tree.root, nd)]
        while que:
            nd_root, nd_cur = que.pop(0)
            nd_root.dist = tree._get_eu_dist(Xi, nd_root)
            heap.add(nd_root)
            while nd_cur is not nd_root:
                nd_cur.dist = tree._get_eu_dist(Xi, nd_cur)
                heap.add(nd_cur)
                if nd_cur.brother and (not heap or heap.items[0].dist >
                         tree._get_hyper_plane_dist(Xi, nd_cur.father)):
                    _nd = tree._search(Xi, nd_cur.brother)
                    que.append((nd_cur.brother, _nd))
                # Back track.
                nd_cur = nd_cur.father
        cnt = 0
        print("????????????????????????")
        for nd in heap.items:
            cnt += 1
            print("???" + str(cnt) + "???" +
                  " ????????????" + str(nd.split[0]) +" ????????????" +
                  str([round(float(simope.decryption(float(nd.split[0][0]))), 6),
                       round(float(simope.decryption(float(nd.split[0][1]))), 6)]))
        return heap

