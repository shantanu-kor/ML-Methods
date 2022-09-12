import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decimal import Decimal
import math
from cmdexec import Terminate
from matrix import matx, matutils
from algoutils import Calculate


class _Calculate(matutils, matx):

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

class Method(_Calculate, matutils, Calculate, matx):
    
    @classmethod
    def _inverse(cls, a: matx, b: matx, ret=False) -> matx:
        try:
            return matutils.mmult(matutils.tpose(b, False, True), matutils.invse(a, False, True), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)
    

    @classmethod
    def _uttform(cls, a: matx, b: matx, ret=False) -> matx:
        try:
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
                an = matx(tuple([(a.mele(a.collen - 1 - i, a.rowlen - 1 + j - i + 1, False, True),) for j in range(i)]), False, True)
                p.matx = matutils.addmatx(matutils.smult(1 / a.mele(a.collen - 1 - i, a.rowlen - 1 - i, False, True), matutils.msub(matx(b.mrow(b.collen - 1 - i, False, True), False, True), matutils.mmult(p, an, False, True), False, True), False, True), p, False, False, True)
            del an
            return p
        except Exception as e:
            Terminate.retrn(ret, e)
    

    @classmethod
    def _gauseidel(cls, a: matx, b: matx, pmpr: tuple[matx, int, Decimal], ret=False) -> tuple[matx, int]:
        try:
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
            a.matx = matutils.madd(a, matutils.sclrm(a.rowlen, Decimal('1.0'), False, True), False, True)
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
                c = 0
                while (c := c + 1) <= m:
                    pn = _Calculate._lup(lt, ut, p, b)
                    if pn is None:
                        raise Exception
                    err = Calculate._cmperrpr(p, pn, pr, True)
                    match err:
                        case True:
                            p.matx = pn
                            break
                        case False:
                            p.matx = pn
                        case _:
                            raise Exception
            else:
                c = 0
                while (c := c + 1) <= m:
                    pn = _Calculate._ulp(ut, lt, p, b)
                    if pn is None:
                        raise Exception
                    err = Calculate._cmperrpr(p, pn, pr, True)
                    match err:
                        case True:
                            p.matx = pn
                            break
                        case False:
                            p.matx = pn
                        case _:
                            raise Exception
            if c == m + 1:
                return p, c - 1
            return p, c
        except Exception as e:
            Terminate.retrn(ret, e)
    

    @classmethod
    def _tridia(cls, a: matx, b: matx, ret=False) -> matx:
        try:
            for i in range(int(a.rowlen / 2) + 1):
                elea = a.mele(i + 1, i, False, True)
                cola = a.mcol(i, False, True)
                for j in range(a.collen):
                    if j > i + 1:
                        a.matx = matutils.tform(a, j, i + 1, - cola[j] / elea, True, False, True)
                        b.matx = matutils.tform(b, j, i + 1, - cola[j] / elea, True, False, True)
                elec = a.mele(a.collen - 2 - i, a.rowlen - 1 - i, False, True)
                colc = a.mcol(a.rowlen - 1 - i, False, True)
                for j in range(a.collen):
                    if j < a.collen - 2 - i:
                        a.matx = matutils.tform(a, j, a.collen - 2 - i, - colc[j] / elec, True, False, True)
                        b.matx = matutils.tform(b, j, a.collen - 2 - i, - colc[j] / elec, True, False, True)
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
        except Exception as e:
            Terminate.retrn(ret, e)