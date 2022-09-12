import math
from decimal import Decimal
from matrix import matx, matutils, pwr
from cmdexec import Terminate, Comp


class axn(matx, Comp):
    
    def __init__(self, f: list | tuple | matx, chk=True, ret=False) -> None:
        f = matx(f, chk, True)
        if f is None:
            Terminate.retrn(ret, "Invalid axn\n")
        if Comp.eqval(f.collen, 1) is None or Comp.eqval(f.rowlen, 2) is None:
                Terminate.retrn(ret, "Invalid axn\n")
        self.f = f
        if self.f.mele(0, 1, False, True) == 0:
            self.df = None
        else:
            self.df = matx(
                (self.f.mele(0, 0, False, True) * self.f.mele(0, 1, False, True), self.f.mele(0, 1, False, True) - 1,),
                False, True)
        del f
        self.val = lambda x: self.f.mele(0, 0, False, True) * pwr(x, self.f.mele(0, 1, False, True), False, True)
        self.dval = lambda x: self.df.mele(0, 0, False, True) * pwr(x, self.df.mele(0, 1, False, True), False, True)
        self.ival = lambda x: self.fival(x)

    def fival(self, x: float | int | Decimal) -> Decimal:
        try:
            if self.f.mele(0, 1, False, True) == -1:
                if x > 0:
                    return matx(self.f.mele(0, 0, False, True), Decimal(str(math.log(x))), False, True)
                else:
                    raise Exception
            else:
                return matx(self.f.mele(0, 0, False, True) / (self.f.mele(0, 1, False, True) + 1), pwr(x, self.f.mele(0, 1, False, True) + 1, False, True), False, True)
        except Exception as e:
            Terminate.retrn(False, e)


class poly(axn, matutils, Comp):
    
    def __init__(self, f: matx | tuple[axn, ...], ret=False) -> None:
        try:
            if type(f) is tuple:
                for i in f:
                    if Comp.taxn(i) is None:
                        raise Exception
                self.f = f
            else:
                if Comp.tmatx(f) is not None:
                    if Comp.eqval(f.collen, 2) is None:
                        raise Exception
                self.f = tuple([axn(i, False, True) for i in matutils.matlxtox(matutils.tpose(f, False, True), False, True)])
            self.df = tuple([axn(i.df, False, True) for i in self.f if i.df is not None])
            del f
            self.val = lambda x: sum([i.val(x) for i in self.f])
            self.dval = lambda x: sum([i.val(x) for i in self.df])
            self.ival = lambda x: sum([i.ival(x) for i in self.f])
        except Exception as e:
            Terminate.retrn(ret, e)


class apolyn(poly, axn):
    
    def __init__(self, an: list | tuple | matx, f: poly | matx | tuple[axn, ...], chk=True, ret=False) -> None:
        self.afn = axn(an, chk, True)
        if f.__class__.__name__ != 'poly':
            self.f = poly(f, True)
        else:
            self.f = f
        del f
        self.df = poly(self.f.df, True)
        self.val = lambda x: self.afn.val(self.f.val(x))
        self.dval = lambda x: self.afn.dval(self.f.val(x)) * self.df.val(x)



class funcutils(apolyn, poly, axn, matutils, matx):
    
    @classmethod
    def rearr(cls, a, pos: int, ret=False) -> apolyn:
        try:
            if pos is None:
                raise Exception
            ta = a.__class__.__name__
            match ta:
                case 'poly':
                    return apolyn(matx((pwr(1/a.f[pos].f.mele(0, 0, False, True), 1/a.f[pos].f.mele(0, 1, False, True), False, True), 1/a.f[pos].f.mele(0, 1, False, True)), False, True), poly(tuple([axn(matutils.smultfac(tuple([-1, 1]), i[1].f, False, False, True), False, True) for i in enumerate(a.f) if i[0] != pos]), True), ret=True)
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def ndpoly(cls, p: poly, n: int) -> poly | None:
        for _ in range(n):
            p = poly(p.df, True)
            if p is None:
                return None
        return p

