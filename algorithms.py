import math
from decimal import Decimal
from matrix import matx, matutils, pwr
from data import data, datautils
from functions import poly, funcutils
from cmdexec import Terminate, Comp


class apn:
    def __init__(self, li: list | tuple | matx, chk=True, ret=False) -> None:
        try:
            apn = matx(li, chk, True)
            if apn is None:
                raise Exception
            if apn.rowlen != 2 or apn.collen != 1:
                raise Exception
            self.apn = apn
            if self.apn.mele(0, 1, False, True) == 0:
                self.dapn = None
            else:
                self.dapn = matx(tuple([self.apn.mele(0, 0, False, True) * self.apn.mele(0, 1, False, True), self.apn.mele(0, 1, False, True) - 1]), False, True)
            del apn
            self.val = lambda p: self.fval(p)
            self.dval = lambda p: self.fdval(p)
        except Exception as e:
            Terminate.retrn(ret, e)

    def fval(self, p: Decimal) -> Decimal:
        if self.apn.mele(0, 1, False, True) == 0:
            return self.apn.mele(0, 0, False, True)
        else:
            return self.apn.mele(0, 0, False, True) * pwr(Decimal(str(p)), self.apn.mele(0, 1, False, True))

    def fdval(self, p: Decimal) -> Decimal:
        if self.dapn.mele(0, 1, False, True) == 0:
            return self.dapn.mele(0, 0, False, True)
        else:
            return self.dapn.mele(0, 0, False, True) * pwr(Decimal(str(p)), self.dapn.mele(0, 1, False, True))


class parameter:
    def __init__(self, li: list | tuple, chk=True, ret=False) -> None:
        try:
            par = list()
            n = list()
            for i in li:
                par1 = list()
                for j in i:
                    par1.append(apn(j, chk, True))
                n.append(len(par1))
                par.append(tuple(par1))
            self.par = tuple(par)
            self.n = tuple(n)
            del par, n
            self.val = lambda p: tuple([matx(tuple([j.val(p[i[0]]) for j in i[1]]), False, True) for i in enumerate(self.par)])
            self.dval = lambda p: tuple([matx(tuple([j.dval(p[i[0]]) for j in i[1] if j.dapn is not None]), False, True) for i in enumerate(self.par)])
        except Exception as e:
            Terminate.retrn(ret, e)


class function:
    def __init__(self, li: tuple, chk=True, ret=False) -> None:
        try:
            match chk:
                case True:
                    for i in li:
                        if Comp.tmatx(i, True) is None:
                            raise Exception
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: chk => bool")
            self.x = li
            self.val = lambda p: matx(tuple([tuple([matutils.mmult(p[j[0]], matutils.tpose(j[1], False, True), False, True).matx[0][0] for j in enumerate(i)]) for i in self.x]), False, True)
            del li, i
        except Exception as e:
            Terminate.retrn(ret, e)


