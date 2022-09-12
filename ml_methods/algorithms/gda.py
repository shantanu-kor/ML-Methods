import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decimal import Decimal
import math
from cmdexec import Terminate
from utils import Comp
from matrix import matx, matutils, pwr
from data import data


class _Predict(matutils, matx):
    
    # returns True for y=1 and False for y=0
    @staticmethod
    def _pc1(d: dict, x: matx, ret=False) -> bool:
        try:
            if Comp.eqval(d["n"], x.rowlen) is None:
                raise Exception
            dif = [matutils.msub(x, matx(i, True, True), False, True) for i in d["mean"]]
            if dif is None:
                raise Exception
            cov = matx(d["cov"], True, True)
            if cov is None:
                raise Exception
            dn = pwr(Decimal(str(2 * math.pi)), Decimal(str(d["n"] / 2)), False, True) * pwr(matutils.dnant(cov, False, True), Decimal(str(1 / 2)))
            if dn is None:
                raise Exception
            h = [pwr(Decimal(str(math.e)), (matutils.mmult(matutils.mmult(i, matutils.invse(cov, False, True), False, True), matutils.tpose(i, False, True), False, True).matx[0][0]) / -2, False, True) / dn for i in dif]
            h = [h[0]*Decimal(d["phi"][0]), h[1]*Decimal(d["phi"][1])]
            if h is None:
                raise Exception
            if h[0] > h[1]:
                return False
            else:
                return True
        except Exception as e:
            Terminate.retrn(ret, e)


class PGDA(_Predict, matx, Comp):
    @classmethod
    def y(cls, d: dict, x: list, ret=False) -> int:
        try:
            if Comp.tdict(d) is None:
                raise Exception
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            if Comp.eqval(d["n"], x.rowlen) is None:
                raise Exception
            y = _Predict._pc1(d, x, True)
            if y is True:
                return 1
            else:
                return 0
        except Exception as e:
            Terminate.retrn(ret, e)


    @classmethod
    def clas(cls, d: dict, x: list, ret=False) -> int:
        try:
            if Comp.tdict(d) is None:
                raise Exception
            c = dict()
            for i in d.items():
                cl = cls.y(i[1], x, True)
                if cl is None:
                    raise Exception
                if cl == 1:
                    c[i[0][1]] = c.setdefault(i[0][1], 0) + 1
                else:
                    c[i[0][0]] = c.setdefault(i[0][0], 0) + 1
            mx = 0
            mc = 0
            for i in c.items():
                if i[1] > mx:
                    mx = i[1]
                    mc = i[0]
            return mc
        except Exception as e:
            Terminate.retrn(ret, e)


class _Calculate(_Predict, matutils, matx):

    # misclassifications after classification
    @classmethod
    def _misclassed(cls, d: tuple, d1: dict, const: tuple[bool, bool], method='logreg', ret=False) -> dict:
        try:
            d = (matutils.matlxtox(d[0], False, True), d[1])
            dic = dict()
            dic.setdefault("0", [0, 0, []])
            dic.setdefault("1", [0, 0, []])
            for i in range(d[1].collen):
                if d[1].mele(i, 0, False, True) == 0:
                    dic["0"][0] += 1
                    if _Predict._pc1(d1, d[0][i]) is True:
                        dic["0"][1] += 1
                        dic["0"][2].append([str(j) for j in d[0][i].matxl()[0]])
                else:
                    dic["1"][0] += 1
                    if _Predict._pc1(d1, d[0][i]) is False:
                        dic["1"][1] += 1
                        dic["1"][2].append([str(j) for j in d[0][i].matxl()[0]])
                    return dic
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns mean x and phi for GDA
    @staticmethod
    def _meanx_phi(d: tuple, ret=False) -> dict:
        try:
            y1 = 0
            y2 = 0
            d = (matutils.matlxtox(d[0], False, True), d[1])
            lx = d[0][0].rowlen
            x1 = matutils.eqelm(1, lx, Decimal('0.0'), False, True)
            x2 = matutils.eqelm(1, lx, Decimal('0.0'), False, True)
            for i in range(d[1].collen):
                if d[1].mele(i, 0, False, True) == 0:
                    y1 += 1
                    x1.matx = matutils.madd(x1, d[0][i], False, True)
                else:
                    x2.matx = matutils.madd(x2, d[0][i], False, True)
                    y2 += 1
            y1 = Comp.tdeciml(y1)
            y2 = Comp.tdeciml(y2)
            return {"mean": [matutils.smult(1 / y1, x1, False, True).matxl()[0], matutils.smult(1 / y2, x2, False, True).matxl()[0]],
                    "phi": [y1 / (y1 + y2), y2 / (y1 + y2)]}
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns covariance and n for GDA
    @staticmethod
    def _cov_n(d: tuple, x1: matx, x2: matx, ret=False) -> dict:
        try:
            d = (matutils.matlxtox(d[0], False, True), d[1])
            xl = d[0][0].rowlen
            cov = matutils.eqelm(xl, xl, Decimal('0.0'), False, True)
            for i in range(d[1].collen):
                if d[1].mele(i, 0, False, True) == 0:
                    xd = matutils.msub(d[0][i], x1, False, True)
                    cov.matx = matutils.madd(cov, matutils.mmult(matutils.tpose(xd, False, True), xd, False, True), False, True)
                else:
                    xd = matutils.msub(d[0][i], x2, False, True)
                    cov.matx = matutils.madd(cov, matutils.mmult(matutils.tpose(xd, False, True), xd, False, True), False, True)
            return {"cov": matutils.smult(Decimal(str(1 / d[1].collen)), cov, False, True).matxl(), "n": xl}
        except Exception as e:
            Terminate.retrn(ret, e)

    # performs gaussian discriminant analysis
    @classmethod
    def _gda(cls, d: data, ret=False) -> dict:
        try:
            d = d.data
            dic1 = cls._meanx_phi(d, True)
            if dic1 is None:
                raise Exception
            dic2 = cls._cov_n(d, matx(dic1["mean"][0]), matx(dic1["mean"][1]), True)
            if dic2 is None:
                raise Exception
            dic1.update(dic2)
            miscl = cls._misclassed(d, dic1, None, 'gda', True)
            if miscl is None:
                raise Exception
            dic1.setdefault("misclassifications", miscl)
            dic1.update({"mean": [[str(j) for j in i] for i in dic1["mean"]], "cov": [[str(j) for j in i] for i in dic1["cov"]], "phi": [str(i) for i in dic1["phi"]]})
            return dic1
        except Exception as e:
            Terminate.retrn(ret, e)


class GDA(_Calculate, Comp):
    
    @classmethod
    def gda(cls, d: data, ret=False) -> dict:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            return _Calculate._gda(d, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def gdagc(cls, d: dict, ret=False) -> dict:
        try:
            dic = dict()
            for i in d.items():
                dic[i[0]] = cls.gda(i[1], True)
            return dic
        except Exception as e:
            Terminate.retrn(ret, e)


# a = GDA.gda(
#    data([[10, 10, 10], [5, 7, 9], [4, 2, 7], [5, 9, 1], [20, 20, 20], [21, 25, 22], [14, 18, 12], [12, 15, 11]],
#         [[0], [0], [0], [0], [1], [1], [1], [1]]))
# print(a)