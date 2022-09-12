import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decimal import Decimal
import math
from cmdexec import Terminate
from utils import Comp
from matrix import matx, matutils, pwr
from data import data, datautils
from algoutils import parameter, Scale, Calculate


class _Predict(matutils, matx):

    @classmethod
    def _pc1(cls, x: matx, p: matx, const: tuple[bool, bool], ret=False) -> bool:
        try:
            match const[1]:
                case True:
                    x = matutils.maddval(x, Decimal('1.0'), False, True)
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            match const[0]:
                case False:
                    h =  1 / (1 + pwr(Decimal(str(math.e)), -matutils.mmult(p, matutils.tpose(x, False, True), False, True).matx[0][0], False, True))
                    if h is None:
                        raise Exception
                    if h < 0.5:
                        return False
                    else:
                        return True
                case True:
                    p = matx(p, False, True)
                    p0 = p.pop(0, False, False, True)[0]
                    h =  1 / (1 + pwr(Decimal(str(math.e)), -p0 * matutils.mmult(p, matutils.tpose(x, False, True), False, True).matx[0][0], False, True))
                    if h is None:
                        raise Exception
                    if h < 0.5:
                        return False
                    else:
                        return True
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
        except Exception as e:
            Terminate.retrn(ret, e)


class PLogReg(_Predict, matx, Comp):

    @classmethod
    def y(cls, x: list, p: list, const=(False, True), ret=False) -> int:
        try:
            p = matx(p, ret=True)
            if p is None:
                raise Exception
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            y = _Predict._pc1(p, x, const, True)
            if y is True:
                return 1
            else:
                return 0
        except Exception as e:
            Terminate.retrn(ret, e)


    @classmethod
    def clas(cls, x: list, d: dict, const=(False, True), ret=False) -> int:
        try:
            if Comp.tdict(d) is None:
                raise Exception
            c = dict()
            for i in d.items():
                cl = cls.y(i[1]["parameters"], x, const, True)
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


class _ScalePar(matutils):
        
    # scale parameter values for logistic regression
    @staticmethod
    def _0to1(c: matx, f: matx, p: matx, const=True, ret=False) -> matx:
        try:
            p = matx(p, False, True)
            match const:
                case True:
                    p0 = (p.pop(0, False, False, True)[0] + sum(matutils.smultfac(p.matx[0], c, False, False, True).matx[0]), )
                    p = p0 + matutils.smultfac(f.matx[0], p, False, False, True).matx[0]
                    return matx(p, False, True)
                case False:
                    p = matutils.smultfac(f.matx[0], p, False, False, True).matx[0]
                    return matx(p, False, True)
                case _:
                    raise Exception("Invalid argument: const => bool")
        except Exception as e:
            Terminate.retrn(ret, e)
    

    @staticmethod
    def _orignl(c: matx, f: matx, p: matx, const=True, ret=False) -> matx:
        try:
            p = matx(p, False, True)
            match const:
                case True:
                    p0 = p.pop(0, False, False, True)[0]
                    p = matutils.smultfac(tuple([1 / i for i in f.matx[0]]), p, False, False, True)
                    p0 -= matutils.mmult(p, matutils.tpose(c, False, True), False, True).matx[0][0]
                    return matx((p0, ) + p.matx[0], False, True)
                case False:
                    p = matutils.smultfac(tuple([1 / i for i in f.matx[0]]), p, False, False, True)
                    return matx(p, False, True)
                case _:
                    raise Exception("Invalid argument: const => bool")
        except Exception as e:
            Terminate.retrn(ret, e)


