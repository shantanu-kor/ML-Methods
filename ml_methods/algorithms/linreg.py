# import os, sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decimal import Decimal
import math
from cmdexec import Terminate
from utils import Comp
from matrix import matx, matutils, pwr
from data import data, datautils
from algoutils import parameter, Scale, Calculate
from linsys import Method


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


class _Predict(parameter, matutils, matx):

    @classmethod
    def _pygp(cls, x: matx, p: matx, p1: parameter, const=(False, True), ret=False) -> Decimal:
        try:
            match const[1]:
                case True:
                    x = matutils.maddval(x, Decimal('1.0'), False, True)
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            x = [matutils.tpose(i, False, True) for i in matutils.dpose(x, p1.n, chk=False, ret=True)]
            match const[0]:
                case False:
                    return sum([matutils.mmult(i[1], x[i[0]], False, True).matx[0][0] for i in enumerate(p1.val(p))])
                case True:
                    p = matx(p, False, True)
                    p0 = p.pop(0, False, False, True)[0]
                    return p0 * sum([matutils.mmult(i[1], x[i[0]], False, True).matx[0][0] for i in enumerate(p1.val(p))])
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def _pallygp(cls, x: matx, p: matx, p1: parameter, const: tuple[bool, bool], ret=False) -> matx:
        try:
            match const[1]:
                case False:
                    pass
                case True:
                    x = matutils.maddval(x, Decimal('1.0'), False, True)
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            x = function(matutils.dpose(x, p1.n, False, False, True), False, True)
            match const[0]:
                case False:
                    p = p1.val(p)
                    return matutils.tpose(matutils.addmel(x.val(p), [[i for i in range(len(p1.n))], ], False, False, True), False, True)
                case True:
                    p = matx(p, False, True)
                    p0 = p.pop(0, False, False, True)
                    return matutils.smult(p0, matutils.tpose(matutils.addmel(x.val(p), [[i for i in range(len(p1.n))], ], False, False, True), False, True), False, True)
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
        except Exception as e:
            Terminate.retrn(ret, e)
    
    # returns predicted value of y for linear regression
    @classmethod
    def _py(cls, x: matx, p: matx, const: tuple[bool, bool], ret=False) -> Decimal:
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
                    return matutils.mmult(p, matutils.tpose(x, False, True), False, True).matx[0][0]
                case True:
                    p = matx(p, False, True)
                    p0 = p.pop(0, False, False, True)[0]
                    return p0 * matutils.mmult(p, matutils.tpose(x, False, True), False, True).matx[0][0]
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
        except Exception as e:
            Terminate.retrn(ret, e)
    
    # returns actual and predicted y
    @classmethod
    def _pally(cls, x: matx, p: matx, const: tuple[bool, bool], ret=False) -> matx:
        try:
            match const[1]:
                case False:
                    match const[0]:
                        case False:
                            return matutils.tpose(matutils.mmult(p, matutils.tpose(x), False, True))
                        case True:
                            p = matx(p, False, True)
                            p0 = p.pop(0, False, False, True)[0]
                            return matutils.tpose(matutils.smult(p0, matutils.mmult(p, matutils.tpose(x), False, True), False, True))
                        case _:
                            raise Exception("Invalid argument: const => (bool, bool)")
                case True:
                    match const[0]:
                        case False:
                            return matutils.tpose(matutils.mmult(p, matutils.tpose(matutils.maddval(x, Decimal('1.0'), False, True)), False, True))
                        case True:
                            p = matx(p, False, True)
                            p0 = p.pop(0, False, False, True)[0]
                            return matutils.tpose(matutils.smult(p0, matutils.mmult(p, matutils.tpose(matutils.maddval(x, Decimal('1.0'), False, True)), False, True), False, True))
                        case _:
                            raise Exception("Invalid argument: const => (bool, bool)")
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
        except Exception as e:
            Terminate.retrn(ret, e)


