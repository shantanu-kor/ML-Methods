from deciml import deciml
from decimal import Decimal
from terminate import retrn


class tint:

    @classmethod
    def iwgrp(cls, li: list | tuple) -> tuple[int]:
        try:
            if tlist(li) is not None:
                ln = list()
                for i in li:
                    ln.append((vi := cls.intw(i)))
                    if vi is None:
                        raise Exception(str(i) + " is not a whole number")    
                return ln
            else:
                raise Exception
        except Exception as e:
            retrn('c', e)
    
    # return true if i is valid element index
    @classmethod
    def ele(cls, i: int | float | list[int | float] | tuple[int | float], ln: int | float) -> int | list[int] | tuple[int]:
        try:
            ln = cls.intn(ln)
            if ln is None:
                raise Exception
            if (ti := i.__class__.__name__) == 'int' or ti == 'float':
                i = cls.intw(i)
                if i > ln - 1:
                    raise Exception(str(i) + " is more than " + str(ln - 1))
                return i
            elif ti == 'list' or ti == 'tuple':
                i = cls.iwgrp(i)
                if i is None:
                    raise Exception
            else:
                raise Exception("Invalid argument: i => int/float")
            for j in i:
                if j > ln - 1:
                    raise Exception(str(j) + " is more than " + str(ln - 1))
            return i
        except Exception as e:
            retrn('c', e)

    # check and return whole numbers
    @classmethod
    def intw(cls, i: int | float) -> int:
        try:
            if (j := int(i)) < 0:
                raise Exception(str(i) + " <= 0")
            else:
                return j
        except Exception as e:
            retrn('c', e)

    # check and return natural numbers
    @classmethod
    def intn(cls, i: int | float) -> int:
        try:
            if (j := int(i)) > 0:
                return j
            else:
                raise Exception(str(i) + " < 0")
        except Exception as e:
            retrn('c', e)

    # check and return int
    @staticmethod
    def int(i: int | float) -> int:
        try:
            return int(i)
        except Exception as e:
            retrn('c', e + "\n" + str(i) + " is not int")


class tdeciml:

    @staticmethod
    def dall(li: list | list[list] | tuple[tuple] | tuple) -> tuple[Decimal, ...] | tuple[tuple[Decimal, ...], ...]:
        try:
            if (tli := li.__class__.__name__) == 'tuple' or tli == 'list':
                if (tli0 := li[0].__class__.__name__) == 'list' or tli0 == 'tuple':
                    li1 = list()
                    for i in li:
                        li2 = list()
                        for j in i:
                            if (j1 := deciml(j)) is not Decimal('NaN'):
                                li2.append(j1)
                            else:
                                raise Exception(str(j) + " is " + j.__class__.__name__)
                        li1.append(tuple(li2))
                    return tuple(li1)
                else:
                    li1 = list()
                    for i in li:
                        if (i1 := deciml(i)) is not Decimal('NaN'):
                            li1.append(i1)
                        else:
                            raise Exception(str(j) + " is " + j.__class__.__name__)
                    return tuple(li1)
            else:
                raise Exception
        except Exception as e:
            retrn('c', str(e))

    # return if positive float
    @staticmethod
    def decip(a: float | int) -> Decimal:
        try:
            if (an := deciml(a)) is Decimal('NaN'):
                raise Exception
            if an <= 0:
                raise Exception(str(a) + " is not positive")
            return an
        except Exception as e:
            retrn('c', e)


def eqval(a, b) -> bool:
    try:
        if a == b:
            return True
        else:
            raise Exception(str(a) + " != " + str(b))
    except Exception as e:
        retrn('c', e)


def tbool(a: bool | list[bool] | tuple[bool], b=None) -> bool:
    try:
        if (ta := a.__class__.__name__) == 'bool':
            return True
        if (ta == 'list' or ta == 'tuple') and b is True:
            for i in a:
                if (ti := i.__class__.__name__) != 'bool':
                    raise Exception(ti + " is not bool")
            return True
        else:
            raise Exception(ta + " is not bool")
    except Exception as e:
        retrn('c', e)

