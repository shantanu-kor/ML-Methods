from utils.deciml import algbra as alg, Decimal
from matrix import matx, matutils
from utils.cmpr import eqval, tfunc, tmatx
from utils.terminate import retrn


class axn:
    
    def __init__(self, f: list | tuple | matx, chk=True, ret='a') -> None:
        f = matx(f, chk, 'c')
        if f is None:
            retrn(ret, "Invalid axn\n")
        if eqval(f.collen, 1) is None or eqval(f.rowlen, 2) is None:
                retrn(ret, "Invalid axn\n")
        self.f = f
        if self.f.mele(0, 1, False, 'c') == 0:
            self.df = None
        else:
            self.df = matx((alg.mul(self.f.mele(0, 0, False, 'c'), self.f.mele(0, 1, False, 'c')), alg.sub(self.f.mele(0, 1, False, 'c'), 1),), False, 'c')
        del f
        self.val = lambda x: alg.mul(self.f.mele(0, 0, False, 'c'), alg.pwr(x, self.f.mele(0, 1, False, 'c')))
        self.dval = lambda x: alg.mul(self.df.mele(0, 0, False, 'c'), alg.pwr(x, self.df.mele(0, 1, False, 'c')))
        self.ival = lambda x: self.fival(x)

    def fival(self, x: float | int | Decimal) -> Decimal:
        try:
            if self.f.mele(0, 1, False, 'c') == -1:
                if x > 0:
                    return alg.mul(self.f.mele(0, 0, False, 'c'), alg.log(x))
                else:
                    raise Exception
            else:
                return alg.mul(alg.div(self.f.mele(0, 0, False, 'c'), (p := self.f.mele(0, 1, False, 'c') + 1)), alg.pwr(x, p))
        except Exception as e:
            retrn(False, e)


class poly:
    
    def __init__(self, f: matx | tuple[axn, ...], ret='a') -> None:
        try:
            if type(f) is tuple:
                for i in f:
                    if tfunc.axn(i) is None:
                        raise Exception
                self.f = f
            else:
                if tmatx(f) is not None:
                    if eqval(f.collen, 2) is None:
                        raise Exception
                self.f = tuple([axn(i, False, 'c') for i in matutils.matlxtox(matutils.tpose(f, False, 'c'), False, 'c')])
            self.df = tuple([axn(i.df, False, 'c') for i in self.f if i.df is not None])
            del f
            self.val = lambda x: alg.addl([i.val(x) for i in self.f])
            self.dval = lambda x: alg.addl([i.val(x) for i in self.df])
            self.ival = lambda x: alg.addl([i.ival(x) for i in self.f])
        except Exception as e:
            retrn(ret, e)


class apolyn:
    
    def __init__(self, an: list | tuple | matx, f: poly | matx | tuple[axn, ...], chk=True, ret='a') -> None:
        self.afn = axn(an, chk, 'c')
        if f.__class__.__name__ != 'poly':
            self.f = poly(f, 'c')
        else:
            self.f = f
        del f
        self.df = poly(self.f.df, 'c')
        self.val = lambda x: self.afn.val(self.f.val(x))
        self.dval = lambda x: alg.mul(self.afn.dval(self.f.val(x)), self.df.val(x))


class funcutils:
    
    @staticmethod
    def rearr(a, pos: int, ret='a') -> apolyn:
        try:
            if pos is None:
                raise Exception
            ta = a.__class__.__name__
            match ta:
                case 'poly':
                    return apolyn(matx((alg.pwr(alg.div(1, a.f[pos].f.mele(0, 0, False, 'c')), alg.div(1, a.f[pos].f.mele(0, 1, False, 'c'))), alg.div(1, a.f[pos].f.mele(0, 1, False, 'c'))), False, 'c'), poly(tuple([axn(matutils.smultfac(tuple([-1, 1]), i[1].f, False, False, 'c'), False, 'c') for i in enumerate(a.f) if i[0] != pos]), 'c'), ret='c')
                case _:
                    raise Exception
        except Exception as e:
            retrn(ret, e)
    
    @staticmethod
    def ndpoly(p: poly, n: int) -> poly | None:
        try:
            for _ in range(n):
                p = poly(p.df, 'c')
                if p is None:
                    return None
            return p
        except Exception as e:
            retrn('c', e)
