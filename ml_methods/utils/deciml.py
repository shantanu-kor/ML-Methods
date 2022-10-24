from decimal import ROUND_HALF_UP, Decimal, getcontext
from terminate import retrn


_DecimalPrecision = 16


getcontext().rounding = ROUND_HALF_UP

class precision:
    
    @staticmethod
    def set(a: int) -> None:
        global _DecimalPrecision
        _DecimalPrecision = a

    @staticmethod
    def get() -> int:
        return _DecimalPrecision


def deciml(a: float | int | str | Decimal) -> Decimal:
    try:
        global _DecimalPrecision
        b = (a := str(a)).lstrip('-').split('.')
        match len(b):
            case 1:
                if 'E' in b[0]:
                    getcontext().prec = _DecimalPrecision + 1
                    return Decimal(a)
                else:
                    return Decimal(a)
            case 2:
                b0, b1 = b
                if int(b0) == 0:
                    c = 0
                    for i in b1:
                        if i != '0':
                            getcontext().prec = _DecimalPrecision - c
                            break
                        c += 1
                        if c > _DecimalPrecision:
                            if a[0][0] == '-':
                                a = '-'+b1+'E-'+str(len(b1))
                                getcontext().prec = _DecimalPrecision + 1
                            else:
                                a = b1+'E-'+str(len(b1))
                                getcontext().prec = _DecimalPrecision + 1
                            break
                else:
                    getcontext().prec = len(b0) + _DecimalPrecision
        return Decimal(a) + 0
    except:
        return Decimal('NaN')


_Pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679'
_EulersNumber = '2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274'


class constant:
    
    @staticmethod
    def e(pr=_DecimalPrecision) -> Decimal | None:
        try:
            if pr > 100:
                raise Exception
            global _EulersNumber
            return Decimal(_EulersNumber[:pr + 2])
        except:
            retrn('c', "Invalid argument: pr -> < 100")


    def pi(pr=_DecimalPrecision) -> Decimal | None:
        try:
            if pr > 100:
                raise Exception
            global _Pi
            return Decimal(_Pi[:pr + 2])
        except:
            retrn('c', "Invalid argument: pr -> < 100")


def abs(a: float | int | str | Decimal) -> Decimal:
    a = Decimal(str(a))
    if a < 0:
        return deciml(algbra.mul(-1, a))
    else:
        return deciml(a)