# return True if matx
def tmatx(a, b=None) -> bool:
    try:
        if (ta := a.__class__.__name__) == 'matx':
            return True
        if (ta == 'list' or ta == 'tuple') and b is True:
            for i in a:
                if (ti := i.__class__.__name__) != 'matx':
                    raise Exception(ti + " is not matx")
            return True
        else:
            raise Exception(ta + " is not matx")
    except Exception as e:
        retrn('c', e)


# return True if tuple
def ttup(a: tuple | tuple[tuple, ...]) -> bool:
    try:
        if (ta := a.__class__.__name__) == 'tuple':
            if (ta0 := a[0].__class__.__name__) == ta:
                for i in range(len(a)):
                    if i == 0:
                        continue
                    if (ti := a[i].__class__.__name__) != ta0:
                        raise Exception(ti + " is not tuple")
                return True
            else:
                return True
        else:
            raise Exception(ta + " is not tuple")
    except Exception as e:
        retrn('c', e)


# return list if list
def tlist(a: list | list[list]) -> bool:
    try:
        if (ta := a.__class__.__name__) == 'list':
            if (ta0 := a[0].__class__.__name__) == ta:
                for i in range(len(a)):
                    if i == 0:
                        continue
                    if (ti := a[i].__class__.__name__) != ta0:
                        raise Exception(ti + " is not list")
                return True
            else:
                return True
        else:
            raise Exception(ta + " is not list")
    except Exception as e:
        retrn('c', e)


# return True if lengths of lists are equal
def eqllen(a: list[list] | tuple[list, ...] | tuple[tuple, ...] | list[tuple]) -> bool:
    try:
        if (ta := a.__class__.__name__) == 'tuple' or ta == 'list':
            l0 = len(a[0])
            c = 0
            if (l := len(a)) == 1:
                return True
            while (c := c + 1) != l:
                if (li := len(a[c])) != l0:
                    raise Exception(li + " != " + l0)
                return True
        else:
            raise Exception("Invalid argument: a => list/tuple")
    except Exception as e:
        retrn('c', e)


# return true if data
def tdata(d, b = None) -> bool:
    try:
        if (td := d.__class__.__name__) == 'data':
            return True
        if (td == 'list' or td == 'tuple') and b is True:
            for i in d:
                if (ti := i.__class__.__name__) != 'data':
                    raise Exception(ti + " is not data")
            return True
        else:
            raise Exception(td + " is not data")
    except Exception as e:
        retrn('c', e)


class tfunc:

    @staticmethod
    def axn(a) -> bool:
        try:
            if (ta := a.__class__.__name__) == 'axn':
                return True
            else:
                raise Exception(ta + " is not axn")
        except Exception as e:
            retrn('c', e)

    @staticmethod
    def poly(a) -> bool:
        try:
            if (ta := a.__class__.__name__) == 'poly':
                return True
            else:
                raise Exception(ta + " is not poly")
        except Exception as e:
            retrn('c', e)

    @staticmethod
    def apolyn(a) -> bool:
        try:
            if (ta := a.__class__.__name__) == 'apolyn':
                return True
            else:
                raise Exception(ta + " is not apolyn")
        except Exception as e:
            retrn('c', e)


class tdict:

    @staticmethod
    def dic(a: dict) -> bool:
        try:
            if (ta := a.__class__.__name__) == 'dict':
                return True
            else:
                raise Exception(ta + " is not dict")
        except Exception as e:
            retrn('c', e)

    @classmethod
    def matchkeys(cls, a: dict, b: dict) -> bool:
        try:
            if cls.dic(a) is None or cls.dic(b) is None:
                raise Exception
            a = a.keys()
            b = list(b.keys())
            if (la := len(a)) != (lb := len(b)):
                raise Exception(la + " != " + lb)
            [b.remove(i) for i in a]
            if len(b) == 0:
                return True
            else:
                raise Exception
        except Exception:
            retrn('c', "Keys are not same")