class PLinReg(_Predict, parameter, matx, Comp):
    
    @classmethod
    def allygp(cls, d: data, p: list, cfp: list[list[list]] | tuple[tuple[tuple[float | Decimal | int, float | Decimal | int], ...], ...], const=(False, True), ret=False) -> matx:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = matx(p, ret=True)
            if p is None:
                raise Exception
            p1 = parameter(cfp, True, True)
            if p1 is None:
                raise Exception
            match const:
                case (True, True):
                    if sum(p1.n) != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
                    if Comp.eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, True):
                    if sum(p1.n) != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    if Comp.eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case (True, False):
                    if sum(p1.n) != d.xvars:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    if Comp.eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, False):
                    if sum(p1.n) != d.xvars:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
                    if Comp.eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._pallygp(d.getax(), p, p1, const, True)
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def ygp(cls, x: list, p: list, cfp: list[list[list]] | tuple[tuple[tuple[float | Decimal | int, float | Decimal | int], ...], ...], const=(False, True), ret=False) -> Decimal:
        try:
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            p = matx(p, ret=True)
            if p is None:
                raise Exception
            p1 = parameter(cfp, True, True)
            if p1 is None:
                raise Exception
            match const:
                case (True, True):
                    if sum(p1.n) != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                    if Comp.eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, True):
                    if sum(p1.n) != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                    if Comp.eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case (True, False):
                    if sum(p1.n) != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                    if Comp.eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, False):
                    if sum(p1.n) != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                    if Comp.eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._pygp(x, p, p1, const, True)
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def ally(cls, d: data, p: list, const=(False, True), ret=False) -> matx:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = matx(p, ret=True)
            if p is None:
                raise Exception
            match const:
                case (True, True):
                    if p.rowlen != d.xvars + 2:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
                case (False, True):
                    if p.rowlen != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                case (True, False):
                    if p.rowlen != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                case (False, False):
                    if p.rowlen != d.xvars:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._pally(d.getax(), p, const, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def y(cls, x: list, p: list, const=(False, True), ret=False) -> Decimal:
        try:
            p = matx(p, ret=True)
            if p is None:
                raise Exception
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            match const:
                case (True, True):
                    if p.rowlen != x.rowlen + 2:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                case (False, True):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (True, False):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (False, False):
                    if p.rowlen != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._py(p, x, const, True)
        except Exception as e:
            Terminate.retrn(ret, e)


class _ScalePar(matutils, matx):

    # scale parameter values for linear regression
    @classmethod
    def _0to1(cls, c: matx, f: matx, p: matx, const=True, ret=False) -> matx:
        try:
            c = matx(c, False, True)
            f = matx(f, False, True)
            match const:
                case True:
                    g = f.pop(-1, False, False, True)[0]
                    d = c.pop(-1, False, False, True)[0] / g
                    p = matutils.smult(1 / g, p, False, True)
                    p0 = (p.pop(0, False, False, True)[0] + sum(matutils.smultfac(p.matx[0], c, False, False, True).matx[0]) - d, )
                    p = p0 + matutils.smultfac(f.matx[0], p, False, False, True).matx[0]
                    return matx(p, False, True)
                case False:
                    p = matutils.smult(1 / f.pop(-1, False, False, True)[0], p, False, True)
                    p = matutils.smultfac(f.matx[0], p, False, False, True).matx[0]
                    return matx(p, False, True)
                case _:
                    raise Exception("Invalid argument: const => bool")
        except Exception as e:
            Terminate.retrn(ret, e)


    @classmethod
    def _orignl(cls, c: matx, f: matx, p: matx, const=True, ret=False) -> matx:
        try:
            c = matx(c, False, True)
            f = matx(f, False, True)
            match const:
                case True:
                    p = matutils.smult(f.pop(-1, False, False, True)[0], p, False, True)
                    p0 = p.pop(0, False, False, True)[0] + c.pop(-1, False, False, True)[0]
                    p = matutils.smultfac(tuple([1 / i for i in f.matx[0]]), p, False, False, True)
                    p0 -= matutils.mmult(p, matutils.tpose(c, False, True), False, True).matx[0][0]
                    return matx((p0, ) + p.matx[0], False, True)
                case False:
                    p = matutils.smult(f.pop(-1, False, False, True)[0], p, False, True)
                    p = matutils.smultfac(tuple([1 / i for i in f.matx[0]]), p, False, False, True)
                    return matx(p, False, True)
                case _:
                    raise Exception("Invalid argument: const => bool")
        except Exception as e:
            Terminate.retrn(ret, e)


class _Calculate(_Predict, _ScalePar, Method, Scale, matutils, Calculate, matx):

    # returns weights for weighted regression
    @classmethod
    def _weights(cls, xd: matx, xmt: tuple[matx, Decimal], ret=False) -> matx:
        try:
            return matutils.expomel([Decimal(str(math.e)), - 1 / pwr(xmt[1], 2, False, True)], matutils.matxtolx([matutils.mmult(j, matutils.tpose(j, False, True), False, True) for j in [matutils.msub(i, xmt[0], False, True) for i in matutils.matlxtox(xd, False, True)]]), [0, ], False, False, True)
        except Exception as e:
            Terminate.retrn(ret, e)
    
    # returns coefficient of determination for regression
    @classmethod
    def _coofdet(cls, d: tuple, p: matx, const: tuple[bool, bool], ret=False) -> Decimal:
        try:
            y = _Predict._pally(d[0], p, const, ret=True)
            ym = matutils.addmel(d[1], [[i for i in range(d[1].collen)], ], True, False, True).matx[0][0] / d[1].collen
            ssr = sum([pwr((i[0] - ym), 2, False, True) for i in y.matx])
            sst = sum([pwr((i[0] - ym), 2, False, True) for i in d[1].matx])
            return ssr / sst
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def _linreg(cls, d: tuple, p: matx, a, m, pr, const: tuple[bool, bool], ret=False) -> tuple[matx, int]:
        try:
            const = const[0]
            c = 0
            while (c := c + 1) <= m:
                match const:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.mmult(d[0], matutils.tpose(matutils.msub(matutils.mmult(p, d[0], False, True), d[1], False, True), False, True), False, True), False, True), False, True), False, True)
                    case True:
                        p1 = matx(p, False, True)
                        p0 = p1.pop(0, False, False, True)[0]
                        dm = matutils.tpose(matutils.msub(matutils.smult(p0, matutils.mmult(p1, d[0], False, True), False, True), d[1], False, True), False, True)
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.addmatx(matutils.mmult(matutils.mmult(p1, d[0], False, True), dm, False, True), matutils.mmult(matutils.smult(p0, d[0], False, True), dm, False, True), True, False, True), False, True), False, True), False, True)
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")        
                if pn is None:
                    raise Exception
                err = Calculate._cmperrpr(p, pn, pr, True)
                match err:
                    case True:
                        return pn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, c - 1
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def _linregsp(cls, d: tuple, p: matx, a, m, pr, cf: tuple[matx, matx], const: tuple[bool, bool], ret=False) -> tuple[matx, int]:
        try:
            scc = cf[0]
            scf = cf[1]
            if const[1] is True:
                cn = matx(scc.matx[0][:-1] + (Decimal('0.0'), ), False, True)
            c = 0
            while (c := c + 1) <= m:
                match const[0]:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.mmult(d[0], matutils.tpose(matutils.msub(matutils.mmult(p, d[0], False, True), d[1], False, True), False, True), False, True), False, True), False, True), False, True)
                    case True:
                        p1 = matx(p, False, True)
                        p0 = p1.pop(0, False, False, True)[0]
                        dm = matutils.tpose(matutils.msub(matutils.smult(p0, matutils.mmult(p1, d[0], False, True), False, True), d[1], False, True), False, True)
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.addmatx(matutils.mmult(matutils.mmult(p1, d[0], False, True), dm, False, True), matutils.mmult(matutils.smult(p0, d[0], False, True), dm, False, True), True, False, True), False, True), False, True), False, True)
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
                        match const[1]:
                            case False:
                                op = matutils.maddval(_ScalePar._orignl(scc, scf, matx(p.matx[0][1:], False, True), False, True), p.mele(0, 0, False, True), False, True)
                                opn = matutils.maddval(_ScalePar._orignl(scc, scf, matx(pn.matx[0][1:], False, True), False, True), p.mele(0, 0, False, True), False, True)
                                if op is None or opn is None:
                                    raise Exception
                            case True:
                                op = matutils.maddval(_ScalePar._orignl(cn, scf, matx(p.matx[0][1:], False, True), True, True), p.mele(0, 0, False, True), False, True)
                                opn = matutils.maddval(_ScalePar._orignl(cn, scf, matx(pn.matx[0][1:], False, True), True, True), p.mele(0, 0, False, True), False, True)
                                if op is None or opn is None:
                                    raise Exception
                            case _:
                                raise Exception("Invalid argument: const => (bool, bool)")
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                err = Calculate._cmperrpr(op, opn, pr, True)
                match err:
                    case True:
                        return pn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, c - 1
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def _weilinreg(cls, d: tuple, p: matx, a, m, pr, w: matx, const: tuple[bool, bool], ret=False) -> tuple[matx, int]:
        try:
            w = w.matx[0]
            c = 0
            while (c := c + 1) <= m:
                match const[0]:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.mmult(matutils.smultfac(w, d[0], False, False, True), matutils.tpose(matutils.msub(matutils.mmult(p, d[0], False, True), d[1], False, True), False, True), False, True), False, True), False, True), False, True)
                    case True:
                        p1 = matx(p, False, True)
                        p0 = p1.pop(0, False, False, True)[0]
                        dm = matutils.tpose(matutils.msub(matutils.smult(p0, matutils.mmult(p1, d[0], False, True), False, True), d[1], False, True), False, True)
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.addmatx(matutils.mmult(matutils.smultfac(w, matutils.mmult(p1, d[0], False, True), False, False, True), dm, False, True), matutils.mmult(matutils.smult(p0, matutils.smultfac(w, d[0], False, False, True), False, True), dm, False, True), True, False, True), False, True), False, True), False, True)
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                if pn is None:
                    raise Exception
                err = Calculate._cmperrpr(p, pn, pr, True)
                match err:
                    case True:
                        return pn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, c - 1
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def _weilinregsp(cls, d: tuple, p: matx, a, m, pr, w: matx, cf: tuple[matx, matx], const: tuple[bool, bool], ret=False) -> tuple[matx, int]:
        try:
            scc = cf[0]
            scf = cf[1]
            if const[1] is True:
                cn = matx(scc.matx[0][:-1] + (Decimal('0.0'), ), False, True)
            w = w.matx[0]
            c = 0
            while (c := c + 1) <= m:
                match const[0]:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.mmult(matutils.smultfac(w, d[0], False, False, True), matutils.tpose(matutils.msub(matutils.mmult(p, d[0], False, True), d[1], False, True), False, True), False, True), False, True), False, True), False, True)
                    case True:
                        p1 = matx(p, False, True)
                        p0 = p1.pop(0, False, False, True)[0]
                        dm = matutils.tpose(matutils.msub(matutils.smult(p0, matutils.mmult(p1, d[0], False, True), False, True), d[1], False, True), False, True)
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.addmatx(matutils.mmult(matutils.smultfac(w, matutils.mmult(p1, d[0], False, True), False, False, True), dm, False, True), matutils.mmult(matutils.smult(p0, matutils.smultfac(w, d[0], False, False, True), False, True), dm, False, True), True, False, True), False, True), False, True), False, True)
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
                        match const[1]:
                            case False:
                                op = matutils.maddval(_ScalePar._orignl(scc, scf, matx(p.matx[0][1:], False, True), False, True), p.mele(0, 0, False, True), False, True)
                                opn = matutils.maddval(_ScalePar._orignl(scc, scf, matx(pn.matx[0][1:], False, True), False, True), p.mele(0, 0, False, True), False, True)
                                if op is None or opn is None:
                                    raise Exception
                            case True:
                                op = matutils.maddval(_ScalePar._orignl(cn, scf, matx(p.matx[0][1:], False, True), True, True), p.mele(0, 0, False, True), False, True)
                                opn = matutils.maddval(_ScalePar._orignl(cn, scf, matx(pn.matx[0][1:], False, True), True, True), p.mele(0, 0, False, True), False, True)
                                if op is None or opn is None:
                                    raise Exception
                            case _:
                                raise Exception("Invalid argument: const => (bool, bool)")
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                err = Calculate._cmperrpr(op, opn, pr, True)
                match err:
                    case True:
                        return pn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, c - 1
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def _grades(cls, d: data, p: matx, a: Decimal, m: int, pr: Decimal, scale=False, xmt=None, const=(False, True), ret=False) -> dict:
        try:
            da = d
            txmt  = xmt.__class__.__name__
            match scale:
                case True:
                    sc = Scale._scale0to1(d, True)
                    if sc is None:
                        raise Exception
                    d = sc["data"]
                    scc = sc["constant"]
                    scf = sc["factor"]
                    del sc
                    match txmt:
                        case 'NoneType':
                            pass
                        case 'tuple':
                            w = cls._weights(matutils.smultfac(scf.matx[0][:-1], d.data[0], False, False, True), (matutils.msub(xmt[0], matx(scc.matx[0][:-1], False, True), False, True), xmt[1]), True)
                        case _:
                            raise Exception("Invalid argument: xmt => None/tuple")
                    match const[1]:
                        case False:
                            c = matutils.smultfac([1 / i for i in scf.matx[0]], scc, False, False, True)
                            cy = c.pop(-1, False, False, True)
                            d = data(matutils.saddcnst(c.matx[0], d.getax(), False, False, True), matutils.saddcnst(cy, d.getay(), False, False, True), False, True)
                        case True:
                            match const[0]:
                                case True:
                                    d = data(matutils.maddval(d.getax(), Decimal('1.0'), False, True), matutils.saddcnst((scc.mele(0, -1, False, True) / scf.mele(0, -1, False, True), ), d.getay(), False, False, True), False, True)
                                case False:
                                    d = datautils.dataval(d, Decimal('1.0'), False, True)
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
                            match const[1]:
                                case False:
                                    p = matutils.maddval(_ScalePar._0to1(scc, scf, matx(p.matx[0][1:], False, True), False, True), p.mele(0, 0, False, True), False, True)
                                    if p is None:
                                        raise Exception
                                case True:
                                    p = matutils.maddval(_ScalePar._0to1(matx(scc.matx[0][:-1] + (Decimal('0.0'), ), False, True), scf, matx(p.matx[0][1:], False, True), True, True), p.mele(0, 0, False, True), True, True)
                                    if p is None:
                                        raise Exception
                                case _:
                                    raise Exception("Invalid argument: const => (bool, bool)")
                        case _:
                            raise Exception("Invalid argument: const => (bool, bool)")
                case False:
                    match txmt:
                        case 'NoneType':
                            pass
                        case 'tuple':
                            w = cls._weights(d.data[0], xmt, True)
                        case _:
                            raise Exception("Invalid argument: xmt => None/tuple")
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
                    match txmt:
                        case 'NoneType':
                            pn = cls._linregsp(d1, p, a, m, pr, (scc, scf), const, True)
                        case 'tuple':
                            pn = cls._weilinregsp(d1, p, a, m, pr, w, (scc, scf), const, True)
                        case _:
                            raise Exception("Invalid argument: xmt => None/tuple")
                case False:
                    match txmt:
                        case 'NoneType':
                            pn = cls._linreg(d1, p, a, m, pr, const, True)
                        case 'tuple':
                            pn = cls._weilinreg(d1, p, a, m, pr, w, const, True)
                        case _:
                            raise Exception("Invalid argument: xmt => None/tuple")
                case _:
                    raise Exception("Invalid argument: scale => bool")
            if pn is None:
                raise Exception
            p = pn[0]
            c = pn[1]
            del pn
            match scale:
                case True:
                    match const[0]:
                        case False:
                            p = _ScalePar._orignl(scc, scf, p, const[1], True)
                            if p is None:
                                raise Exception
                        case True:
                            match const[1]:
                                case False:
                                    p = matutils.maddval(_ScalePar._orignl(scc, scf, matx(p.matx[0][1:], False, True), False, True), p.mele(0, 0, False, True), False, True)
                                    if p is None:
                                        raise Exception
                                case True:
                                    p = matutils.maddval(_ScalePar._orignl(matx(scc.matx[0][:-1] + (Decimal('0.0'), ), False, True), scf, matx(p.matx[0][1:], False, True), True, True), p.mele(0, 0, False, True), False, True)
                                    if p is None:
                                        raise Exception
                                case _:
                                    raise Exception("Invalid argument: const => (bool, bool)")
                        case _:
                            raise Exception("Invalid argument: const => (bool, bool)")
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: scale => bool")
            dic = dict()
            dic["parameters"] = [str(i) for i in p.matxl()[0]]
            dic["iterations"] = c
            dic["r^2"] = str(cls._coofdet(da.data, p, const, True))
            if dic["r^2"] is None:
                raise Exception
            try:
                dic["r^2_adj"] = str(1 - ((1 - Decimal(dic["r^2"])) * (da.datalen - 1) / (da.datalen - da.xvars - 1)))
            except ZeroDivisionError:
                dic["r^2_adj"] = 'NaN'
            return dic
        except Exception as e:
            Terminate.retrn(ret, e)
    

    @classmethod
    def _linreggp(cls, d: tuple, p: matx, p1: parameter, a: Decimal, m: int, pr: Decimal, const=(False, True), ret=False) -> tuple[matx, matx, int]:
        try:
            c = 0
            while (c := c + 1) <= m:
                match const[0]:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.mmult(matutils.tpose(d[0].val(p1.dval(p)), False, True), matutils.msub(matx(tuple([(sum(i),) for i in d[0].val(p1.val(p)).matx]), False, True), d[1], False, True), False, True), False, True), False, True), False, True)
                    case True:
                        pn = matx(p, False, True)
                        p0 = pn.pop(0, False, False, True)[0]
                        p1v = p1.val(pn)
                        dm = matutils.msub(matx(tuple([(p0 * sum(i),) for i in d[0].val(p1v).matx]), False, True), d[1], False, True)
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.addmatx(matutils.mmult(matx(tuple([sum(i) for i in d[0].val(p1v).matx]), False, True), dm, False, True), matutils.mmult(matutils.smult(p0, matutils.tpose(d[0].val(p1.dval(pn)), False, True), False, True), dm, False, True), True, False, True), False, True), False, True), False, True)
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                if pn is None:
                    raise Exception
                match const[0]:
                    case False:
                        pv = p1.val(p)
                        pnv = p1.val(pn)
                        for i in range(len(pv)):
                            if i == 0:
                                ap = pv[i]
                                apn = pnv[i]
                            else:
                                ap.matx = matutils.addmatx(ap, pv[i], False, False, True)
                                apn.matx = matutils.addmatx(apn, pnv[i], False, False, True)
                    case True:
                        pv = matx(p, False, True)
                        pnv = matx(pn, False, True)
                        ap0 = matx(pv.pop(0, False, False, True), False, True)
                        apn0 = matx(pnv.pop(0, False, False, True), False, True)
                        pv = p1.val(pv)
                        pnv = p1.val(pnv)
                        for i in range(len(pv)):
                            if i == 0:
                                ap = matutils.addmatx(ap0, pv[i], False, False, True)
                                apn = matutils.addmatx(apn0, pnv[i], False, False, True)
                            else:
                                ap.matx = matutils.addmatx(ap, pv[i], False, False, True)
                                apn.matx = matutils.addmatx(apn, pnv[i], False, False, True)
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                err = Calculate._cmperrpr(ap, apn, pr, True)
                match err:
                    case True:
                        return pn, apn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, apn, c - 1
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def _weilinreggp(cls, d: tuple, p: matx, p1: parameter, a: Decimal, m: int, pr: Decimal, w: matx, const=(False, True), ret=False) -> tuple[matx, matx, int]:
        try:
            w = w.matx[0]
            c = 0
            while (c := c + 1) <= m:
                match const[0]:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.mmult(matutils.tpose(matutils.smultfac(w, d[0].val(p1.dval(p)), chk=False, ret=True), False, True), matutils.msub(matx(tuple([(sum(i),) for i in d[0].val(p1.val(p)).matx]), False, True), d[1], False, True), False, True), False, True), False, True), False, True)
                    case True:
                        pn = matx(p, False, True)
                        p0 = pn.pop(0, False, False, True)[0]
                        dm = matutils.msub(matx(tuple([(p0 * sum(i),) for i in d[0].val(p1.val(pn)).matx]), False, True), d[1], False, True)
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(-a, matutils.addmatx(matutils.mmult(matutils.smultfac(w, matx(tuple([sum(i) for i in d[0].val(p1.val(pn)).matx]), False, True), False, False, True), dm, False, True), matutils.mmult(matutils.tpose(matutils.smult(p0, matutils.smultfac(w, d[0].val(p1.dval(pn)), chk=False, ret=True), False, True), False, True), dm, False, True), True, False, True), False, True), False, True), False, True)
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                if pn is None:
                    raise Exception
                match const[0]:
                    case False:
                        pv = p1.val(p)
                        pnv = p1.val(pn)
                        for i in range(len(pv)):
                            if i == 0:
                                ap = pv[i]
                                apn = pnv[i]
                            else:
                                ap.matx = matutils.addmatx(ap, pv[i], False, False, True)
                                apn.matx = matutils.addmatx(apn, pnv[i], False, False, True)
                    case True:
                        pv = matx(p, False, True)
                        pnv = matx(pn, False, True)
                        ap0 = matx(pv.pop(0, False, False, True), False, True)
                        apn0 = matx(pnv.pop(0, False, False, True), False, True)
                        pv = p1.val(pv)
                        pnv = p1.val(pnv)
                        for i in range(len(pv)):
                            if i == 0:
                                ap = matutils.addmatx(ap0, pv[i], False, False, True)
                                apn = matutils.addmatx(apn0, pnv[i], False, False, True)
                            else:
                                ap.matx = matutils.addmatx(ap, pv[i], False, False, True)
                                apn.matx = matutils.addmatx(apn, pnv[i], False, False, True)
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                err = Calculate._cmperrpr(ap, apn, pr, True)
                match err:
                    case True:
                        return pn, apn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, apn, c - 1
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def _gradesgp(cls, d: data, p: matx, p1: parameter, a: Decimal, m: int, pr: Decimal, xmt=None, const=(False, True), ret=False) -> dict:
        try:
            da = d
            match (txmt := xmt.__class__.__name__):
                case 'NoneType':
                    pass
                case 'tuple':
                    w = cls._weights(d.data[0], xmt, False)
                case _:
                    raise Exception("Invalid argument: xmt => None/tuple")
            match const[1]:
                case True:
                    d = datautils.dataval(d, Decimal('1.0'), False, True)
                case False:
                    pass
                case _:
                   raise Exception("Invalid argument: const => (bool, bool)")
            d = (function(matutils.dpose(d.getax(), p1.n, chk=False, ret=True), True), d.getay())
            match txmt:
                case 'NoneType':
                    pn = cls._linreggp(d, p, p1, a, m, pr, const, True)
                case 'tuple':
                    pn = cls._weilinreggp(d, p, p1, a, m, pr, w, const, True)
                case _:
                    raise Exception("Invalid argument: xmt")
            if pn is None:
                raise Exception
            p = pn[0]
            ap = pn[1]
            c = pn[2]
            dic = dict()
            dic["parameters"] = [[str(i) for i in p.matxl()[0]], [str(i) for i in ap.matxl()[0]]]
            dic["iterations"] = c
            dic["r^2"] = str(cls._coofdet(da.data, ap, const, True))
            if dic["r^2"] is None:
                raise Exception
            try:
                dic["r^2_adj"] = str(1 - ((1 - Decimal(dic["r^2"])) * (da.datalen - 1) / (da.datalen - da.xvars - 1)))
            except ZeroDivisionError:
                dic["r^2_adj"] = 'NaN'
            return dic
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


    @classmethod
    def _regmatrix(cls, d: data, pmpr: tuple[matx, int, Decimal], weigh=False, xmt=None, method='inverse', const=True, ret=False) -> dict:
        try:
            match weigh:
                # performs linear regression using matrix method
                case False:
                    match const:
                        case True:
                            d1 = datautils.dataval(d, Decimal('1.0'), False, True)
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
                    w = cls._weights(d.data[0], xmt, False).matx[0]
                    if w is None:
                        raise Exception
                    match const:
                        case True:
                            d1 = datautils.dataval(d, Decimal('1.0'), False, True)
                        case False:
                            d1 = d
                        case _:
                            raise Exception("Invalid argument: const=bool")
                    y = d1.getay()
                    x = d1.getax()
                    xt = matutils.smultfac(w, x, True, False, True)
                    y.matx = cls._jacobiany(xt, y, True)
                    x.matx = cls._hessianx(x, xt, True)
                    del xt
                case _:
                    raise Exception("Invalid argument: weigh => bool")
            match method:
                case 'inverse':
                    p = Method._inverse(x, y, True)
                    if p is None:
                        raise Exception
                case 'uttform':
                    p = Method._uttform(x, y, True)
                    if p is None:
                        raise Exception
                case 'gauseidel':
                    p = Method._gauseidel(x, y, pmpr, True)
                    if p is None:
                        raise Exception
                    dic = dict()
                    dic["parameters"] = [str(i) for i in p[0].matxl()[0]]
                    dic["iterations"] = p[1]
                    dic["r^2"] = str(cls._coofdet(d.data, p[0], (False, const), True))
                    if dic["r^2"] is None:
                        raise Exception
                    try:
                        dic["r^2_adj"] = str(1 - ((1 - Decimal(dic["r^2"])) * (d.datalen - 1) / (d.datalen - d.xvars - 1)))
                    except ZeroDivisionError:
                        dic["r^2_adj"] = 'NaN'
                    return dic
                case 'tridia':
                    p = Method._tridia(x, y, True)
                    if p is None:
                        raise Exception
            dic = dict()
            dic["parameters"] = [str(i) for i in p.matxl()[0]]
            dic["r^2"] = str(cls._coofdet(d.data, p, (False, const), True))
            if dic["r^2"] is None:
                raise Exception
            try:
                dic["r^2_adj"] = str(1 - ((1 - Decimal(dic["r^2"])) * (d.datalen - 1) / (d.datalen - d.xvars - 1)))
            except ZeroDivisionError:
                dic["r^2_adj"] = 'NaN'
            return dic
        except Exception as e:
            Terminate.retrn(ret, e)