class algbra:

    @staticmethod
    def add(a: float | int | str | Decimal, *b: float | int | str | Decimal) -> Decimal:
        global _DecimalPrecision
        _DecimalPrecision += 3
        def __add(a, b):
            try:
                global _DecimalPrecision
                a1, b1, ae, be = (a := str(a)).split('E'), (b := str(b)).split('E'), 0, 0
                if len(a1) == 2:
                    ae = a1[1]
                if len(b1) == 2:
                    be = b1[1]
                an, bn = a1[0].lstrip('-').split('.'), b1[0].lstrip('-').split('.')
                d1, d2 = len(an[0]) + int(ae), len(bn[0]) + int(be)
                p = _DecimalPrecision + 2
                if d1 > d2:
                    if d1 > 0:
                        getcontext().prec = p + d1
                    else:
                        getcontext().prec = p
                else:
                    if d2 > 0:
                        getcontext().prec = p + d2
                    else:
                        getcontext().prec = p
                return deciml(Decimal(a) + Decimal(b))
            except:
                return Decimal('NaN')
        r = a
        for i in b:
            r = __add(r, i)
        _DecimalPrecision -= 3
        return deciml(r)

    @staticmethod
    def sub(a: float | int | str | Decimal, *b: float | int | str | Decimal) -> Decimal:
        global _DecimalPrecision
        _DecimalPrecision += 3
        def __sub(a, b):
            try:
                global _DecimalPrecision
                a1, b1, ae, be = (a := str(a)).split('E'), (b := str(b)).split('E'), 0, 0
                if len(a1) == 2:
                    ae = a1[1]
                if len(b1) == 2:
                    be = b1[1]
                an, bn = a1[0].lstrip('-').split('.'), b1[0].lstrip('-').split('.')
                d1, d2 = len(an[0]) + int(ae), len(bn[0]) + int(be)
                p = _DecimalPrecision + 2
                if d1 > d2:
                    if d1 > 0:
                        getcontext().prec = p + d1
                    else:
                        getcontext().prec = p
                else:
                    if d2 > 0:
                        getcontext().prec = p + d2
                    else:
                        getcontext().prec = p
                return deciml(Decimal(a) - Decimal(b))
            except:
                return Decimal('NaN')
        r = a
        for i in b:
            r = __sub(r, i)
        _DecimalPrecision -= 3
        return deciml(r)

    @staticmethod
    def mul(a: float | int | str | Decimal, *b: float | int | str | Decimal) -> Decimal:
        global _DecimalPrecision
        _DecimalPrecision += 3
        def __mul(a,b):
            try:
                global _DecimalPrecision
                a1, b1, ae, be = (a := str(a)).split('E'), (b := str(b)).split('E'), 0, 0
                if len(a1) == 2:
                    ae = int(a1[1])
                if len(b1) == 2:
                    be = int(b1[1])
                an, bn = a1[0].lstrip('-').split('.'), b1[0].lstrip('-').split('.')
                p = _DecimalPrecision + 2
                if (p1 := ae + be + len(an[0]) + len(bn[0])) > 0:
                    getcontext().prec = p1 + p
                else:
                    getcontext().prec = p
                return deciml(Decimal(a) * Decimal(b))
            except:
                return Decimal('NaN')
        r = a
        for i in b:
            r = __mul(r, i)
        _DecimalPrecision -= 3
        return deciml(r)

    @staticmethod
    def div(a: float | int | str | Decimal, b: float | int | str | Decimal) -> Decimal:
        try:
            global _DecimalPrecision
            a1, b1, ae, be = (a := str(a)).split('E'), (b := str(b)).split('E'), 0, 0
            if len(a1) == 2:
                ae = a1[1]
            if len(b1) == 2:
                be = b1[1]
            an, bn = a[0].lstrip('-').split('.'), b[0].lstrip('-').split('.')
            p = _DecimalPrecision + 4
            if (p1 := int(ae) - int(be) + len(an[0]) - len(bn[0])) > 0:
                getcontext().prec = p1 + p
            else:
                getcontext().prec = p
            return deciml(Decimal(a) / Decimal(b))
        except:
            return Decimal('NaN')
    
    @classmethod
    def log(cls, a: float | int | str | Decimal, b=constant.e()) -> Decimal:
        try:
            global _DecimalPrecision
            a, b, c = Decimal(str(a)), Decimal(str(b)), 0
            if b >= 1:
                if a >= 1:
                    while a > b:
                        a = cls.div(a, b)
                        c += 1
                    if c != 0:
                        getcontext().prec = _DecimalPrecision + len(str(c)) + 2
                        return deciml((a.ln() / b.ln()) + c)
                    else:
                        getcontext().prec = _DecimalPrecision + 2
                        return deciml(a.ln() / b.ln())
                if a < 1:
                    while a < 1:
                        a = cls.mul(a, b)
                        c += 1
                    if c != 0:
                        getcontext().prec = _DecimalPrecision + len(str(c)) + 2
                        return deciml((a.ln() / b.ln()) - c)
                    else:
                        getcontext().prec = _DecimalPrecision + 2
                        return deciml(a.ln() / b.ln())
            if b < 1:
                if a >= b:
                    while a > b:
                        a = cls.mul(a, b)
                        c += 1
                    if c != 0:
                        getcontext().prec = _DecimalPrecision + len(str(c)) + 2
                        return deciml((a.ln() / b.ln()) - c)
                    else:
                        getcontext().prec = _DecimalPrecision + 2
                        return deciml(a.ln() / b.ln())
                if a < b:
                    while a < b:
                        a = cls.div(a, b)
                        c += 1
                    if c != 0:
                        getcontext().prec = _DecimalPrecision + len(str(c)) + 2
                        return deciml((a.ln() / b.ln()) + c)
                    else:
                        getcontext().prec = _DecimalPrecision + 2
                        return deciml(a.ln() / b.ln())
        except:
            return Decimal('NaN')

    @classmethod
    def pwr(cls, a: float | int | Decimal | str, b: float | int | Decimal | str) -> Decimal:
        try:
            global _DecimalPrecision
            a, b, c = Decimal(str(a)), Decimal(str(b)), 0
            if b == (ib := int(b)):
                _DecimalPrecision += 2
                r = 1
                if b < 0:
                    for _ in range(-ib):
                        r = cls.mul(r, a)
                    r = cls.div(1, r)
                else:
                    for _ in range(ib):
                        r = cls.mul(r, a)
                _DecimalPrecision -= 2
                return deciml(r)
            elif a < 0:
                raise Exception
            elif b == 0:
                return Decimal('1')
            elif a == 0:
                return Decimal('0')
            if a >= 1:
                if b >= 0:
                    while a > 1:
                        a = cls.div(a, 10)
                        c += 1
                    getcontext().prec = int((p := c*b)) + _DecimalPrecision + 2
                    return deciml((10 ** p) * (a ** b))
                if b < 0:
                    getcontext().prec = _DecimalPrecision + 2
                    return deciml(a ** b)
            if a < 1:
                if b >= 0:
                    getcontext().prec = _DecimalPrecision + 2
                    return deciml(a ** b)
                if b < 0:
                    while a < 1:
                        a = cls.mul(a, 10)
                        c += 1
                    getcontext().prec = int((p := -c*b)) + _DecimalPrecision + 2
                    return deciml((10 ** p) * (a ** b))
        except:
            return Decimal('NaN')
    
    @classmethod
    def ladd(cls, a: list[Decimal] | tuple[Decimal, ...], *b: list[Decimal] | tuple[Decimal, ...]) -> tuple[Decimal, ...]:
        try:
            r = list()
            for i in range(len(a)):
                r1 = a[i]
                for j in b:
                    r1 = cls.add(r1, j[i])
                r.append(r1)
            return tuple(r)
        except Exception as e:
            retrn('c', e)
    
    @classmethod
    def lsub(cls, a: list[Decimal] | tuple[Decimal, ...], *b: list[Decimal] | tuple[Decimal, ...]) -> tuple[Decimal, ...]:
        try:
            r = list()
            for i in range(len(a)):
                r1 = a[i]
                for j in b:
                    r1 = cls.sub(r1, j[i])
                r.append(r1)
            return tuple(r)
        except Exception as e:
            retrn('c', e)
    
    @classmethod
    def lmul(cls, a: list[Decimal] | tuple[Decimal , ...], *b: list[Decimal] | tuple[Decimal, ...]) -> tuple[Decimal, ...]:
        try:
            r = list()
            for i in range(len(a)):
                r1 = a[i]
                for j in b:
                    r1 = cls.mul(r1, j[i])
                r.append(r1)
            return tuple(r)
        except Exception as e:
            retrn('c', e)
    
    @classmethod
    def ldiv(cls, a: list[Decimal] | tuple[Decimal , ...], b: list[Decimal] | tuple[Decimal, ...]) -> tuple[Decimal, ...]:
        try:
            return tuple([cls.div(a[i], b[i]) for i in range(len(a))])
        except Exception as e:
            retrn('c', e)
    
    @classmethod
    def addl(cls, a: list[Decimal] | tuple[Decimal, ...]) -> Decimal:
        try:
            r = a[0]
            for i in a[1:]:
                r = cls.add(r, i)
            return r
        except Exception as e:
            retrn('c', e)
    
    @classmethod
    def subl(cls, a: list[Decimal] | tuple[Decimal, ...]) -> Decimal:
        try:
            r = a[0]
            for i in a[1:]:
                r = cls.sub(r, i)
            return r
        except Exception as e:
            retrn('c', e)
    
    @classmethod
    def mull(cls, a: list[Decimal] | tuple[Decimal, ...]) -> Decimal:
        try:
            r = a[0]
            for i in a[1:]:
                r = cls.mul(r, i)
            return r
        except Exception as e:
            retrn('c', e)