class _Calculate(_Predict, _ScalePar, Scale, matutils, Calculate, matx):

    # misclassifications after classification
    @classmethod
    def _misclassed(cls, d: tuple, d1: dict, const: tuple[bool, bool], ret=False) -> dict:
        try:
            d = (matutils.matlxtox(d[0], False, True), d[1])
            dic = dict()
            dic.setdefault("0", [0, 0, []])
            dic.setdefault("1", [0, 0, []])
            for i in range(d[1].collen):
                if d[1].mele(i, 0, False, True) == 0:
                    dic["0"][0] += 1
                    if cls._pc1(matx(tuple(d1["parameters"]), False, True), d[0][i], const, True) is True:
                        dic["0"][1] += 1
                        dic["0"][2].append([str(j) for j in d[0][i].matxl()[0]])
                else:
                    dic["1"][0] += 1
                    if cls._pc1(matx(tuple(d1["parameters"]), False, True), d[0][i], const, True) is False:
                        dic["1"][1] += 1
                        dic["1"][2].append([str(j) for j in d[0][i].matxl()[0]])
                    return dic
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def _logreg(cls, d: tuple, p: matx, a: Decimal, m: int, pr: Decimal, const: tuple[bool, bool], ret=False) -> tuple[matx, int]:
        try:
            c = 0
            while (c := c + 1) <= m:
                match const[0]:
                    case False:
                        h = matutils.powmel((Decimal('1.0'), Decimal('-1.0')), matutils.madd(matutils.eqelm(1, d[0].rowlen, Decimal('1.0'), False, True), matutils.expomel((Decimal(str(math.e)), Decimal('-1.0')), matutils.mmult(p, d[0], False, True), [0, ], True, False, True), False, True), [0, ], True, False, True)
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.mmult(d[0], matutils.tpose(matutils.msub(h, d[1], False, True), False, True), False, True), False, True), False, True), False, True)
                    case True:
                        p1 = matx(p, False, True)
                        p0 = p1.pop(0, False, False, True)[0]
                        h = matutils.powmel((Decimal('1.0'), Decimal('-1.0')), matutils.madd(matutils.eqelm(1, d[0].rowlen, Decimal('1.0'), False, True), matutils.expomel((Decimal(str(math.e)), Decimal('-1.0')), matutils.smult(p0, matutils.mmult(p1, d[0], False, True), False, True), [0, ], True, False, True), False, True), [0, ], True, False, True)
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.addmatx(matutils.mmult(matutils.mmult(p1, d[0], False, True), matutils.tpose(matutils.msub(h, d[1], False, True), False, True), False, True), matutils.mmult(matutils.smult(p0, d[0], False, True), matutils.tpose(matutils.msub(h, d[1], False, True), False, True), False, True), True, False, True), False, True), False, True), False, True)
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")        
                if pn is None:
                    raise Exception
                err = Calculate._cmperrpr(p, pn, pr)
                match err:
                    case True:
                        p.matx = pn
                        return p, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return p, c - 1
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def _logregsp(cls, d: tuple, p: matx, a, m, pr, cf: tuple[matx, matx], const: tuple[bool, bool], ret=False) -> tuple[matx, int]:
        try:
            scc = cf[0]
            scf = cf[1]
            c = 0
            while (c := c + 1) <= m:
                match const[0]:
                    case False:
                        h = matutils.powmel((Decimal('1.0'), Decimal('-1.0')), matutils.madd(matutils.eqelm(1, d[0].rowlen, Decimal('1.0'), False, True), matutils.expomel((Decimal(str(math.e)), Decimal('-1.0')), matutils.mmult(p, d[0], False, True), [0, ], True, False, True), False, True), [0, ], True, False, True)
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.mmult(d[0], matutils.tpose(matutils.msub(h, d[1], False, True), False, True), False, True), False, True), False, True), False, True)
                    case True:
                        p1 = matx(p, False, True)
                        p0 = p1.pop(0, False, False, True)[0]
                        h = matutils.powmel((Decimal('1.0'), Decimal('-1.0')), matutils.madd(matutils.eqelm(1, d[0].rowlen, Decimal('1.0'), False, True), matutils.expomel((Decimal(str(math.e)), Decimal('-1.0')), matutils.smult(p0, matutils.mmult(p1, d[0], False, True), False, True), [0, ], True, False, True), False, True), [0, ], True, False, True)
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.addmatx(matutils.mmult(matutils.mmult(p1, d[0], False, True), matutils.tpose(matutils.msub(h, d[1], False, True), False, True), False, True), matutils.mmult(matutils.smult(p0, d[0], False, True), matutils.tpose(matutils.msub(h, d[1], False, True), False, True), False, True), True, False, True), False, True), False, True), False, True)
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")       
                if pn is None:
                    raise Exception
                match const[0]:
                    case False:
                        op = _ScalePar._orignl(scc, scf, p, const[1], True)
                        opn = _ScalePar._orignl(scc, scf, pn, const[1], True)
                        if op is None or opn is None:
                            raise Exception
                    case True:
                        op = matutils.maddval(_ScalePar._orignl(scc, scf, matx(p.matx[0][1:], False, True), const[1], True), p.mele(0, 0, False, True), False, True)
                        opn = matutils.maddval(_ScalePar._orignl(scc, scf, matx(pn.matx[0][1:], False, True), const[1], True), p.mele(0, 0, False, True), False, True)
                        if op is None or opn is None:
                            raise Exception
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                err = Calculate._cmperrpr(op, opn, pr)
                match err:
                    case True:
                        p.matx = pn
                        return p, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return p, c - 1
        except Exception as e:
            Terminate.retrn(ret, e)


    @classmethod
    def _grades(cls, d: data, p: matx, a: Decimal, m: int, pr: Decimal, scale=False, const=(False, True), ret=False) -> dict:
        try:
            da = d.data
            match scale:
                case True:
                    sc = Scale._scale0to1x(d.getax(), True)
                    if sc is None:
                        raise Exception
                    d = data(sc["values"], d.getay(), False, True)
                    scc = sc["constant"]
                    scf = sc["factor"]
                    del sc
                    match const[0]:
                        case False:
                            match const[1]:
                                case True:
                                    d = datautils.dataval(d, Decimal('1.0'), False, True)
                                case False:
                                    c = matutils.smultfac([1 / i for i in scf.matx[0]], scc, False, False, True)
                                    d = data(matutils.saddcnst(c, d.getax(), False, False, True), d.getay(), False, True)
                                case _:
                                    raise Exception("Invalid argument: const => (bool, bool)")
                        case True:
                            match const[1]:
                                case True:
                                    d = datautils.dataval(d, Decimal('1.0'), False, True)
                                case False:
                                    c = matutils.smultfac([1 / i for i in scf.matx[0]], scc, False, False, True)
                                    d = data(matutils.saddcnst(c, d.getax(), False, False, True), d.getay(), False, True)
                                case _:
                                    raise Exception("Invalid argument: const => (bool, bool)")
                        case _:
                            raise Exception("Invalid argument: const => (bool, bool)")
                    match const[0]:
                        case False:
                            p = _ScalePar._0to1(scc, scf, p, const[1], True)
                            if p is None:
                                raise Exception
                        case True:
                            p = matutils.maddval(_ScalePar._0to1(scc, scf, matx(p.matx[0][1:], False, True), const[1], True), p.mele(0, 0, False, True), False, True)
                            if p is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: const => (bool, bool)")
                case False:
                    match const[1]:
                        case True:
                            d = datautils.dataval(d, Decimal('1.0'), False, True)
                        case False:
                            pass
                        case _:
                            raise Exception("Invalid argument: const => (bool, bool)")
                case _:
                    raise Exception("Invalid argument: scale => bool")
            d1 = (matutils.tpose(d.getax()), matutils.tpose(d.getay()))
            match scale:
                case True:
                    p1 = cls._logregsp(d1, p, a, m, pr, (scc, scf), const, True)
                case False:
                    p1 = cls._logreg(d1, p, a, m, pr, const, True)
                case _:
                    raise Exception("Invalid argument: scale => bool")
            if p is None:
                raise Exception
            p = p1[0]
            c = p1[1]
            del p1
            match scale:
                case True:
                    match const[0]:
                        case False:
                            p = _ScalePar._orignl(scc, scf, p, const[1], True)
                            if p is None:
                                raise Exception
                        case True:
                            p = matutils.maddval(_ScalePar._orignl(scc, scf, matx(p.matx[0][1:], False, True), const[1], True), p.mele(0, 0, False, True), False, True)
                            if p is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: const => (bool, bool)")
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: scale => bool")
            dic = {"parameters": p.matxl()[0], "iterations": c, }
            miscl = str(cls._misclassed(da, dic, const, True))
            if miscl is None:
                raise Exception
            dic.update({"misclassifications": miscl})
            dic.update({"parameters": [str(i) for i in dic["parameters"]]})
            return dic
        except Exception as e:
            Terminate.retrn(ret, e)


