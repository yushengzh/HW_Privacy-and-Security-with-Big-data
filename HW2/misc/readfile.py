
class Readfile:
    def __init__(self, filename: str):
        self.name = filename

    def read_txt(self, path: str) -> list:
        filepath = path + self.name
        txt = []
        with open(filepath, encoding='gbk') as f:
            for line in f:
                txt.append(line.strip().split(" ", 1))
            f.close()
        # for pair in txt
        for i in range(len(txt)):
            txt[i] = [float(txt[i][0]), float(txt[i][1])]
        return txt
