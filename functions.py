# import math
from decimal import Decimal
from matrix import matx, matutils, pwr
from cmdexec import Terminate, Comp


class axn:
    def __init__(self, f: list | matx, chk=True, ret=False) -> None:
        f = matx(f, chk, True)
        if f is None:
            Terminate.retrn(ret, "Invalid axn\n")
        if f.collen != 1 or f.rowlen != 2:
                Terminate.retrn(ret, "Invalid axn\n")
        self.f = f
        if self.f.mele(0, 1, False, True) == 0:
            self.df = None
        else:
            self.df = matx(
                (self.f.mele(0, 0, False, True) * self.f.mele(0, 1, False, True), self.f.mele(0, 1, False, True) - 1,),
                False, True)
        del f
        self.val = lambda x: self.f.mele(0, 0, False, True) * pwr(x, self.f.mele(0, 1, False, True))
        self.dval = lambda x: self.df.mele(0, 0, False, True) * pwr(x, self.df.mele(0, 1, False, True))


class poly:
    def __init__(self, f: matx | tuple[axn, ...], ret=False) -> None:
        try:
            if type(f) is tuple:
                for i in f:
                    if Comp.taxn(i) is None:
                        raise Exception
                self.f = f
            else:
                if Comp.tmatx(f) is not None:
                    if f.collen != 2:
                        raise Exception(str(f.collen)+" != 2")
                self.f = tuple([axn(i, False, True) for i in matutils.matlxtox(matutils.tpose(f, False, True), False, True)])
            self.df = tuple([axn(i.df, False, True) for i in self.f if i.df is not None])
            del f
            self.val = lambda x: sum([i.val(x) for i in self.f])
            self.dval = lambda x: sum([i.val(x) for i in self.df])
        except Exception as e:
            Terminate.retrn(ret, e)


class apolyn:
    def __init__(self, a: float | Decimal, n: float | Decimal, f: poly | matx, chk=True, ret=False) -> None:
        if chk is True:
            a = Comp.tdeciml(a)
            n = Comp.tdeciml(n)
            if a is None or n is None or n is None:
                Terminate.retrn(ret, "")
        self.afn = axn(matx(tuple([a, n]), False, True), False, True)
        if f.__class__.__name__ != 'poly':
            if f.__class__.__name__ != 'matx':
                Terminate.retrn(ret, "")
            else:
                self.f = poly(f, True)
        else:
            self.f = f
        del f
        self.df = poly(self.f.df, True)
        self.val = lambda x: self.afn.val(self.f.val(x))
        self.dval = lambda x: self.afn.dval(self.f.val(x)) * self.df.val(x)


class funcutils(matutils):
    @staticmethod
    def rearr(a, pos: int, ret=False) -> apolyn:
        try:
            if pos is None:
                raise Exception
            ta = a.__class__.__name__
            match ta:
                case 'poly':
                    return apolyn(pwr(1/a.f[pos].f.mele(0, 0, False, True), 1/a.f[pos].f.mele(0, 1, False, True)), 1/a.f[pos].f.mele(0, 1, False, True), poly(tuple([axn(matutils.smultfac(tuple([-1, 1]), i[1].f, False, False, True), False, True) for i in enumerate(a.f) if i[0] != pos]), True), ret=True)
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @staticmethod
    def ndpoly(p: poly, n: int) -> poly | None:
        for _ in range(n):
            p = poly(p.df, True)
            if p is None:
                return None
        return p

    @staticmethod
    def polytoan(f: poly) -> tuple[matx, matx]:
        return matutils.matlxtox(matutils.tpose(matutils.matxtolx(tuple([i.f for i in f.f]))))
