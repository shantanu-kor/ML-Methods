import json
from decimal import Decimal
from data import data
from matrix import matx, matutils
from cmdexec import Terminate, Comp


class _Output:
    # save the regression output
    @classmethod
    def _save(cls, li: str, d: dict, k: str) -> None:
        with open(li, 'r') as f:
            dic = json.load(f)
        dic[k] = cls._chktuple(d)
        with open(li, 'w') as f:
            json.dump(dic, f)

    @classmethod
    def _chktuple(cls, d: dict) -> dict:
        dic = dict()
        for i in d.keys():
            if type(d[i]) == dict:
                if type(i) != tuple:
                    dic.update({i: cls._chktuple(d[i])})
                else:
                    dic.update({str(i): cls._chktuple(d[i])})
            else:
                if type(i) != tuple:
                    dic.update({i: d[i]})
                else:
                    dic.update({str(i): d[i]})
        return dic


class _getData(data):
    # transform json data into data object for regression
    @classmethod
    def _regression(cls, li: str) -> data:
        with open(li, 'r') as f:
            dic = json.load(f)
        x = list()
        y = list()
        for i in dic["points"].values():
            x.append(i[0])
            y.append([i[1]])
        return data(x, y)

    # transform json data into data object for classification
    @classmethod
    def _classification(cls, li: str) -> dict:
        with open(li, 'r') as f:
            dic = json.load(f)
        d = dict()
        for i, j in dic["classes"].items():
            for k, l in dic["classes"].items():
                if k > i:
                    d[(i, k)] = cls._clasdata(j, l)
        return d

    @classmethod
    def _clasdata(cls, x1: list, x2: list) -> data:
        return data(x1 + x2, [[0.0] for _ in range(len(x1))] + [[1.0] for _ in range(len(x2))])

    @classmethod
    def _regdata(cls, y: list, x: tuple) -> data:
        lx = list()
        for i in x:
            lx.append(i)
        return data(matutils.tpose(matx(lx)).matx, y)


class Results(_Output):
    @classmethod
    def save(cls, d: dict, li: str, k: str) -> None:
        cls._save(li, d, k)


class GetData(_getData):
    @classmethod
    def regression(cls, li: str) -> data:
        return cls._regression(li)

    @classmethod
    def classification(cls, li: str) -> dict:
        return cls._classification(li)

    @classmethod
    def regdata(cls, y: list, *x: list) -> data:
        return cls._regdata(y, x)

    @classmethod
    def clasdata(cls, c0: list, c1: list) -> data:
        return cls._clasdata(c0, c1)


class Parameter:
    @classmethod
    def parlogreg(cls, d: dict, p: list) -> dict:
        try:
            if Comp.tdict(d) is None:
                raise Exception
            p = Comp.dlist(p)
            if p is None:
                raise Exception
            if Comp.tdata(list(d.values())) is None:
                raise Exception
            pd = dict()
            for i in d.keys():
                pd[i] = {"parameters": p[i]}
            return pd
        except Exception as e:
            Terminate.retrn(True, e)

    @classmethod
    def parlogregter(cls, d: dict) -> dict:
        try:
            if Comp.tdict(d) is None:
                raise Exception
            if Comp.tdata(list(d.values())) is None:
                raise Exception
            pd = dict()
            for i in d.keys():
                print("class: " + str(i) + "\n")
                p = list()
                for j in range(d[i].xvars + 1):
                    par = input("parameter " + str(j) + "\n")
                    try:
                        par = Decimal(str(par))
                    except ValueError:
                        raise Exception(str(par) + " is not float")
                    if par is None:
                        raise Exception
                    p.append(par)
                if p is None:
                    raise Exception
                pd[i] = {"parameters": p}
            return pd
        except Exception as e:
            Terminate.retrn(True, e)


# d = GetData.clasdata([[0, 1, 2], [2, 1, 2], [2, 1, 5]], [[2, 4, 5], [5, 6, 8]])
# d.pdata
# p = Parameter.parlogregter({('0', '1'): d})
# print(p)
# d = GetData.regdata([1, 2, 3, 4], [1, 2, 3, 4], [2, 4, 6, 8], [1, 4, 9, 16], [4, 5, 9, 8])
# d.pdata
