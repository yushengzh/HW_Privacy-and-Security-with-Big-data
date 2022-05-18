from misc.KDTree import KDTree


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
        self._items = [None] * int(max_size)

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
        """If the heap is full.
        Returns:
            bool
        """

        return self.size == self.max_size

    def value(self, idx):
        """Caculate the value of item.
        Arguments:
            idx {int} -- The index of item.
        Returns:
            float
        """
        item = self._items[idx]
        if item is None:
            ret = -float('inf')
        else:
            ret = self.fn(item)
        return ret

    def add(self, item):
        """Add a new item to the MaxHeap.
        Arguments:
            item {object} -- The item to add.
        """

        if self.full:
            if self.fn(item) < self.value(0):
                self._items[0] = item
                self._shift_down(0)
        else:
            self._items[self.size] = item
            self.size += 1
            self._shift_up(self.size - 1)

    def pop(self):
        """Pop the top item out of the heap.
        Returns:
            object -- The item popped.
        """

        assert self.size > 0, "Cannot pop item! The MaxHeap is empty!"
        ret = self._items[0]
        self._items[0], self._items[self.size - 1] = \
            self._items[self.size - 1], self._items[0]
        self.size -= 1
        self._shift_down(0)
        return ret

    def _shift_up(self, idx):
        """Shift up item unitl its parent is greater than the item.
        Arguments:
            idx {int} -- Heap item's index.
        """

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


class K_Nearest_Neighbor():
    def __init__(self):
        self.k = None
        self.tree = None

    def fit(self, X, y, k):
        self.k = k
        self.tree = KDTree()
        self.tree.build_tree(X, y)

    def knn(self, tar):
        tree = self.tree
        simope = tree.simope
        print("需要查询的明文为" + str(tar))
        tar = [float(simope.encryption(float(tar[0]))), float(simope.encryption(float(tar[1])))]
        print("simOPE加密为" + str(tar))
        heap = MaxHeap(self.k, lambda x: x.dist)
        node = tree.search_new(tar, tree.root)
        que = [(tree.root, node)]
        while que:
            nd_root, nd_cur = que.pop(0)
            # Calculate distance between Xi and root node
            nd_root.dist = tree.get_eu_distance(tar, nd_root)
            # Update best node and distance.
            heap.add(nd_root)
            while nd_cur is not nd_root:
                # Calculate distance between Xi and current node
                nd_cur.dist = tree.get_eu_distance(tar, nd_cur)
                # Update best node and distance
                heap.add(nd_cur)
                # If it's necessary to visit brother node.
                if nd_cur.get_brother and \
                        (not heap or
                         heap.items[0].dist >tree.get_hyper_plane_dist(tar, nd_cur.father)):
                    _nd = tree.search_new(tar, nd_cur.get_brother)
                    que.append((nd_cur.get_brother, _nd))
                # Back track.
                nd_cur = nd_cur.father
        print("近似查询结果如下")
        cnt = 0
        for nd in heap.items:
            cnt += 1
            print("第"+str(cnt)+"项")
            print([round(float(simope.decryption(float(nd.split[0][0]))), 6),round(float(simope.decryption(float(nd.split[0][1]))), 6)])
            print("加密值为" + str(nd.split[0]))
        return heap