class LogReg(_Calculate, matx, Comp):
    
    @classmethod
    def grades(cls, d: data, p: list, a: float, m=100, pr=0.01, scale=False, const=(False, True), ret=False) -> dict:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = matx(p, True, True)
            if p is None or Comp.eqval(p.collen, 1) is None:
                raise Exception
            a = Comp.tdecimlp(a)
            if a is None:
                raise Exception
            pr = Comp.tdecimlp(pr)
            if pr is None:
                raise Exception
            m = Comp.tintn(m)
            if m is None:
                raise Exception
            if const == (True, True):
                if p.rowlen != d.xvars + 2:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
            elif const == (True, False) or const == (False, True):
                if p.rowlen != d.xvars + 1:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
            elif const == (False, False):
                if p.rowlen != d.xvars:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
            else:
                raise Exception("Invalid argument: const => (bool, bool)")
            return _Calculate._grades(d, p, a, m, pr, scale, const, ret=True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def gradesgc(cls, d: dict, p: dict, a: float, m=100, pr=0.01, scale=False, const=(False, True), ret=False) -> dict:
        try:
            if Comp.matchkeys(d, p) is None:
                raise Exception
            if Comp.lenlist([i["parameters"] for i in p.values()]) is None:
                raise Exception
            if Comp.tdata(list(d.values())) is None:
                raise Exception
            par = dict()
            for i in p.items():
                par[i[0]] = i[1]["parameters"]
            dic = dict()
            match scale:
                case False:
                    for i in d.items():
                        dic[i[0]] = cls.grades(i[1], par[i[0]], a, m, pr, False, const, True)
                    return dic
                case True:
                    for i in d.items():
                        dic[i[0]] = cls.grades(i[1], par[i[0]], a, m, pr, True, const, True)
                    return dic
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(ret, e)


# d = LogReg.grades(
#    data([[10, 10, 10], [5, 7, 9], [4, 2, 7], [5, 9, 1], [20, 20, 20], [21, 25, 22], [14, 18, 12], [12, 15, 11]],
#         [[0], [0], [0], [0], [1], [1], [1], [1]]), [1, -6, 1, 1, 1], 0.01, 1000, const=(True, True))
# print(d)
# print(Predict.y(d["parameters"], [5, 7, 9], const=(True, True)), Predict.y(d["parameters"], [14, 18, 12], const=(True, True)))
