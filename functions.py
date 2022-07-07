import math
from matrix import matx, matutils, Comp, pwr
from cmdexec import Terminate


class Compf(Comp):
    @staticmethod
    def taxn(a) -> bool:
        if a.__class__.__name__ != 'axn':
            Terminate.retrn(True, str(type(a)) + " is not axn")
        else:
            return True

    @staticmethod
    def tpoly(a) -> bool:
        if a.__class__.__name__ != 'poly':
            Terminate.retrn(True, str(type(a)) + " is not poly")
        else:
            return True

    @staticmethod
    def tapolyn(a) -> bool:
        if a.__class__.__name__ != 'apolyn':
            Terminate.retrn(True, str(type(a)) + " is not apolyn")
        else:
            return True


class axn:
    def __init__(self, f: list | matx, chk=True, ret=False) -> None:
        if chk is True:
            f = matx(f, True, True)
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


class poly(Compf):
    def __init__(self, f: matx | tuple[axn], ret=False) -> None:
        try:
            if type(f) is tuple:
                for i in f:
                    if Compf.taxn(i) is None:
                        raise Exception
                self.f = f
            else:
                if Compf.tmatx(f) is not None:
                    if f.collen != 2:
                        raise Exception(str(f.collen)+" != 2")
                self.f = tuple([axn(i, False, True) for i in matutils.matlxtox(matutils.tpose(f, True), True)])
            self.df = tuple([axn(i.df, False, True) for i in self.f if i.df is not None])
            del f
            self.val = lambda x: sum([_.val(x) for _ in self.f])
            self.dval = lambda x: sum([_.val(x) for _ in self.df])
        except Exception as e:
            Terminate.retrn(ret, e)


class apolyn(Compf):
    def __init__(self, a: float, n: float, f: poly | matx, chk=True, ret=False) -> None:
        if chk is True:
            a = Compf.tdeciml(a)
            n = Compf.tdeciml(n)
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


class funcutils:
    @staticmethod
    def rearr(a, pos: int, ret=False) -> None:
        try:
            if pos is None:
                raise Exception
            ta = a.__class__.__name__
            match ta:
                case 'poly':
                    return apolyn(pwr(1/a.f[pos].f.mele(0, 0, False, True), 1/a.f[pos].f.mele(0, 1, False, True)), 1/a.f[pos].f.mele(0, 1, False, True), poly(tuple([axn(matutils.smultfac(tuple([-1, 1]), i[1].f, False, True), False, True) for i in enumerate(a.f) if i[0] != pos]), True), ret=True)
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
        x = [i.f for i in f.f]
        for i in enumerate(x):
            if i[0] == 0:
                a = i[1]
            else:
                a.matx = matutils.addmatx(a, i[1], True, True)
        n = matx(a.gele([1, ], False, False, True), False, True)
        a = matx(a.gele([0, ], False, False, True), False, True)
        return a, n
