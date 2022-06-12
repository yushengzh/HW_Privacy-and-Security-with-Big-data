"""
算法实现参考了https://en.wikipedia.org/wiki/Datafly_algorithm
"""

from utils import *
class datafly_anonymity:

    def __init__(self, k: int, raw_data: pd.DataFrame):
        """
        Assumes: | PT | ≤ k, and loss * | PT | = k
        """
        self.k = k
        self.PT = raw_data
        self.QI_num = 10
        self.QI_list = []   #  quasi-identifier QI = ( A1, ..., An )
        self.DGH_QI = []    # k-anonymity constraint k; domain generalization hierarchies DGH_Ai
        self.freq_list = []
        self.loss = self.k / len(self.PT) * 1.0 # a limit on the percentage of tuples that can be suppressed


    def get_freq_list(self, QI_name):
        freq = []
        QI = QI_name
        occur = 0
        sid = []
        for qi in self.QI_list:
            self.PT.iloc



    def compute_freq_cnt(self):
        pass

class Tree():
    def __init__(self, conf):
        self.conf =  conf
        self.root = dict()
        self.depth = -1
        self.highsest = ''
        self.build()

    def build(self):
        with open(self.conf, 'r') as file:
            for line in file:
                line = line.strip()
                if not line: continue
                line = [item.strip() for item in line.strip(',')]
                height = len(line) - 1
                if self.depth == -1: self.depth = height
                if not self.highsest: self.highsest = line[::-1]
                pre = None
                for index, val in enumerate(line[::-1]):
                    self.root[val] = (pre, height - index)
                    pre = val
            file.close()


class KAnonymity():
    def __init__(self, raw_data: list, k: int):
        self.data = raw_data
        self.k = k
        self.QI_column = ['age', 'workclass', 'education', 'education-num', 'marital-status',
                          'relationship', 'race', 'sex', 'hours-per-week', 'native-country']
        self.QI_list = [AGE_CONF, WORKCLASS_CONF, EDU_CONF, EDUNUM_CONF, MARITAL_CONF,
                        RELATIONSHIP_CONF, RACE_CONF, SEX_CONF, HPW_CONF, COUNTRY_CONF]
        assert len(self.QI_list) == len(self.QI_column)


    def __get_QI_value(self, data: list, names: list, gen_tree: Tree) -> tuple:
        QI_index, seq = [title_column.index(name) for name in names], []
        for index in QI_index:
            if index == title_column.index('age'):
                if data[index] == -1: seq.append('0-100')
                else: seq.append(str(data[index]))
            else:
                if data[index] == '*':
                    data[index] = gen_tree[names[index]].highsest
                seq.append(data[index])
        #print(seq)
        return tuple(seq)


    def anonymize(self):
        QI_freq, domains, gen_levels = {}, {}, {}
        columns = self.QI_column
        confs = self.QI_list
        k = self.k
        assert len(confs) == len(columns)
        gen_tree = dict()
        for index, name in enumerate(columns):
            gen_tree[name] = Tree(confs[index])

        # init
        for column in columns:
            domains[column] = set()
            gen_levels[column] = 0

        for index, record in enumerate(self.data):
            QI_seq = self.__get_QI_value(record[:], columns, gen_tree)

            if QI_seq in QI_freq:
                QI_freq[QI_seq].add(index)
            else:
                QI_freq[QI_seq] = {index}
                for i, val in enumerate(QI_seq):
                    domains[columns[i]].add(val)

        while True:
            neg_cnt = 0
            for _, idx_set in QI_freq.items():
                if len(idx_set) < k: neg_cnt += len(idx_set)

            if neg_cnt > k:
                most_freq_att_num = -1
                most_freq_att_name = None
                for column in columns:
                    if len(domains[column]) > most_freq_att_num:
                        most_freq_att_num = len(domains[column])
                        most_freq_att_name = column
                gen_att = most_freq_att_name
                QI_idx = columns.index(gen_att)
                domains[gen_att] = set()
                for qi_sequence in list(QI_freq.keys()):
                    new_qi_sequence = list(qi_sequence)
                    new_qi_sequence[QI_idx] = gen_tree[gen_att].root[qi_sequence[QI_idx]][0]
                    new_qi_sequence = tuple(new_qi_sequence)

                    if new_qi_sequence in QI_freq:
                        QI_freq[new_qi_sequence].update(
                            QI_freq[qi_sequence])
                        QI_freq.pop(qi_sequence, 0)
                    else:
                        QI_freq[new_qi_sequence] = QI_freq.pop(qi_sequence)

                    domains[gen_att].add(new_qi_sequence[QI_idx])

                gen_levels[gen_att] += 1
                """
                for qis in list(QI_freq.keys()):
                    new_qis = list(qis)
                    new_qis[QI_idx] = gen_tree[gen_att].root[qis[QI_idx]][0]
                    new_qis = tuple(new_qis)

                    if new_qis in QI_freq:
                        QI_freq[new_qis].update(QI_freq[qis])
                        QI_freq.pop(qis, 0)
                    else:
                        QI_freq[new_qis] = QI_freq.pop(qis)
                    domains[gen_att].add(new_qis[QI_idx])

                gen_levels[gen_att] += 1
                """
            else:
                # end the while loop
                # suppress sequences not satisfying k-anonymity
                # save results and calculate distoration and precision
                genlvl_att = [0 for _ in range(len(columns))]
                dgh_att = [gen_tree[name].level for name in columns]
                datasize = 0
                qiindex = [title_column.index(name) for name in columns]

                # used to make sure the output file keeps the same order with original data file
                towriterecords = [None for _ in range(len(self.records))]
                with open('./res/adult_%d_kanonymity.data' %k, 'w') as wf:
                    for qi_sequence, recordidxs in QI_freq.items():
                        if len(recordidxs) < k:
                            continue
                        for idx in recordidxs:
                            record = self.records[idx][:]
                            for i in range(len(qiindex)):
                                record[qiindex[i]] = qi_sequence[i]
                                genlvl_att[i] += gen_tree[columns[i]].root[qi_sequence[i]][1]
                            record = list(map(str, record))
                            for i in range(len(record)):
                                if record[i] == '*' and i not in qiindex:
                                    record[i] = '?'
                            towriterecords[idx] = record[:]
                            # wf.write(', '.join(record))
                            # wf.write('\n')
                        datasize += len(recordidxs)
                    for record in towriterecords:
                        if record is not None:
                            wf.write(', '.join(record))
                            wf.write('\n')
                        else:
                            wf.write('\n')