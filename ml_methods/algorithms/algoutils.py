# import os, sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decimal import Decimal
import math
from cmdexec import Terminate, Comp
from matrix import matx, matutils, pwr
from data import data


class apn(matx, Comp):
    def __init__(self, apn: tuple[Decimal | Decimal], chk=True, ret=False) -> None:
        try:
            match chk:
                case False:
                    self.__apn = matx(apn, False, True)
                case True:
                    apn = matx(apn, True, True)
                    if apn is None or Comp.eqval(apn.rowlen, 2) is None or Comp.eqval(apn.collen, 1) is None:
                        raise Exception
                    self.__apn = apn
                case _:
                    raise Exception("Invalid argument: chk => bool")
            if self.__apn.mele(0, 1, False, True) == 0:
                self.__dapn = None
            else:
                self.__dapn = matx(tuple([self.__apn.mele(0, 0, False, True) * self.__apn.mele(0, 1, False, True), self.__apn.mele(0, 1, False, True) - 1]), False, True)
            del apn
            self.val = lambda p: self.__fval(p)
            self.dval = lambda p: self.__fdval(p)
        except Exception as e:
            Terminate.retrn(ret, e)

    def __fval(self, p: Decimal) -> Decimal:
        if self.__apn.mele(0, 1, False, True) == 0:
            return self.__apn.mele(0, 0, False, True)
        else:
            return self.__apn.mele(0, 0, False, True) * pwr(Decimal(str(p)), self.__apn.mele(0, 1, False, True), False, True)

    def __fdval(self, p: Decimal) -> Decimal:
        if self.__dapn == None:
            return Decimal('0.0')
        else:
            return self.__dapn.mele(0, 0, False, True) * pwr(Decimal(str(p)), self.__dapn.mele(0, 1, False, True), False, True)


class parameter(matx):
    def __init__(self, li: list[list[list]] | tuple[tuple[tuple[Decimal, Decimal], ...], ...], chk=True, ret=False) -> None:
        try:
            par = list()
            n = list()
            for i in li:
                par1 = list()
                for j in i:
                    par1.append(apn(j, chk, True))
                n.append(len(par1))
                par.append(tuple(par1))
            self.__par = tuple(par)
            self.n = tuple(n)
            del par, n
            self.val = lambda p: self.__fval(p)
            self.dval = lambda p: self.__fdval(p)
        except Exception as e:
            Terminate.retrn(ret, e)
    
    def __fval(self, p: matx) -> tuple[matx, ...]:
        l = list()
        for i in enumerate(self.__par):
            pv = p.mele(0, i[0], False, True)
            li = list()
            for j in i[1]:
                li.append(j.val(pv))
            l.append(matx(tuple(li), False, True))
        return tuple(l)
    
    def __fdval(self, p: matx) -> tuple[matx, ...]:
        l = list()
        for i in enumerate(self.__par):
            pv = p.mele(0, i[0], False, True)
            li = list()
            for j in i[1]:
                li.append(j.dval(pv))
            l.append(matx(tuple(li), False, True))
        return tuple(l)


class function(matutils, matx):
    def __init__(self, li: tuple, chk=True, ret=False) -> None:
        try:
            match chk:
                case True:
                    if Comp.tmatx(li, True) is None:
                        raise Exception
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: chk => bool")
            self.__x = li
            self.val = lambda p: self.__fval(p)
            del li
        except Exception as e:
            Terminate.retrn(ret, e)
    
    def __fval(self, p: tuple[matx, ...]) -> matx:
        for i in enumerate([matutils.mmult(i[1], matutils.tpose(p[i[0]]), False, True) for i in enumerate(self.__x)]):
            if i[0] == 0:
                x = i[1]
            else:
                x = matutils.addmatx(x, i[1], False, False, True)
        return x


class Calculate(matx):

    @classmethod
    def _cmperrpr(cls, p: matx, pn: matx, pr: Decimal, ret=False) -> bool:
        try:
            for i in range(pn.rowlen):
                if float(pn.mele(0, i, False, True)) == float("nan") or float(pn.mele(0, i, False, True)) == float(Decimal("inf")) or float(pn.mele(0, i, False, True)) == float("-inf"):
                    for j in range(pn.rowlen):
                            print("parameter " + str(j) + " is " + str(float(pn.mele(0, j, False, True))))
                    raise Exception
            err = math.sqrt(sum([pwr((i[1] - p.mele(0, i[0], False, True)) / i[1], 2, False, True) for i in enumerate(pn.matx[0])]) / p.rowlen)
            if err < pr:
                return True
            else:
                return False
        except Exception as e:
            Terminate.retrn(ret, e)


class Scale(data, matutils, matx):
    # scale matx between [0, 1]
    @classmethod
    def _scale0to1x(cls, x: matx, ret=False) -> dict:
        try:
            x = matutils.tpose(x, False, True)
            mx = list()
            mn = list()
            for i in x.matx:
                mn.append(min(i))
            x = matutils.msub(x, matx(tuple([tuple([mn[i] for _ in range(x.rowlen)]) for i in range(x.collen)]), False, True), False, True)
            for i in x.matx:
                mx.append(max(i))
            x = matutils.tpose(matutils.smultfac(tuple([1/ i for i in mx]), x, True, False, True), False, True)
            if x is None:
                raise Exception
            return {"constant": matx(tuple(mn), False, True), "factor": matx(tuple(mx), False, True), "values": x}
        except Exception as e:
            Terminate.retrn(ret, e)

    # scale data values between [0,1]
    @classmethod
    def _scale0to1(cls, d: data, ret=False) -> dict:
        try:
            x = cls._scale0to1x(d.getax(), True)
            y = cls._scale0to1x(d.getay(), True)
            if x is None or y is None:
                raise Exception
            return {"constant": matutils.addmatx(x["constant"], y["constant"], chk=False, ret=True),
                    "factor": matutils.addmatx(x["factor"], y["factor"], chk=False, ret=True),
                    "data": data(x["values"], y["values"], False, True)}
        except Exception as e:
            Terminate.retrn(ret, e)