class LinReg(_Calculate, parameter, Comp):
    @staticmethod
    def gradesgp(d: data, p: list | matx, cfp: list[list[list]] | tuple[tuple[tuple[float | Decimal | int, float | Decimal | int], ...], ...], a: float, m=100, pr=0.01, const=(False, True), ret=False) -> dict:
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
            p1 = parameter(cfp, True, True)
            if p1 is None:
                raise Exception
            match const:
                case (True, True):
                    if sum(p1.n) != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
                    if Comp.eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, True):
                    if sum(p1.n) != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    if Comp.eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case (True, False):
                    if sum(p1.n) != d.xvars:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    if Comp.eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, False):
                    if sum(p1.n) != d.xvars:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
                    if Comp.eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Calculate._gradesgp(d, p, p1, a, m, pr, const=const, ret=True)
        except Exception as e:
            Terminate.retrn(ret, e)
    
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
            return _Calculate._grades(d, p, a, m, pr, scale, const=const, ret=True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @staticmethod
    def matrix(d: data, p=None, m=100, pr=0.01, method='inverse', const=True, ret=False) -> dict:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            pr = Comp.tdecimlp(pr)
            if pr is None:
                raise Exception
            if p is not None:
                p = matx(p, ret=True)
                if p is None or Comp.eqval(p.collen, 1) is None:
                    raise Exception
                match const:
                    case True:
                        if p.rowlen != d.xvars + 1:
                            raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    case False:
                        if p.rowlen != d.xvars:
                            raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
                    case _:
                        raise Exception("Invalid argument: const => bool")
            return _Calculate._regmatrix(d, (p, m, pr), method=method, const=const, ret=True)
        except Exception as e:
            Terminate.retrn(ret, e)


class WeiLinReg(_Calculate, parameter, Comp):

    @staticmethod
    def gradesgp(d: data, p: list | matx, a: float, cfp: list[list[list]] | tuple[tuple[tuple[float | Decimal | int, float | Decimal | int], ...], ...], x: list, t=float("inf"), m=100, pr=0.01, const=(False, True), ret=False) -> dict:
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
            x = matx(x, ret=True)
            if x.rowlen != d.xvars:
                raise Exception(str(x.rowlen) + " != " + str(d.xvars))
            t = Comp.tdeciml(t)
            if t is None:
                raise Exception
            p1 = parameter(cfp, True, True)
            if p1 is None:
                raise Exception
            match const:
                case (True, True):
                    if sum(p1.n) != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
                    if Comp.eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, True):
                    if sum(p1.n) != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    if Comp.eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case (True, False):
                    if sum(p1.n) != d.xvars:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    if Comp.eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, False):
                    if sum(p1.n) != d.xvars:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
                    if Comp.eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Calculate._gradesgp(d, p, p1, a, m, pr, (x, t), const, ret=True)
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def grades(cls, d: data, p: list, a: float, x: list, t=float("inf"), m=100, pr=0.01, scale=False, const=(False, True), ret=False) -> dict:
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
            x = matx(x, True, True)
            if x is None:
                raise Exception
            if Comp.eqval(x.rowlen, d.xvars) is None or Comp.eqval(x.collen, 1) is None:
                raise Exception
            t = Comp.tdeciml(t)
            if t is None:
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
            return _Calculate._grades(d, p, a, m, pr, scale, (x, t), const=const, ret=True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @staticmethod
    def matrix(d: data, x: list, t=float('inf'), p=None, m=100, pr=0.01, method='inverse', const=True, ret=False) -> dict:
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
                if p is None or Comp.eqval(p.collen, 1) is None:
                    raise Exception
                match const:
                    case True:
                        if p.rowlen != d.xvars + 1:
                            raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    case False:
                        if p.rowlen != d.xvars:
                            raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
                    case _:
                        raise Exception("Invalid argument: const => bool")
            return _Calculate._regmatrix(d, (p, m, pr), True, (x, t), method=method, const=const, ret=True)
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
#                    [1, 1, 1], 0.01, 100, scale=True, const=(False, False), ret=True)
# print(b)
# a = 0.00196
# c = (False, True)
# b = LinReg.grades(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), [0, 1, 1, 1], a, 1000, 0.01, const=c, ret=True)
# print(b)
# print(PLinReg.y([2,3,6], b["parameters"], c))
# print('2')
# c = WeiLinReg.matrix(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), [2, 6, 4])
# print(c)
# c = WeiLinReg.gradesgp(
#    data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), [1, 1, 1],
#    0.0008, [[[1, 1 ], ] for _ in range(3)], [2, 4, 6], const=(False, False))
# print(c)
# PLinReg.allygp(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]),  c["parameters"][0], [[[1,1], ] for i in range(3)], (False, False)).pmatx
# PLinReg.ally(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]),  c["parameters"][1] , (False, False)).pmatx