class _Predict(matutils):

    @staticmethod
    def _plinreggp(p: matx, p1: parameter, x: matx, const=False, ret=False) -> Decimal:
        try:
            match const:
                case True:
                    x = matutils.maddone(x, False, True)
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: const => bool")
            x = [matutils.tpose(i, False, True) for i in matutils.dpose(x, p1.n, chk=False, ret=True)]
            return sum([matutils.mmult(i[1], x[i[0]], False, True).matx[0][0] for i in enumerate(p1.val(p.matx[0]))])
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns predicted value of y for linear regression
    @classmethod
    def _plinreg(cls, p: matx, x: matx, const=False, ret=False) -> Decimal:
        try:
            return cls._plinreggp(p, parameter(tuple([((Decimal('1'), Decimal('1')),) for _ in range(p.rowlen)]), False, True), x, const, ret=True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns True for y=1 and False for y=0
    @staticmethod
    def _plogreggp(p: matx, p1: parameter, x: matx, const=False, ret=False) -> bool:
        try:
            match const:
                case True:
                    x = matutils.maddone(x, False, True)
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: const => bool")
            x = [matutils.tpose(i, False, True) for i in matutils.dpose(x, p1.n, chk=False, ret=True)]
            h = 1 / (1 + pwr(Decimal(str(math.e)), -1 * sum([matutils.mmult(i[1], x[i[0]], False, True).matx[0][0] for i in enumerate(p1.val(p.matx[0]))])))
            h = [h[0]*Decimal(d["phi"][0]), h[1]*Decimal(d["phi"][1])]
            if h is None:
                raise Exception
            if h < 0.5:
                return False
            else:
                return True
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def _plogreg(cls, p: matx, x: matx, const=False, ret=False) -> bool:
        try:
            return cls._plogreggp(p, parameter(tuple([((Decimal('1'), Decimal('1')),) for _ in range(p.rowlen)]), False, True), x, const, ret=True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns True for y=1 and False for y=0
    @staticmethod
    def _pgda(d: dict, x: matx, ret=False) -> bool:
        try:
            if d["n"] != x.rowlen:
                raise Exception(str(d["n"]) + " != " + str(x.rowlen))
            dif = [matutils.msub(x, matx(i, True, True), False, True) for i in d["mean"]]
            if dif is None:
                raise Exception
            cov = matx(d["cov"], True, True)
            if cov is None:
                raise Exception
            dn = pwr(Decimal(str(2 * math.pi)), Decimal(str(d["n"] / 2))) * pwr(matutils.dnant(cov, False, True), Decimal(str(1 / 2)))
            if dn is None:
                raise Exception
            h = [pwr(Decimal(str(math.e)), (
                matutils.mmult(matutils.mmult(i, matutils.invse(cov, False, True), False, True), matutils.tpose(i, False, True), False, True).matx[0][0]) / -2) / dn for i in dif]
            if h is None:
                raise Exception
            if h[0] > h[1]:
                return False
            else:
                return True
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns actual and predicted y
    @classmethod
    def _ypy(cls, d: tuple, p: matx, const=False, ret=False) -> list:
        try:
            return [[d[1][i].matx[0][0], cls._plinreg(p, d[0][i], const, True)] for i in range(len(d[1]))]
        except Exception as e:
            Terminate.retrn(ret, e)


class _Calculate(_Predict, matutils):

    # scale x values between [0, 1]
    @staticmethod
    def _scale0to1x(x: matx, ret=False) -> dict:
        try:
            x = matutils.tpose(x, False, True)
            mx = list()
            mn = list()
            for i in x.matx:
                mn.append(min(i))
            x = matutils.msub(x, matx(tuple([tuple([mn[i] for _ in range(x.rowlen)]) for i in range(x.collen)]), False, True), False, True)
            for i in x.matx:
                mx.append(max(i))
            x = tuple([matutils.smult(1 / mx[i[0]], i[1], False, True) for i in enumerate(matutils.matlxtox(x, False, True))])
            x = matutils.matlxtox(matutils.tpose(matutils.matxtolx(x, False, True), False, True), False, True)
            if x is None:
                raise Exception
            return {"constant": matx(tuple(mn), False, True), "factor": matx(tuple(mx), False, True), "values": x}
        except Exception as e:
            Terminate.retrn(ret, e)

    # scale x and y values between [0,1] for linear regression
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

    # scale parameter values for linear regression
    @staticmethod
    def _scalepar(c: matx, f: matx, p: matx, scale='0to1', ret=False) -> matx:
        try:
            c = matx(c, True, True)
            match scale:
                case '0to1':
                    pn = list()
                    p = matx(tuple([(1 / f.mele(0, -1, False, True)) * i for i in p.matx[0]]), False, True)
                    c = matx(tuple([c.mele(0, i, False, True) / f.mele(0, i, False, True) for i in range(c.rowlen)]),
                             False, True)
                    d = c.pop(c.rowlen - 1, False, False, True)[0]
                    for i in range(p.rowlen):
                        if i == 0:
                            pn.append(p.mele(0, i, False, True) + sum(c.matx[0]) - d)
                        else:
                            pn.append(p.mele(0, i, False, True) * f.mele(0, i - 1, False, True))
                    return matx(tuple(pn), False, True)
                case 'orignl':
                    pn = list()
                    c = matx(tuple([c.mele(0, i, False, True) / f.mele(0, i, False, True) for i in range(c.rowlen)]),
                             False, True)
                    d = c.pop(c.rowlen - 1, False, False, True)[0]
                    for i in range(p.rowlen):
                        if i == 0:
                            pn.append(p.mele(0, i, False, True) - sum(c.matx[0]) + d)
                        else:
                            pn.append(p.mele(0, i, False, True) * (1 / f.mele(0, i - 1, False, True)))
                    return matx(tuple([f.mele(0, -1, False, True) * i for i in pn]), False, True)
                case _:
                    raise Exception("Invalid argument: scale => '0to1'/'orignl'")
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns weights for weighted regression
    @staticmethod
    def _weights(d: tuple, xmt: tuple[matx, Decimal], ret=False) -> tuple:
        try:
            t = Comp.tdeciml(xmt[1])
            xm = xmt[0]
            if Comp.tmatx(xm) is None:
                raise Exception
            if t is None:
                raise Exception
            if d[0].rowlen != xm.rowlen:
                raise Exception(str(d[0].rowlen) + " != " + str(xm.rowlen))
            w = list()
            for i in d:
                w1 = matutils.msub(i, xm, False, True)
                w1 = matutils.mmult(w1, matutils.tpose(w1, False, True), False, True).matx[0][0]
                w.append(pwr(Decimal(str(math.e)), - w1 / pwr(t, 2)))
            return tuple(w)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns parameter using gradient descent for linear regression
    @staticmethod
    def _nextp(d: tuple, p: matx, a: Decimal, p1: parameter, w=None, reg='linreg', ret=False) -> matx:
        try:
            wt = w.__class__.__name__
            match reg:
                case 'linreg':
                    match wt:
                        case 'NoneType':
                            return matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.mmult(matutils.tpose(d[0].val(p1.dval(p.matx[0])), False, True), matutils.msub(matx(tuple([(sum(i),) for i in d[0].val(p1.val(p.matx[0])).matx]), False, True), d[1], False, True), False, True), False, True), False, True), False, True)
                        case 'tuple':
                            return matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.mmult(matutils.tpose(matutils.smultfac(w, d[0].val(p1.dval(p.matx[0])), chk=False, ret=True), False, True), matutils.msub(matx(tuple([(sum(i),) for i in d[0].val(p1.val(p.matx[0])).matx]), False, True), d[1], False, True), False, True), False, True), False, True), False, True)
                        case _:
                            raise Exception("Invalid argument: w => None/(weights, ...)")
                case 'logreg':
                    match wt:
                        case 'NoneType':
                            return matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.mmult(matutils.tpose(d[0].val(p1.dval(p.matx[0])), False, True), matutils.msub(matx(tuple([(1 / (1 + pwr(Decimal(str(math.e)), -sum(i))),) for i in d[0].val(p1.val(p.matx[0])).matx]), False, True), d[1], False, True), False, True), False, True), False, True), False, True)
                        case _:
                            raise Exception("Invalid argument: w => None")
                case _:
                    raise Exception("Invalid argument: reg => 'linreg'/'logreg'")
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns coefficient of determination for regression
    @classmethod
    def _coofdet(cls, d: tuple, p: matx, ret=False) -> Decimal:
        try:
            y = cls._ypy(d, p, ret=True)
            ym = sum([i.matx[0][0] for i in d[1]]) / len(d[1])
            ssr = sum([pwr((i[1] - ym), 2) for i in y])
            sst = sum([pwr((i[0] - ym), 2) for i in y])
            return ssr / sst
        except Exception as e:
            Terminate.retrn(ret, e)

    # misclassifications after classification
    @classmethod
    def _misclassed(cls, d: tuple, d1: dict, method='logreg', ret=False) -> dict:
        try:
            dic = dict()
            dic.setdefault("0", [0, 0, []])
            dic.setdefault("1", [0, 0, []])
            match method:
                # retuns misclassifications after logistic regression
                case 'logreg':
                    for i in range(len(d[1])):
                        if d[1][i].matx[0][0] == 0:
                            dic["0"][0] += 1
                            if cls._plogreg(matx(tuple(d1["parameters"]), False, True), d[0][i], True) is True:
                                dic["0"][1] += 1
                                dic["0"][2].append([str(j) for j in d[0][i].matxl()[0]])
                        else:
                            dic["1"][0] += 1
                            if cls._plogreg(matx(tuple(d1["parameters"]), False, True), d[0][i], True) is False:
                                dic["1"][1] += 1
                                dic["1"][2].append([str(j) for j in d[0][i].matxl()[0]])
                    return dic
                # returns misclassifications after gda
                case 'gda':
                    for i in range(len(d[1])):
                        if d[1][i].matx[0][0] == 0:
                            dic["0"][0] += 1
                            if cls._pgda(d1, d[0][i]) is True:
                                dic["0"][1] += 1
                                dic["0"][2].append([str(j) for j in d[0][i].matxl()[0]])
                        else:
                            dic["1"][0] += 1
                            if cls._pgda(d1, d[0][i]) is False:
                                dic["1"][1] += 1
                                dic["1"][2].append([str(j) for j in d[0][i].matxl()[0]])
                    return dic
                case _:
                    raise Exception("Invalid argument: method => 'logreg'/'gda'")
        except Exception as e:
            Terminate.retrn(ret, e)

    # performs regression using gradient descent
    @classmethod
    def _grades(cls, d: data, p: matx, a: Decimal, cfp: list | tuple, m: int, pr: Decimal, scale=False, weigh=False, xmt=None, reg='linreg', const=True, ret=False) -> dict:
        try:
            li = list()
            for i in cfp:
                li.append(len(i))
            p1 = parameter(cfp, ret=True)
            if p.collen != 1 or p.rowlen != len(p1.n):
                raise Exception("Check: p/cpf")
            match weigh:
                case False:
                    pass
                case True:
                    w = cls._weights(d.data[0], xmt, False)
                case _:
                    raise Exception("Invalid argument: weigh => bool")
            match scale:
                case True:
                    sc = cls._scale0to1(d, True)
                    if sc is None:
                        raise Exception
                    match const:
                        case True:
                            d = datautils.data1(sc["data"], True)
                        case False:
                            d = sc["data"]
                        case _:
                            raise Exception("Invalid argument: const => bool")
                    scc = sc["constant"]
                    scf = sc["factor"]
                    del sc
                    p = cls._scalepar(scc, scf, p, ret=True)
                    if p is None:
                        raise Exception
                case False:
                    match const:
                        case True:
                            d = datautils.data1(d, True)
                        case False:
                            pass
                        case _:
                            raise Exception("Invalid argument: const => bool")
                case _:
                    raise Exception("Invalid argument: scale => bool")
            d1 = (function(tuple([matutils.dpose(i, li, chk=False, ret=True) for i in d.data[0]]), True), d.getay())
            while (c := 0) < m:
                c += 1
                match reg:
                    case 'linreg':
                        match weigh:
                            case False:
                                pn = cls._nextp(d1, p, a, p1, ret=True)
                            case True:
                                pn = cls._nextp(d1, p, a, p1, w, ret=True)
                            case _:
                                raise Exception("Invalid argument: weigh => bool")
                    case 'logreg':
                        match weigh:
                            case False:
                                pn = cls._nextp(d1, p, a, p1, reg=reg, ret=True)
                            case _:
                                raise Exception("Invalid argument: weigh => bool")
                    case _:
                        raise Exception("Invalid argument: reg => 'linreg'/'logreg'")
                if pn is None:
                    raise Exception
                err = math.sqrt(sum([pwr((i[1] - p.mele(0, i[0], False, True)) / i[1], 2) for i in
                                     enumerate(pn.matx[0])]) / p.rowlen)
                if err < pr:
                    break
                p.matx = pn
                for i in range(pn.rowlen):
                    if pn.mele(0, i, False, True) == Decimal("nan") or pn.mele(0, i, False, True) == Decimal(
                            "inf") or pn.mele(0, i, False, True) == Decimal("-inf"):
                        raise Exception("parameter", i, "is ", pn.mele(0, i, False, True))
            match scale:
                case True:
                    p = cls._scalepar(scc, scf, p, 'orignl', True)
                    if p is None:
                        raise Exception
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: scale => bool")
            match reg:
                case 'linreg':
                    dic = dict()
                    dic["parameters"] = [str(i) for i in p.matxl()[0]]
                    dic["iterations"] = c
                    dic["r^2"] = str(cls._coofdet(d.data, p, True))
                    if dic["r^2"] is None:
                        raise Exception
                    try:
                        dic["r^2_adj"] = str(1 - ((1 - Decimal(dic["r^2"])) * (d.datalen - 1) / (d.datalen - d.xvars - 1)))
                    except ZeroDivisionError:
                        dic["r^2_adj"] = 'NaN'
                    return dic
                case 'logreg':
                    dic1 = {"parameters": p.matxl()[0], "iterations": c, }
                    miscl = str(cls._misclassed(d.data, dic1, ret=True))
                    if miscl is None:
                        raise Exception
                    dic1.update({"misclassifications": miscl})
                    dic1.update({"parameters": [str(i) for i in dic1["parameters"]]})
                    return dic1
                case _:
                    raise Exception("Invalid argument: reg => 'linreg'/'logreg'")
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def _hessianx(cls, x: matx, xt=None, ret=False) -> matx:
        try:
            xtt = xt.__class__.__name__
            match xtt:
                case 'NoneType':
                    x = matutils.matlxtox(matutils.tpose(x, False, True), False, True)
                    upr = list()
                    dia = list()
                    for i in range(len(x)):
                        upr1 = list()
                        dia1 = list()
                        for j in range(len(x)):
                            if j == i:
                                dia1.append(
                                    matutils.mmult(x[i], matutils.tpose(x[j], False, True), False, True).matx[0][0])
                                upr1.append(Decimal('0.0'))
                            elif j > i:
                                upr1.append(
                                    matutils.mmult(x[i], matutils.tpose(x[j], False, True), False, True).matx[0][0])
                                dia1.append(Decimal('0.0'))
                            else:
                                upr1.append(Decimal('0.0'))
                                dia1.append(Decimal('0.0'))
                        upr.append(tuple(upr1))
                        dia.append(tuple(dia1))
                case 'matx':
                    return matutils.mmult(matutils.tpose(xt, False, True), x, False, True)
                case _:
                    raise Exception("Invalid argument: xt => None/matx")
            upr = matx(tuple(upr), False, True)
            dia = matx(tuple(dia), False, True)
            return matutils.madd(dia, matutils.madd(upr, matutils.tpose(upr, False, True), False, True), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @staticmethod
    def _jacobiany(x: matx, y: matx, ret=False) -> matx:
        try:
            x = matutils.matlxtox(matutils.tpose(x, False, True), False, True)
            j = list()
            for i in x:
                j.append((matutils.mmult(i, y, False, True).matx[0][0],))
            return matx(tuple(j), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @staticmethod
    def _ulp(ut: matx, lt: matx, p: matx, c: matx, ret=False) -> matx:
        try:
            pn = list()
            for i in range(lt.collen):
                pn1 = 0
                for j in range(lt.rowlen):
                    if j < i:
                        pn1 += lt.mele(i, j, False, True) * p.mele(0, j, False, True)
                pn.append((pn1,))
            p = matutils.matlxtox(matutils.msub(matx(tuple(pn), False, True), c, False, True), False, True)
            for i in range(ut.collen):
                if i > 0:
                    pn.matx = matutils.addmatx(matutils.madd(matutils.mmult(pn, matx(tuple([(j,) for j in ut.mrow(ut.collen - 1 - i, False, True)[ut.collen - i:]]), False, True), False, True), p[-(i + 1)], False, True), pn, chk=False, ret=True)
                else:
                    pn = p[-1]
            return pn
        except Exception as e:
            Terminate.retrn(ret, e)

    @staticmethod
    def _lup(lt: matx, ut: matx, p: matx, c: matx, ret=False) -> matx:
        try:
            pn = list()
            for i in range(ut.collen):
                pn1 = 0
                for j in range(ut.rowlen):
                    if j > i:
                        pn1 += ut.mele(i, j, False, True) * p.mele(0, j, False, True)
                pn.append((pn1,))
            p = matutils.matlxtox(matutils.msub(matx(tuple(pn), False, True), c, False, True), False, True)
            for i in range(lt.collen):
                if i > 0:
                    pn.matx = matutils.addmatx(pn, matutils.madd(matutils.mmult(pn, matx(tuple([(j,) for j in lt.mrow(i, False, True)[:i]]), False, True), False, True), p[i], False, True), chk=False, ret=True)
                else:
                    pn = p[0]
            return pn
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def _linsys(cls, a: matx, b: matx, pmpr: tuple[matx, int, Decimal], method: str, ret=False) -> matx | tuple[matx, int]:
        try:
            match method:
                case 'inverse':
                    return matutils.mmult(matutils.tpose(b, False, True), matutils.invse(a, False, True), False, True)
                case 'uttform':
                    for i in range(a.collen):
                        an = list(a.matx)
                        bn = list(b.matx)
                        acol = matutils.gele(a, [i, ], False, False, True).matx[0]
                        acm = max([acol[j] for j in range(len(acol)) if j > i - 1])
                        for j in range(a.collen):
                            if a.mele(0, j, False, True) == acm:
                                an.insert(i, an.pop(j))
                                bn.insert(i, bn.pop(j))
                                break
                        a.matx = matx(tuple(an), False, True)
                        b.matx = matx(tuple(bn), False, True)
                        ai = a.mele(i, i, False, True)
                        if ai == 0:
                            raise Exception
                        for j in range(a.collen):
                            if j > i:
                                facx = -a.mele(j, i, False, True) / ai
                                a.matx = matutils.tform(a, j, i, facx, True, False, True)
                                b.matx = matutils.tform(b, j, i, facx, True, False, True)
                    p = matx((b.mele(b.collen - 1, 0, False, True) / a.mele(a.collen - 1, a.rowlen - 1),), False, True)
                    del an, acm, acol, facx, ai
                    for i in range(a.collen):
                        if i == 0:
                            continue
                        an = matx(tuple(
                            [(a.mele(a.collen - 1 - i, a.rowlen - 1 + j - i + 1, False, True),) for j in range(i)]),
                            False, True)
                        p.matx = matutils.addmatx(matutils.smult(1 / a.mele(a.collen - 1 - i, a.rowlen - 1 - i, False, True), matutils.msub(matx(b.mrow(b.collen - 1 - i, False, True), False, True), matutils.mmult(p, an, False, True), False, True), False, True), p, False, False, True)
                    del an
                    return p
                case 'gauseidel':
                    p = pmpr[0]
                    m = pmpr[1]
                    pr = pmpr[2]
                    for i in range(a.rowlen):
                        row = None
                        el = 0
                        ele = a.mele(i, i, False, True)
                        fac = [Decimal('1.0') for _ in range(a.collen - 1)]
                        if ele == 0:
                            for j in range(a.collen):
                                if j != i:
                                    el = a.mele(j, i, False, True)
                                    if el != 0:
                                        if row == None:
                                            row = j
                                        if math.fabs(el) < math.fabs(a.mele(row, i, False, True)):
                                            row = j
                            if row is None:
                                raise Exception
                            el = a.mele(row, i, False, True)
                            a.matx = matutils.tform(a, i, row, (-1) / el, True, False, True)
                            b.matx = matutils.tform(b, i, row, (-1) / el, True, False, True)
                        else:
                            fac.insert(i, -1 / ele)
                            a.matx = matutils.smultfac(tuple(fac), a, chk=False, ret=True)
                            b.matx = matutils.smultfac(tuple(fac), b, chk=False, ret=True)
                    a.matx = matutils.madd(a, matutils.idm(a.rowlen, False, True), False, True)
                    a = matutils.uldcompose(a, False, True)
                    ut = a[0]
                    lt = a[1]
                    del a
                    uts = 0
                    lts = 0
                    for i in range(ut.collen):
                        for j in range(lt.rowlen):
                            if j > i:
                                uts += ut.mele(i, j, False, True)
                            elif j < i:
                                lts += lt.mele(i, j, False, True)
                    if math.fabs(lts) > math.fabs(uts):
                        while (c := 0) < m:
                            c += 1
                            pn = cls._lup(lt, ut, p, b)
                            if pn is None:
                                raise Exception
                            err = math.sqrt(sum([pwr((i[1] - p.mele(0, i[0], False, True)) / i[1], 2) for i in
                                                 enumerate(pn.matx[0])]) / p.rowlen)
                            if err < pr:
                                break
                            p.matx = pn
                            for i in range(pn.rowlen):
                                if pn.mele(0, i, False, True) == float("nan") or pn.mele(0, i, False, True) == float(
                                        "inf") or pn.mele(0, i, False, True) == float("-inf"):
                                    raise Exception("parameter", i, "is ", pn.mele(0, i, False, True))
                    else:
                        while (c := 0) < m:
                            c += 1
                            pn = cls._ulp(ut, lt, p, b)
                            if pn is None:
                                raise Exception
                            err = math.sqrt(sum([pwr((i[1] - p.mele(0, i[0], False, True)) / i[1], 2) for i in
                                                 enumerate(pn.matx[0])]) / p.rowlen)
                            if err < pr:
                                break
                            p.matx = pn
                            for i in range(pn.rowlen):
                                if pn.mele(0, i, False, True) == float("nan") or pn.mele(0, i, False, True) == float(
                                        "inf") or pn.mele(0, i, False, True) == float("-inf"):
                                    raise Exception("parameter", i, "is ", pn.mele(0, i, False, True))
                    return p, c
                case 'tridia':
                    for i in range(int(a.rowlen / 2) + 1):
                        elea = a.mele(i + 1, i, False, True)
                        cola = a.mcol(i, False, True)
                        for j in range(a.collen):
                            if j > i + 1:
                                a.matx = cls.tform(a, j, i + 1, - cola[j] / elea, True, False, True)
                                b.matx = cls.tform(b, j, i + 1, - cola[j] / elea, True, False, True)
                        elec = a.mele(a.collen - 2 - i, a.rowlen - 1 - i, False, True)
                        colc = a.mcol(a.rowlen - 1 - i, False, True)
                        for j in range(a.collen):
                            if j < a.collen - 2 - i:
                                a.matx = cls.tform(a, j, a.collen - 2 - i, - colc[j] / elec, True, False, True)
                                b.matx = cls.tform(b, j, a.collen - 2 - i, - colc[j] / elec, True, False, True)
                    del elea, elec, cola, colc, j
                    x = a
                    y = matutils.tpose(b, False, True).matx[0]
                    a = list()
                    b = list()
                    c = list()
                    for i in range(x.collen):
                        if i == 0:
                            a.append(Decimal('0.0'))
                            b.append(x.mele(i, i, False, True))
                            c.append(x.mele(i, i + 1, False, True))
                        elif i == x.collen - 1:
                            a.append(x.mele(i, i - 1, False, True))
                            b.append(x.mele(i, i, False, True))
                            c.append(Decimal('0.0'))
                        else:
                            a.append(x.mele(i, i - 1, False, True))
                            b.append(x.mele(i, i, False, True))
                            c.append(x.mele(i, i + 1, False, True))
                    del x
                    theta = [Decimal('0.0'), ]
                    phi = [Decimal('0.0'), ]
                    for i in range(len(a)):
                        dn = (a[i] * theta[i]) + b[i]
                        theta.append(- c[i] / dn)
                        phi.append((y[i] - (a[i] * phi[i])) / dn)
                    theta.pop(0)
                    phi.pop(0)
                    p = [Decimal('0.0'), ]
                    for i in range(len(theta)):
                        p.insert(0, (p[0] * theta[-(i + 1)]) + phi[-(i + 1)])
                    p.pop(-1)
                    return matx(tuple(p), False, True)
                case _:
                    raise Exception("Invalid argument: method => 'inverse'/'uttform'/'gauseidel'/'tridia'")
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def _regmatrix(cls, d: data, pmpr: tuple[matx, int, Decimal], weigh=False, xmt=None, method='inverse', const=True, ret=False) -> dict:
        try:
            match weigh:
                # performs linear regression using matrix method
                case False:
                    match const:
                        case True:
                            d1 = datautils.data1(d, True)
                        case False:
                            d1 = d
                        case _:
                            raise Exception("Invalid argument: const=bool")
                    x = d1.getax()
                    y = d1.getay()
                    y.matx = cls._jacobiany(x, y, True)
                    x.matx = cls._hessianx(x, ret=True)
                # performs weighted linear regression using matrix method
                case True:
                    w = cls._weights(d.data[0], xmt, False)
                    if w is None:
                        raise Exception
                    d1 = datautils.data1(d)
                    y = d1.getay()
                    x = d1.getax()
                    xt = matutils.smultfac(w, x, True, False, True)
                    y.matx = cls._jacobiany(xt, y, True)
                    x.matx = cls._hessianx(x, xt, True)
                    del xt
                case _:
                    raise Exception("Invalid argument: weigh => bool")
            p = cls._linsys(x, y, pmpr, method, True)
            if p is None:
                raise Exception
            if method == 'gauseidel':
                dic = dict()
                dic["parameters"] = [str(i) for i in p[0].matxl()[0]]
                dic["iterations"] = p[1]
                dic["r^2"] = str(cls._coofdet(d1.data, p[0], True))
                if dic["r^2"] is None:
                    raise Exception
                try:
                    dic["r^2_adj"] = str(1 - ((1 - Decimal(dic["r^2"])) * (d1.datalen - 1) / (d1.datalen - d1.xvars - 1)))
                except ZeroDivisionError:
                    dic["r^2_adj"] = 'NaN'
                return dic
            dic = dict()
            dic["parameters"] = [str(i) for i in p.matxl()[0]]
            dic["r^2"] = str(cls._coofdet(d1.data, p, True))
            if dic["r^2"] is None:
                raise Exception
            try:
                dic["r^2_adj"] = str(1 - ((1 - Decimal(dic["r^2"])) * (d1.datalen - 1) / (d1.datalen - d1.xvars - 1)))
            except ZeroDivisionError:
                dic["r^2_adj"] = 'NaN'
            return dic
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns mean x and phi for GDA
    @staticmethod
    def _meanx_phi(d: tuple, ret=False) -> dict:
        try:
            y1 = 0
            y2 = 0
            lx = d[0][0].rowlen
            x1 = matutils.zerom(1, lx, False, True)
            x2 = matutils.zerom(1, lx, False, True)
            for i in range(len(d[1])):
                if d[1][i].mele(0, 0) == 0:
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
            xl = d[0][0].rowlen
            cov = matutils.zerom(xl, xl, False, True)
            for i in range(len(d[1])):
                if d[1][i].matx[0][0] == 0:
                    xd = matutils.msub(d[0][i], x1, False, True)
                    cov.matx = matutils.madd(cov, matutils.mmult(matutils.tpose(xd, False, True), xd, False, True), False, True)
                else:
                    xd = matutils.msub(d[0][i], x2, False, True)
                    cov.matx = matutils.madd(cov, matutils.mmult(matutils.tpose(xd, False, True), xd, False, True), False, True)
            return {"cov": matutils.smult(Decimal(str(1 / len(d[1]))), cov, False, True).matxl(), "n": xl}
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
            miscl = cls._misclassed(d, dic1, 'gda', True)
            if miscl is None:
                raise Exception
            dic1.setdefault("misclassifications", miscl)
            dic1.update({"mean": [[str(j) for j in i] for i in dic1["mean"]], "cov": [[str(j) for j in i] for i in dic1["cov"]], "phi": [str(i) for i in dic1["phi"]]})
            return dic1
        except Exception as e:
            Terminate.retrn(ret, e)


class LinReg(_Calculate):

    @staticmethod
    def gradesgp(d: data, p: list | matx, a: float, cpf: list | tuple, m=100, pr=0.01, scale=False, ret=False) -> dict:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = matx(p, True, True)
            if p is None:
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
            if p.rowlen != d.xvars + 1:
                raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
            r = _Calculate._grades(d, p, a, cpf, m, pr, scale=scale, ret=True)
            if r is None:
                raise Exception
            return r
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def grades(cls, d: data, p: list, a: float, m=100, pr=0.01, scale=False, ret=False) -> dict:
        try:
            p = matx(p, ret=True)
            if p is None:
                raise Exception
            return cls.gradesgp(d, p, a, [((1, 1),) for _ in range(p.rowlen)], m, pr, scale, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @staticmethod
    def matrix(d: data, p=None, m=100, pr=0.01, method='inverse', ret=False) -> dict:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            pr = Comp.tdecimlp(pr)
            if pr is None:
                raise Exception
            if p is not None:
                p = matx(p, ret=True)
                if p is None:
                    raise Exception
                if p.collen != 1 or p.rowlen != d.xvars + 1:
                    raise Exception(str(p.collen) + " != " + str(d.xvars + 1))
            r = _Calculate._regmatrix(d, (p, m, pr), method=method, ret=True)
            if r is None:
                raise Exception
            return r
        except Exception as e:
            Terminate.retrn(ret, e)


class WeiLinReg(_Calculate):

    @staticmethod
    def gradesgp(d: data, p: list | matx, a: float, cfp: list | tuple, x: list, t=float("inf"), m=100, pr=0.01, scale=False, ret=False) -> dict:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = matx(p, ret=True)
            if p is None:
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
            if p.rowlen != d.xvars + 1:
                raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
            x = matx(x, ret=True)
            if x.rowlen != d.xvars:
                raise Exception(str(x.rowlen) + " != " + str(d.xvars))
            t = Comp.tdeciml(t)
            if t is None:
                raise Exception
            r = _Calculate._grades(d, p, a, cfp, m, pr, scale, True, (x, t), ret=True)
            if r is None:
                raise Exception
            return r
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def grades(cls, d: data, p: list, a: float, x: list, t=float("inf"), m=100, pr=0.01, scale=False, ret=False) -> dict:
        try:
            p = matx(p, ret=True)
            if p is None:
                raise Exception
            return cls.gradesgp(d, p, a, [((1, 1),) for _ in range(p.rowlen)], x, t, m, pr, scale, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @staticmethod
    def matrix(d: data, x: list, t=float('inf'), p=None, m=100, pr=0.01, method='inverse', ret=False) -> dict:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            x = matx(x, ret=True)
            if x.rowlen != d.xvars:
                raise Exception(str(x.rowlen) + " != " + str(d.xvars))
            t = Comp.tdeciml(t)
            if t is None:
                raise Exception
            pr = Comp.tdecimlp(pr)
            if pr is None:
                raise Exception
            if p is not None:
                p = matx(p, ret=True)
                if p is None:
                    raise Exception
                if p.collen != 1 or p.rowlen != d.xvars + 1:
                    raise Exception(str(p.collen) + " != " + str(d.xvars + 1))
            r = _Calculate._regmatrix(d, (p, m, pr), True, (x, t), method=method, ret=True)
            if r is None:
                raise Exception
            return r
        except Exception as e:
            Terminate.retrn(ret, e)


class LogReg(_Calculate):

    @staticmethod
    def gradesgp(d: data, p: list | matx, a: float, cfp: list | tuple, m=100, pr=0.01, scale=False, ret=False) -> dict:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = matx(p, ret=True)
            if p is None:
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
            if p.rowlen != d.xvars + 1:
                raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
            r = _Calculate._grades(d, p, a, cfp, m, pr, scale, reg='logreg', ret=True)
            if r is None:
                raise Exception
            return r
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def grades(cls, d: data, p: list, a: float, m=100, pr=0.01, scale=False, ret=False) -> dict:
        try:
            p = matx(p, ret=True)
            if p is None:
                raise Exception
            return cls.gradesgp(d, p, a, [((1, 1),) for _ in range(p.rowlen)], m, pr, scale, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def gradesgc(cls, d: dict, p: dict, a: float, m=100, pr=0.01, scale=False, ret=False) -> dict:
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
                        dic[i[0]] = cls.grades(i[1], par[i[0]], a, m, pr, False, True)
                    return dic
                case True:
                    for i in d.items():
                        dic[i[0]] = cls.grades(i[1], par[i[0]], a, m, pr, True, True)
                    return dic
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(ret, e)


class GDA(_Calculate):
    
    @classmethod
    def gda(cls, d: data, ret=False) -> dict:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            return cls._gda(d, True)
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


class Predict(_Predict):
    
    @classmethod
    def ylinreg(cls, d: data, p: list, const=True, ret=False) -> matx:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = matx(p, ret=True)
            if p is None:
                raise Exception
            if p.rowlen != d.xvars + 1:
                raise Exception(str(p.rowlen) + " != " + str(d.xvars + 1))
            return matx(tuple([tuple(i) for i in cls._ypy(d.data, p, const, True)]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def linreg(cls, p: list, x: list, const=True, ret=False) -> Decimal:
        try:
            p = matx(p, ret=True)
            if p is None:
                raise Exception
            x = matx(x, ret=True)
            if x.rowlen + 1 != p.rowlen:
                raise Exception(str(p.rowlen) + " != " + str(x.rowlen + 1))
            return cls._plinreg(p, x, const, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def logreg(cls, p: list, x: list, const=True, ret=False) -> int:
        try:
            p = matx(p, ret=True)
            if p is None:
                raise Exception
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            if x.rowlen + 1 != p.rowlen:
                raise Exception(str(p.rowlen) + " != " + str(x.rowlen + 1))
            y = cls._plogreg(p, x, const, True)
            if y is True:
                return 1
            else:
                return 0
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def gda(cls, d: dict, x: list, ret=False) -> int:
        try:
            if Comp.tdict(d) is None:
                raise Exception
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            if d["n"] != x.rowlen:
                raise Exception(str(x.rowlen) + " != " + str(d["n"]))
            y = cls._pgda(d, x, True)
            if y is True:
                return 1
            else:
                return 0
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def logreggc(cls, d: dict, x: list, ret=False) -> int:
        try:
            if Comp.tdict(d) is None:
                raise Exception
            c = dict()
            for i in d.items():
                cl = cls.logreg(i[1]["parameters"], x, True)
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

    @classmethod
    def gdagc(cls, d: dict, x: list, ret=False) -> int:
        try:
            if Comp.tdict(d) is None:
                raise Exception
            c = dict()
            for i in d.items():
                cl = cls.gda(i[1], x, True)
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


class SolveFn(funcutils, matutils):
    
    @staticmethod
    def rootrre(fn: tuple, pos: float, x: list | matx, m=100, pr=0.01, fnt='poly', ret=False) -> dict:
        try:
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            if x.collen != 1:
                raise Exception(str(x.collen) + " != 1")
            pos = Comp.tint(pos)
            if pos is None:
                raise Exception
            match fnt:
                case 'poly':
                    p = matutils.addmatx(matx(fn[0], ret=True), matx(fn[1], ret=True), True, True, True)
                    if p is None:
                        raise Exception
                    if p.collen != 2:
                        raise Exception
                    p = poly(p, True)
                    if p is None:
                        raise Exception
            xre = funcutils.rearr(p, pos, True)
            if xre is None:
                raise Exception
            xn = list()
            for i in x.matx[0]:
                try:
                    dxre = math.fabs(xre.dval(i))
                    if dxre < 0:
                        if dxre < -1:
                            continue
                    if dxre > 0:
                        if dxre > 1:
                            continue
                    xn.append(i)
                except ArithmeticError:
                    continue
                except TypeError:
                    continue
            if len(xn) == 0:
                raise Exception
            value = dict()
            for i in xn:
                xi = i
                c = 0
                while c < m:
                    c += 1
                    val = xre.val(xi)
                    valy = p.val(val)
                    if str(valy) == 'NaN':
                        break
                    if math.fabs(valy) < pr or c == m:
                        value[str(i)] = (str(val), c, )
                        break
                    else:
                        xi = val
            return value
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @staticmethod
    def lininter(fn: tuple, x: list | matx, m=100, pr=0.01, fnt='poly', ret=False) -> dict:
        try:
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            if x.rowlen != 2:
                raise Exception(str(x.rowlen) + " != 2")
            x = matutils.matlxtox(x, False, True)
            match fnt:
                case 'poly':
                    p = matutils.addmatx(matx(fn[0], ret=True), matx(fn[1], ret=True), True, True, True)
                    if p is None:
                        raise Exception
                    if p.collen != 2:
                        raise Exception
                    p = poly(p, True)
                    if p is None:
                        raise Exception
            value = dict()
            for i in x:
                c = 0
                p1 = (i.mele(0, 0, False, True), p.val(i.mele(0, 0, False, True)))
                p2 = (i.mele(0, 1, False, True), p.val(i.mele(0, 1, False, True)))
                if p1[1]*p2[1] < 0:
                    while c < m:
                        c += 1
                        valx = (((p1[0] - p2[0]) * (- p1[1])) / (p1[1] - p2[1])) + p1[0]
                        p3 = (valx, p.val(valx))
                        if str(p3[1]) == 'NaN':
                            break
                        if math.fabs(p3[1]) < pr or c == m:
                            value[str(i.matx[0])] = (str(p3[0]), c, )
                            break
                        if p1[1]*p3[1] < 0:
                            p2 = p3
                        else:
                            p1 = p3
            return value
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @staticmethod
    def bchop(fn: tuple, x: list | matx, m=100, pr=0.01, fnt='poly', ret=False) -> dict:
        try:
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            if x.rowlen != 2:
                raise Exception(str(x.rowlen) + " != 2")
            x = matutils.matlxtox(x, False, True)
            match fnt:
                case 'poly':
                    p = matutils.addmatx(matx(fn[0], ret=True), matx(fn[1], ret=True), True, True, True)
                    if p is None:
                        raise Exception
                    if p.collen != 2:
                        raise Exception
                    p = poly(p, True)
                    if p is None:
                        raise Exception
            value = dict()
            for i in x:
                c = 0
                p1 = (i.mele(0, 0, False, True), p.val(i.mele(0, 0, False, True)))
                p2 = (i.mele(0, 1, False, True), p.val(i.mele(0, 1, False, True)))
                if p1[1]*p2[1] < 0:
                    while c < m:
                        c += 1
                        mid = (p1[0] + p2[0]) / 2
                        p3 = (mid, p.val(mid))
                        if str(p3[1]) == 'NaN':
                            break
                        if math.fabs(p3[1]) < pr or c == m:
                            value[str(i.matx[0])] = (str(p3[0]), c, )
                            break
                        if p1[1]*p3[1] < 0:
                            p2 = p3
                        else:
                            p1 = p3
            return value
        except Exception as e:
            Terminate.retrn(ret, e)

    @staticmethod
    def nrinter(fn: tuple, x: list | matx, m=100, pr=0.01, fnt='poly', ret=False) -> dict:
        try:
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            if x.collen != 1:
                raise Exception(str(x.collen) + " != 1")
            match fnt:
                case 'poly':
                    p = matutils.addmatx(matx(fn[0], ret=True), matx(fn[1], ret=True), True, True, True)
                    if p is None:
                        raise Exception
                    if p.collen != 2:
                        raise Exception
                    p = poly(p, True)
                    if p is None:
                        raise Exception
            value = dict()
            for i in x.matx[0]:
                while (c := 0) < m:
                    nx = i - (p.val(i) / p.dval(i))
                    if p.val(nx) < pr:
                        value[str(i)] = (str(nx), c, )
                        break
            return value
        except Exception as e:
            Terminate.retrn(ret, e)

# print('1')
# b = LinReg.matrix(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), method='inverse')
# print(b)
# b = LinReg.matrix(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), method='tridia')
# print(b)
# b = LinReg.matrix(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), [1,1,1,1], pr=0.01, method='gauseidel')
# print(b)
# b = LinReg.grades(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]),
#                    [0, 1, 1, 1], 0.01, 100, scale=True, ret=True)
# print(b)
# a = 0.00196
# b = LinReg.grades(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), [0, 1, 1, 1], a, 1000, 0.01, ret=True)
# print(b)
# print(Predict.linreg(b["parameters"], [2,3,6]))
# print('2')
# c = WeiLinReg.matrix(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), [2, 6, 4])
# print(c)
# c = WeiLinReg.grades(
#    data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), [1, 1, 1, 1],
#    0.01, [2, 4, 6], scale=True)
# print(c)
# d = LogReg.grades(
#    data([[10, 10, 10], [5, 7, 9], [4, 2, 7], [5, 9, 1], [20, 20, 20], [21, 25, 22], [14, 18, 12], [12, 15, 11]],
#         [[0], [0], [0], [0], [1], [1], [1], [1]]), [-10, 1, 1, 1], 0.01, 1000)
# print(d)
# print(Predict.logreg(d["parameters"], [5, 7, 9]), Predict.logreg(d["parameters"], [14, 18, 12]))
# a = GDA.gda(
#    data([[10, 10, 10], [5, 7, 9], [4, 2, 7], [5, 9, 1], [20, 20, 20], [21, 25, 22], [14, 18, 12], [12, 15, 11]],
#         [[0], [0], [0], [0], [1], [1], [1], [1]]))
# print(a)

# for j in range(1):
#     d = {'Al_LowCutoff': {'parameters': [16.058881741715595, -8.955601539113559, 1.0939627709012711],
#                           'r^2': 0.9983192621607382, 'r^2_adj': 0.9978390513495206},
#         'Al_HighCutoff': {'parameters': [15.811508555198088, -8.971596025396138, 1.1032308384019416],
#                            'r^2': 0.998828056926424, 'r^2_adj': 0.9984932160482594},
#          'Al_MedCutoff': {'parameters': [15.946995875099674, -9.0157831403194, 1.107305156358052],
#                           'r^2': 0.9988916677797752, 'r^2_adj': 0.9985750014311395}}
#     p = dict()
#     for i in d.items():
#         p[i[0]] = poly(matx([i[1]["parameters"], [0, 1, 2]]), True)
#     for i in p.items():
#         p[i[0]] = funcutils.polytoan(funcutils.ndpoly(i[1], True))
#     for i in p.items():
#         p[i[0]] = SolveFn.nrinter(i[1], [-10, 0, 10], 1000, 0.001)
#     print(p)
#     p = SolveFn.rootrre(([4, -4, 1], [0, 1, 2]), 2, [i - 5 for i in range(10)], 1000, 0.001)
#     print(p)
