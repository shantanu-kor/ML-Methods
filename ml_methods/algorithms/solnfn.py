# import os, sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
from functions import funcutils
from matrix import matutils, matx
from cmdexec import Terminate, Comp

class SolveFn(funcutils, matutils, matx, math, Comp):
    
    @classmethod
    def rootrre(cls, fn, pos: int, x: list | matx, m=100, pr=0.01, ret=False) -> dict:
        try:
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            if Comp.eqval(x.collen, 1) is None:
                raise Exception
            pos = Comp.tint(pos)
            if pos is None:
                raise Exception
            fnr = funcutils.rearr(fn, pos, True)
            if fnr is None:
                raise Exception
            xn = list()
            for i in x.matx[0]:
                try:
                    dfnr = math.fabs(fnr.dval(i))
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
                    if math.fabs(valy) < pr or c == m:
                        value[str(i)] = (str(val), c, )
                        break
                    else:
                        xi = val
            return value
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def lininter(cls, fn, x: list | matx, m=100, pr=0.01, ret=False) -> dict:
        try:
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            if Comp.eqval(x.rowlen, 2) is None:
                raise Exception
            x = matutils.matlxtox(x, False, True)
            value = dict()
            for i in x:
                c = -1
                p1 = (i.mele(0, 0, False, True), fn.val(i.mele(0, 0, False, True)))
                p2 = (i.mele(0, 1, False, True), fn.val(i.mele(0, 1, False, True)))
                if p1[1]*p2[1] < 0:
                    while (c := c + 1) < m:
                        valx = (((p1[0] - p2[0]) * (- p1[1])) / (p1[1] - p2[1])) + p1[0]
                        p3 = (valx, fn.val(valx))
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
    
    @classmethod
    def bchop(cls, fn, x: list | matx, m=100, pr=0.01, ret=False) -> dict:
        try:
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            if x.rowlen != 2:
                raise Exception(str(x.rowlen) + " != 2")
            x = matutils.matlxtox(x, False, True)
            value = dict()
            for i in x:
                c = -1
                p1 = (i.mele(0, 0, False, True), fn.val(i.mele(0, 0, False, True)))
                p2 = (i.mele(0, 1, False, True), fn.val(i.mele(0, 1, False, True)))
                if p1[1]*p2[1] < 0:
                    while (c := c + 1) < m:
                        mid = (p1[0] + p2[0]) / 2
                        p3 = (mid, fn.val(mid))
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

    @classmethod
    def nrinter(cls, fn, x: list | matx, m=100, pr=0.01, ret=False) -> dict:
        try:
            x = matx(x, ret=True)
            if x is None:
                raise Exception
            if Comp.eqval(x.collen, 1) is None:
                raise Exception
            value = dict()
            for i in x.matx[0]:
                c = -1
                while (c := c + 1) < m:
                    nx = i - (fn.val(i) / fn.dval(i))
                    if fn.val(nx) < pr:
                        value[str(i)] = (str(nx), c, )
                        break
            return value
        except Exception as e:
            Terminate.retrn(ret, e)


# for j in range(1):
#     d = {'Al_LowCutoff': {'parameters': [16.058881741715595, -8.955601539113559, 1.0939627709012711],
#                           'r^2': 0.9983192621607382, 'r^2_adj': 0.9978390513495206},
#         'Al_HighCutoff': {'parameters': [15.811508555198088, -8.971596025396138, 1.1032308384019416],
#                            'r^2': 0.998828056926424, 'r^2_adj': 0.9984932160482594},
#         'Al_MedCutoff': {'parameters': [15.946995875099674, -9.0157831403194, 1.107305156358052],
#                           'r^2': 0.9988916677797752, 'r^2_adj': 0.9985750014311395}}
#     p = dict()
#     for i in d.items():
#         p[i[0]] = poly(matx([i[1]["parameters"], [0, 1, 2]]), True)
#     for i in p.items():
#         p[i[0]] = funcutils.ndpoly(i[1], True)
#     for i in p.items():
#         p[i[0]] = SolveFn.nrinter(i[1], [-10, 0, 10], 1000, 0.001)
#     print(p)
#     p = SolveFn.rootrre(poly(matx([[4, -4, 1], [0, 1, 2]])), 2, [i - 5 for i in range(10)], 1000, 0.001)
#     print(p)