class trig:

    global _DecimalPrecision

    @staticmethod
    def sin(a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            a = Decimal(str(a))
            _DecimalPrecision += 2
            p = algbra.mul(constant.pi(_DecimalPrecision), 2)
            if a > p:
                _DecimalPrecision += (d := len(str(a)))
                a = '0.' + str(algbra.div(a, p)).split('.')[1]
                _DecimalPrecision -= d
                a = algbra.mul(Decimal(a), p)
            elif a < algbra.mul(-1, p):
                _DecimalPrecision += (d := len(str(a)))
                a = '-0.' + str(algbra.div(a, p)).split('.')[1]
                _DecimalPrecision -= d
                a = algbra.mul(Decimal(a), p)
            rp, n, d, c, a1 = None, a, 1, 1, algbra.pwr(a, 2)
            r = algbra.div(n, d)
            while r != rp:
                rp = r
                r = algbra.add(r, algbra.div((n := algbra.mul(n, a1, -1)), (d := d*(c+1)*((c := c+2)))))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')

    @staticmethod
    def cos(a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            a = Decimal(str(a))
            _DecimalPrecision += 2
            p = algbra.mul(constant.pi(_DecimalPrecision), 2)
            if a > p:
                _DecimalPrecision += (d := len(str(a)))
                a = '0.' + str(algbra.div(a, p)).split('.')[1]
                _DecimalPrecision -= d
                a = algbra.mul(Decimal(a), p)
            elif a < algbra.mul(-1, p):
                _DecimalPrecision += (d := len(str(a)))
                a = '-0.' + str(algbra.div(a, p)).split('.')[1]
                _DecimalPrecision -= d
                a = algbra.mul(Decimal(a), p)
            rp, n, d, c, r, a1 = 0, 1, 1, 0, 1, algbra.pwr(a, 2)
            while r != rp:
                rp = r
                r = algbra.add(r, algbra.div((n := algbra.mul(n, a1, -1)), (d := d*(c+1)*((c := c+2)))))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')

    @classmethod
    def tan(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            p = algbra.mul(constant.pi(_DecimalPrecision), 2)
            if a > p:
                _DecimalPrecision += (d := len(str(a)))
                a = '0.' + str(algbra.div(a, p)).split('.')[1]
                _DecimalPrecision -= d
                a = algbra.mul(Decimal(a), p)
            elif a < algbra.mul(-1, p):
                _DecimalPrecision += (d := len(str(a)))
                a = '-0.' + str(algbra.div(a, p)).split('.')[1]
                _DecimalPrecision -= d
                a = algbra.mul(Decimal(a), p)
            r = algbra.div(cls.sin(a), cls.cos(a))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')

    @classmethod
    def cosec(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            r = algbra.div(1, cls.sin(a))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')

    @classmethod
    def sec(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            r = algbra.div(1, cls.cos(a))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')

    @classmethod
    def cot(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            r = algbra.div(cls.cos(a), cls.sin(a))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')

    @classmethod
    def asin(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            if a < -1 or a > 1:
                raise Exception
            a1 = algbra.pwr(2, -0.5)
            if a > a1:
                r = cls.acos(algbra.pwr(algbra.sub(1, algbra.pwr(a, 2)), 0.5))
            elif a < algbra.mul(-1, a1):
                r = algbra.mul(-1, cls.acos(algbra.pwr(algbra.sub(1, algbra.pwr(a, 2)), 0.5)))
            else:
                a = Decimal(str(a))
                i, r, rn, a1, d1, d2, d3 = 0, (n := a), None, algbra.pwr(a, 2), 1, 1, 1
                while r != rn:
                    rn = r
                    i += 1
                    r = algbra.add(r, algbra.div((n := algbra.mul(n, (q := 2 * i), (q - 1), a1)), (d1 := d1 * 4)*((d2 := d2 * i) ** 2)*(d3 := d3 + 2)))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')

    @classmethod
    def acos(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            if a < -1 or a > 1:
                raise Exception
            a1 = algbra.pwr(2, -0.5)
            if a > a1:
                r = cls.asin(algbra.pwr(algbra.sub(1, algbra.pwr(a, 2)), 0.5))
            elif a < algbra.mul(-1, a1):
                r = algbra.add(algbra.mul(-1, cls.asin(a)), algbra.div(constant.pi(_DecimalPrecision), 2))
            else:
                a = Decimal(str(a))
                i = 0
                r = algbra.sub(algbra.div(constant.pi(_DecimalPrecision), 2), (n := a))
                rn, a1, d1, d2, d3 = None, algbra.pwr(a, 2), 1, 1, 1 
                while r != rn:
                    rn = r
                    i += 1
                    r = algbra.sub(r, algbra.div((n := algbra.mul(n, (q := 2 * i), (q - 1), a1)), (d1 := d1 * 4)*((d2 := d2 * i) ** 2)*(d3 := d3 + 2)))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')

    @classmethod
    def atan(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            a = Decimal(str(a))
            _DecimalPrecision += 2
            if a < 0:
                r = algbra.mul(-1, cls.asec(algbra.pwr(algbra.add(algbra.pwr(a, 2), 1), 0.5)))
            else:
                r = cls.asec(algbra.pwr(algbra.add(algbra.pwr(a, 2), 1), 0.5))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')

    @classmethod
    def acosec(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            r = cls.asin(algbra.div(1, a))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')

    @classmethod
    def asec(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            r = cls.acos(algbra.div(1, a))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')

    @classmethod
    def acot(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            r = cls.atan(algbra.div(1, a))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')
    
    def sinh(a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            r, rn, n, d, c, a1 = a, None, a, 1, 1, algbra.pwr(a, 2)
            while r != rn:
                rn = r
                r = algbra.add(r, algbra.div((n := algbra.mul(n, a1)), (d := d*(c+1)*((c := c+2)))))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')
    
    def cosh(a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            r, rn, n, d, c, a1 = 1, None, 1, 1, 0, algbra.pwr(a, 2)
            while r != rn:
                rn = r
                r = algbra.add(r, algbra.div((n := algbra.mul(n, a1)), (d := d*(c+1)*((c := c+2)))))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')
    
    @classmethod
    def tanh(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            r = algbra.div(cls.sinh(a), cls.cosh(a))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')
    
    @classmethod
    def cosech(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            r = algbra.div(1, cls.sinh(a))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')
    
    @classmethod
    def sech(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            r = algbra.div(1, cls.cosh(a))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')
    
    @classmethod
    def coth(cls, a: Decimal | int | float | str) -> Decimal:
        try:
            global _DecimalPrecision
            _DecimalPrecision += 2
            if deciml(a) == 0:
                raise Exception
            r = algbra.div(cls.cosh(a), cls.sinh(a))
            _DecimalPrecision -= 2
            return deciml(r)
        except:
            return Decimal('NaN')
    
class stat:

    def median(x: list[Decimal] | tuple[Decimal, ...]) -> Decimal:
        try:
            lm = algbra.div(len(x), 2)
            (x:= list(x)).sort()
            if (i := int(lm) - 1) == lm:
                return x[i]
            else:
                return(algbra.div(algbra.add(x[i], x[i+1]), 2))
        except:
            return Decimal('NaN')
    
    def mode(x: list | tuple) -> Decimal | tuple[Decimal]:
        try:
            d = dict()
            r = list()
            for i in x:
                d[i] = d.setdefault(i, 0) + 1
            c = max(d.values())
            for i in d.items():
                if i[1] == c:
                    r.append(i[0])
            return tuple(r)
        except:
            return Decimal('NaN')