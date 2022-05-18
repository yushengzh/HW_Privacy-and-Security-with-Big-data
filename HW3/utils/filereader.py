import pandas as pd
import numpy as np

class txt_Reader():
    def __init__(self, filename):
        self.filename = filename

    def read_txt(self, path: str, title_column: list) -> list:
        filepath = path + self.filename
        txtlist = []
        with open(filepath, encoding='gbk') as f:
            for line in f:
                txtlist.append(line.strip().split(","))
            f.close()
        return pd.DataFrame(txtlist, columns=title_column)

