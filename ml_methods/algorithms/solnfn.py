from dobj.functions import funcutils
from dobj.matrix import matutils, matx
from utils.deciml import algbra as alg, abs
from utils.cmpr import eqval, tint
from utils.terminate import retrn


class SolveFn:
    
    @classmethod
    def rootrre(cls, fn, pos: int, x: list | matx, m=100, pr=0.01, ret='a') -> dict:
        try:
            if (x := matx(x, ret='c')) is None:
                raise Exception
            if eqval(x.collen, 1) is None:
                raise Exception
            if (pos := tint.int(pos)) is None:
                raise Exception
            if (fnr := funcutils.rearr(fn, pos, 'c')) is None:
                raise Exception
            xn = list()
            for i in x.matx[0]:
                try:
                    dfnr = abs(fnr.dval(i))
                    if dfnr < 0:
                        if dfnr < -1:
                            continue
                    if dfnr > 0:
                        if dfnr > 1:
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
                c = -1
                while (c := c + 1) < m:
                    val = fnr.val(xi)
                    valy = fn.val(val)
                    if str(valy) == 'NaN':
                        break
                    if abs(valy) < pr or c == m:
                        value[str(i)] = (str(val), c, )
                        break
                    else:
                        xi = val
            return value
        except Exception as e:
            retrn(ret, e)
    
    @classmethod
    def lininter(cls, fn, x: list | matx, m=100, pr=0.01, ret='a') -> dict:
        try:
            if (x := matx(x, ret='c')) is None:
                raise Exception
            if eqval(x.rowlen, 2) is None:
                raise Exception
            x = matutils.matlxtox(x, False, 'c')
            value = dict()
            for i in x:
                c = -1
                p1 = (i.mele(0, 0, False, 'c'), fn.val(i.mele(0, 0, False, 'c')))
                p2 = (i.mele(0, 1, False, 'c'), fn.val(i.mele(0, 1, False, 'c')))
                if (p1[1] > 0 and p2[1] < 0) or (p1[1] < 0 and p2[1] > 0):
                    while (c := c + 1) < m:
                        valx = alg.add(alg.div(alg.mul(alg.sub(p1[0], p2[0]), alg.mul(-1, p1[1])), alg.sub(p1[1], p2[1])), p1[0])
                        p3 = (valx, fn.val(valx))
                        if str(p3[1]) == 'NaN':
                            break
                        if abs(p3[1]) < pr or c == m:
                            value[str(i.matx[0])] = (str(p3[0]), c, )
                            break
                        if p1[1]*p3[1] < 0:
                            p2 = p3
                        else:
                            p1 = p3
            return value
        except Exception as e:
            retrn(ret, e)
    
    @classmethod
    def bchop(cls, fn, x: list | matx, m=100, pr=0.01, ret='a') -> dict:
        try:
            if (x := matx(x, ret='c')) is None:
                raise Exception
            if x.rowlen != 2:
                raise Exception(str(x.rowlen) + " != 2")
            x = matutils.matlxtox(x, False, 'c')
            value = dict()
            for i in x:
                c = -1
                p1 = (i.mele(0, 0, False, 'c'), fn.val(i.mele(0, 0, False, 'c')))
                p2 = (i.mele(0, 1, False, 'c'), fn.val(i.mele(0, 1, False, 'c')))
                if (p1[1] > 0 and p2[1] < 0) or (p1[1] < 0 and p2[1] > 0):
                    while (c := c + 1) < m:
                        mid = alg.div(alg.add(p1[0], p2[0]), 2)
                        p3 = (mid, fn.val(mid))
                        if str(p3[1]) == 'NaN':
                            break
                        if abs(p3[1]) < pr or c == m:
                            value[str(i.matx[0])] = (str(p3[0]), c, )
                            break
                        if (p1[1] > 0 and p3[1] < 0) or (p1[1] < 0 and p3[1] > 0):
                            p2 = p3
                        else:
                            p1 = p3
            return value
        except Exception as e:
            retrn(ret, e)

    @classmethod
    def nrinter(cls, fn, x: list | matx, m=100, pr=0.01, ret='a') -> dict:
        try:
            if (x := matx(x, ret='c')) is None:
                raise Exception
            if eqval(x.collen, 1) is None:
                raise Exception
            value = dict()
            for i in x.matx[0]:
                c = -1
                while (c := c + 1) < m:
                    nx = alg.sub(i, alg.div(fn.val(i), fn.dval(i)))
                    if fn.val(nx) < pr:
                        value[str(i)] = (str(nx), c, )
                        break
            return value
        except Exception as e:
            retrn(ret, e)
