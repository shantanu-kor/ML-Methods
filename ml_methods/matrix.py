import math
from decimal import Decimal
from cmdexec import Terminate, Comp


def pwr(a: Decimal, b: Decimal, chk=True, ret=False) -> Decimal:
    try:
        match chk:
            case False:
                pass
            case True:
                a = Comp.tdeciml(a)
                b = Comp.tdeciml(b)
                if a is None or b is None:
                    raise Exception
            case _:
                raise Exception("Invalid argument: chk => bool")
        if a == 0 and b == 0:
            return Decimal('1')
        else:
            try:
                return a ** b
            except:
                return Decimal('NaN')
    except Exception as e:
        Terminate.retrn(ret, e)        


class Matx(Comp):
    
    @classmethod
    def matrix(cls, li: list[list] | tuple[tuple] | list | tuple, chk=True) -> tuple[tuple[Decimal]]:
        try:
            tli = li.__class__.__name__
            match chk:
                case True:
                    match tli:
                        case 'list':
                            li = Comp.dlist(li)
                            if li is None:
                                raise Exception("Invalid argument: li")
                            if li[0].__class__.__name__ == 'list':
                                if Comp.lenlist(li) is None:
                                    raise Exception("Invalid argument: li")
                                return tuple([tuple(i) for i in li])
                            else:
                                return tuple(li),
                        case 'tuple':
                            li = Comp.dtup(li)
                            if li is None:
                                raise Exception("Invalid argument: li")
                            if li[0].__class__.__name__ == 'tuple':
                                if Comp.lentup(li) is None:
                                    raise Exception("Invalid argument: li")
                                return li
                            else:
                                return li,
                        case 'matx':
                            return li.matx
                        case _:
                            raise Exception("Invalid argument: li => list/tuple/matx")
                case False:
                    match tli:
                        case 'tuple':
                            if li[0].__class__.__name__ == 'float':
                                return tuple(Decimal(str(i)) for i in li),
                            elif li[0].__class__.__name__ == 'Decimal':
                                return li,
                            elif li[0].__class__.__name__ == 'tuple':
                                return li
                            else:
                                raise Exception("Invalid argument: li")
                        case 'matx':
                            return li.matx
                        case _:
                            raise Exception("Invalid argument: li => tuple/matx")
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(True, e)


class matx(Matx):
    
    def __init__(self, li: list | tuple, chk=True, ret=False) -> None:
        if (m := Matx.matrix(li, chk)) is not None:
            self._matx = m
            self.collen = len(m)
            self.rowlen = len(m[0])
            del m
            if self.rowlen == self.collen:
                self.sqmatx = True
            else:
                self.sqmatx = False
        else:
            Terminate.retrn(ret, "Error: Invalid matx")

    @property
    def matx(self) -> tuple:
        return self._matx

    @matx.setter
    def matx(self, li: list | tuple) -> None:
        if (m := Matx.matrix(li)) is not None:
            self._matx = m
            self.collen = len(m)
            self.rowlen = len(m[0])
            del m
            if self.rowlen == self.collen:
                self.sqmatx = True
            else:
                self.sqmatx = False
        else:
            Terminate.retrn(False, "Error: Invalid matx")
    
    # prints the value of matx object
    @matx.getter
    def pmatx(self) -> None:
        print("matx(")
        for k in [[float(j) for j in i] for i in self.matx]:
            print('|', str(k)[1:-1], '|')
        print(')\n')

    # returns matx as a list
    def matxl(self) -> list:
        return [list(i) for i in self.matx]
    
    def pop(self, i: int, r=True, chk=True, ret=False) -> tuple[Decimal]:
        try:
            match chk:
                case False:
                    pass
                case True:
                    i = Comp.intele(i, self.collen)
                    if i is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            match r:
                case True:
                    m = list(self.matx)
                    p = m.pop(i)
                    self.matx = tuple(m)
                case False:
                    m = self.matxl()
                    p = list()
                    for j in range(self.collen):
                        p.append(m[j].pop(i))
                        m[j] = tuple(m[j])
                    self.matx = tuple(m)
                case _:
                    raise Exception("Invalid argument: r => bool")
            del m
            return tuple(p)
        except Exception as e:
            Terminate.retrn(ret, e)

    # return element at i,j of matrix
    def mele(self, i: int, j: int, chk=True, ret=False) -> Decimal:
        try:
            match chk:
                case False:
                    return self.matx[i][j]
                case True:
                    i = Comp.intele(i, self.collen)
                    if i is None:
                        raise Exception
                    j = Comp.intele(j, self.rowlen)
                    if j is None:
                        raise Exception
                    return self.matx[i][j]
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    # return tuple of i'th row
    def mrow(self, i: int, chk=True, ret=False) -> tuple[Decimal]:
        try:
            match chk:
                case False:
                    return self.matx[i]
                case True:
                    i = Comp.intele(i, self.collen)
                    if i is None:
                        raise Exception
                    return self.matx[i]
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns tuple of i'th column
    def mcol(self, j: int, chk=True, ret=False) -> tuple[Decimal]:
        try:
            match chk:
                case False:
                    return tuple([self.matx[i][j] for i in range(self.collen)])
                case True:
                    j = Comp.intele(j, self.rowlen)
                    if j is None:
                        raise Exception
                    return tuple([self.matx[i][j] for i in range(self.collen)])
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(ret, e)


class matutils(matx, Comp):
    
    # returns identity matrix of size nxn
    @classmethod
    def sclrm(cls, n: int, el: Decimal, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    n = Comp.tintn(n)
                    el = Comp.tdeciml(el)
                    if n is None or el is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            m = list()
            for i in range(n):
                l1 = list()
                for j in range(n):
                    if i == j:
                        l1.append(el)
                    else:
                        l1.append(Decimal('0.0'))
                m.append(tuple(l1))
            return matx(tuple(m), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns 0 matrix of size mxn
    @classmethod
    def eqelm(cls, m: int, n: int, i: Decimal, chk=True, ret=False) -> matx:
        try:
            match chk:
                case True:
                    return matx(tuple([tuple([i for _ in range(n)]) for _ in range(m)]), False, True)
                case False:
                    n = Comp.tintn(n)
                    m = Comp.tintn(m)
                    i = Comp.tdeciml(i)
                    if m is None or n is None or i is None:
                        raise Exception
                    return matx(tuple([tuple([i for _ in range(n)]) for _ in range(m)]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def addmatx(cls, a: matx, b: matx, r=False, chk=True, ret=False) -> matx:
        try:
            match chk:
                case True:
                    if Comp.tmatx([a, b], True) is None:
                        raise Exception
                    match r:
                        case False:
                            if Comp.eqval(b.collen, a.collen) is None:
                                raise Exception
                        case True:
                            if Comp.eqval(b.rowlen, a.rowlen) is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: r => bool")
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: chk => bool")
            match r:
                case False:
                    return matx(tuple([tuple(list(a.mrow(i, False, True)) + list(b.mrow(i, False, True))) for i in range(a.collen)]), False, True)
                case True:
                    return matx(tuple(list(a.matx) + list(b.matx)), False, True)
                case _:
                    raise Exception("Invalid argument: r => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def maddval(cls, a: matx, x: Decimal, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    a1 = cls.eqelm(a.collen, 1, x, False, True)
                    return cls.addmatx(a1, a, False, False, True)
                case True:
                    if Comp.tmatx(a) is None:
                        raise Exception
                    x = Comp.tdeciml(x)
                    if x is None:
                        raise Exception
                    a1 = cls.eqelm(a.collen, 1, x, False, True)
                    return cls.addmatx(a1, a, False, False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    # convert list x to x
    @classmethod
    def matlxtox(cls, a: matx, chk=True, ret=False) -> tuple:
        try:
            match chk:
                case False:
                    return tuple([matx(i, False, True) for i in a.matx])
                case True:
                    if Comp.tmatx(a) is None:
                        raise Exception
                    return tuple([matx(i, False, True) for i in a.matx])
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def matxtolx(cls, a: tuple | list, chk=True, ret=False) -> matx:
        try:
            x = list()
            match chk:
                case False:
                    for i in a:
                        x.append(i.matx[0])
                case True:
                    if Comp.tmatx(a, True) is None:
                        raise Exception
                    ar = a[0].rowlen
                    for i in a:
                        if Comp.eqval(i.collen, 1) is None or Comp.eqval(i.rowlen, ar) is None:
                            raise Exception
                        x.append(i.matx[0])
                case _:
                    raise Exception("Invalid argument: chk => bool")
            return matx(tuple(x), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns row or column elements of the matrix
    @classmethod
    def gele(cls, a: matx, b: list, r=False, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if Comp.tmatx(a) is None or b is None:
                        raise Exception
                    match r:
                        case True:
                            b = Comp.intele(b, a.collen)
                        case False:
                            b = Comp.intele(b, a.rowlen)
                        case _:
                            raise Exception("Invalid argument: r => bool")
                case _:
                    raise Exception("Invalid argument: chk => bool")
            match r:
                case True:
                    m = tuple([a.mrow(i, False, True) for i in b])
                case False:
                    m = tuple([a.mcol(i, False, True) for i in b])
                case _:
                    raise Exception("Invalid argument: r => bool")
            return matx(m, False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns the transpose of the matrix
    @classmethod
    def tpose(cls, a: matx, chk=True, ret=False) -> matx:
        try:
            return cls.gele(a, [i for i in range(a.rowlen)], False, chk, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns the co-factor of the matrix element
    @classmethod
    def cofac(cls, a: matx, b: int, c: int, chk=True, ret=False) -> Decimal:
        try:
            match chk:
                case True:
                    if Comp.tmatx(a) is None:
                        raise Exception
                    if a.sqmatx is False:
                        raise Exception("Error: Not a square matrix")
                    d = Comp.intele([b, c], a.rowlen)
                    if d is None:
                        raise Exception
                    b = d[0]
                    c = d[1]
                    del d
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: chk => bool")
            a = matx(a, True, True)
            p = pwr(Decimal('-1'), Decimal(str(b + c)), False, True)
            a.pop(c, False, False, True)
            a.pop(b, chk=False, ret=True)
            dn = cls.dnant(a, False, True)
            cfc = p * dn
            return cfc
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns the determinant of the matrix
    @classmethod
    def dnant(cls, a: matx, chk=True, ret=False) -> Decimal:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if Comp.tmatx(a) is None:
                        raise Exception
                    if a.sqmatx is False:
                        raise Exception("Error: Not a square matrix")
                case _:
                    raise Exception("Invalid argument: chk => bool")
            a = matx(a, True, True)
            if (lr := a.rowlen) == 1:
                d = a.mele(0, 0, False, True)
            else:
                d = 0
                ep = None
                ele = a.mele(0, 0, False, True)
                li = a.mrow(0, True)
                if ele == 0:
                    for i in range(lr):
                        if i > 0:
                            if li[i] != 0:
                                e = li[i]
                                ep = i
                    if ep is None:
                        return Decimal('0')
                else:
                    ep = 0
                    e = ele
                for i in range(lr):
                    if i != ep:
                        ele = li[i]
                        fac = -1 * ele / e
                        a.matx = cls.tform(a, i, ep, fac, False, False, True)
                cfc = cls.cofac(a, 0, ep, False, True)
                if cfc is None:
                    raise Exception
                else:
                    d += e * cfc
            return d
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns adjoint matrix of the matrix
    @classmethod
    def adjnt(cls, a: matx, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    return cls.tpose(matx(tuple([tuple([cls.cofac(a, i, j, False, True) for j in range(a.rowlen)]) for i in range(a.collen)]), False, True), False, True)
                case True:
                    if Comp.tmatx(a) is None:
                        raise Exception
                    if a.sqmatx is False:
                        raise Exception("Error: Not a square matrix")
                    return cls.tpose(matx(tuple([tuple([cls.cofac(a, i, j, False, True) for j in range(a.rowlen)]) for i in range(a.collen)]), False, True), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            print(e)
            Terminate.retrn(ret, e)

    # returns inverse matrix of the matrix
    @classmethod
    def invse(cls, a: matx, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if Comp.tmatx(a) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            det = cls.dnant(a, False, True)
            if det is None:
                raise Exception
            if det == 0:
                raise Exception("Error: Determinant is 0,\nInverse DNE!")
            return cls.smult(1 / det, cls.adjnt(a, False, True), False, True)
        except Exception as e:
            print(e)
            Terminate.retrn(ret, e)

    # returns inverse matrix of the matrix using matrix transformation
    @classmethod
    def invsednant(cls, a: matx, chk=True, ret=False) -> Decimal:
        try:
            match chk:
                case True:
                    if Comp.tmatx(a) is None:
                        raise Exception
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: chk => bool")
            a = matx(a, True, False)
            det = cls.dnant(a, False, True)
            if det is None:
                raise Exception
            if det == 0:
                raise Exception("Error: Determinant is 0,\nInverse DNE!")
            elif det > 0:
                a.matx = cls.smult(pwr(det, Decimal(-1 / a.collen), False, True), a, False, True)
            else:
                a.matx = cls.smult(-pwr(-det, Decimal(-1 / a.collen), False, True), a, False, True)
            b = cls.sclrm(a.rowlen, Decimal('1.0'), False, True)
            for i in range(a.collen):
                ele = a.mele(i, i, False, True)
                if ele != 1:
                    for j in range(a.rowlen):
                        if j > i:
                            el = a.mele(i, j, False, True)
                            if el != 0:
                                a.matx = cls.tform(a, i, j, (1 - ele) / el, False, False, True)
                                b.matx = cls.tform(b, i, j, (1 - ele) / el, False, False, True)
                                break
                            else:
                                if j == a.rowlen - 1:
                                    if ele != 0:
                                        a.matx = cls.tform(a, i + 1, i, Decimal('1'), False, False, True)
                                        a.matx = cls.tform(a, i, i + 1, (1 / ele) - 1, False, False, True)
                                        b.matx = cls.tform(b, i + 1, i, Decimal('1'), False, False, True)
                                        b.matx = cls.tform(b, i, i + 1, (1 / ele) - 1, False, False, True)
                                    else:
                                        raise Exception("Error: Invalid Matrix Inverse")
                ele = a.mele(i, i, False, True)
                row = a.mrow(i, False, True)
                col = a.mcol(i, False, True)
                for j in range(a.rowlen):
                    if j > i:
                        el = row[j]
                        e = col[j]
                        a.matx = cls.tform(a, j, i, -el / ele, False, False, True)
                        b.matx = cls.tform(b, j, i, -el / ele, False, False, True)
                        a.matx = cls.tform(a, j, i, -e / ele, True, False, True)
                        b.matx = cls.tform(b, j, i, -e / ele, True, False, True)
                        del e
                        del el
                del ele
            if det > 0:
                b.matx = cls.smult(pwr(det, Decimal(-1 / a.collen), False, True), b, False, True)
            if det < 0:
                b.matx = cls.smult(-pwr(-det, Decimal(-1 / a.collen), False, True), b, False, True)
            return cls.dnant(b, False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns matrix after row or column tranformation
    @classmethod
    def tform(cls, a: matx, b: int, c: int, d: Decimal, r=False, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    d = Comp.tdeciml(d)
                    if Comp.tmatx(a) is None or d is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            m = cls.gele(a, [b, c], r, chk, True)
            if m is None:
                raise Exception
            m = m.matx
            match r:
                case True:
                    lr = a.rowlen
                    a = list(a.matx)
                    a[b] = tuple([m[0][i] + (d * m[1][i]) for i in range(lr)])
                    del m
                    return matx(tuple(a), False, True)
                case False:
                    lc = a.collen
                    a = list(cls.tpose(a, False, True).matx)
                    a[b] = tuple([m[0][i] + (d * m[1][i]) for i in range(lc)])
                    del m
                    return cls.tpose(matx(tuple(a), False, True), False, True)
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns sum of two matrices
    @classmethod
    def madd(cls, a: matx, b: matx, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    return matx(tuple([tuple([a.mele(i, j, False, True) + b.mele(i, j, False, True) for j in range(a.rowlen)]) for i in range(a.collen)]), False, True)
                case True:
                    if Comp.tmatx([a, b], True) is None:
                        raise Exception
                    alc = a.collen
                    alr = a.rowlen
                    blc = b.collen
                    blr = b.rowlen
                    if Comp.eqval([alc, alr], [blc, blr]) is None:
                        raise Exception
                    return matx(tuple([tuple([a.mele(i, j, False, True) + b.mele(i, j, False, True) for j in range(alr)]) for i in range(alc)]), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def saddcnst(cls, a: tuple | list, b: matx, r=False, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    match a.__class__.__name__:
                        case 'tuple':
                            a = Comp.dtup(a)
                            if a is None:
                                raise Exception
                        case 'list':
                            a = Comp.dlist(a)
                            if a is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: a => tuple/list")
                    if Comp.tmatx(b) is None:
                        raise Exception
                    match r:
                        case True:
                            if Comp.eqval(len(a), b.collen) is None:
                                raise Exception
                        case False:
                            if Comp.eqval(len(a), b.rowlen) is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: r => bool")
                case _:
                    raise Exception("Invalid argument: chk => bool")
            if r is True:
                b = cls.matlxtox(cls.tpose(b, False, True), False, True)
                a = matx(tuple(a), False, True)
                if a is None:
                    raise Exception
                return cls.tpose(matx(tuple([cls.madd(a, i, False, True).matx[0] for i in b]), False, True), False, True)
            else:
                b = cls.matlxtox(b, False, True)
                a = matx(tuple(a), False, True)
                if a is None:
                    raise Exception
                return matx(tuple([cls.madd(a, i, False, True).matx[0] for i in b]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns difference of two matrices
    @classmethod
    def msub(cls, a: matx, b: matx, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    return matx(tuple([tuple([a.mele(i, j, False, True) - b.mele(i, j, False, True) for j in range(a.rowlen)]) for i in range(a.collen)]), False, True)
                case True:
                    if Comp.tmatx([a, b], True) is None:
                        raise Exception
                    alc = a.collen
                    alr = a.rowlen
                    blc = b.collen
                    blr = b.rowlen
                    if Comp.eqval([alc, alr], [blc, blr]) is None:
                        raise Exception
                    return matx(tuple([tuple([a.mele(i, j, False, True) - b.mele(i, j, False, True) for j in range(alr)]) for i in range(alc)]), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns matrix after scalar multiplication
    @classmethod
    def smult(cls, a: Decimal, b: matx, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    return matx(tuple([tuple([a * b.mele(i, j, False, True) for j in range(b.rowlen)]) for i in range(b.collen)]), False, True)
                case True:
                    a = Comp.tdeciml(a)
                    if a is None:
                        raise Exception
                    if Comp.tmatx(b) is None:
                        raise Exception
                    blc = b.collen
                    blr = b.rowlen
                    return matx(tuple([tuple([a * b.mele(i, j, False, True) for j in range(blr)]) for i in range(blc)]), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def smultfac(cls, a: tuple | list, b: matx, r=True, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    match a.__class__.__name__:
                        case 'tuple':
                            a = Comp.dtup(a)
                            if a is None:
                                raise Exception
                        case 'list':
                            a = Comp.dlist(a)
                            if a is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: a => tuple/list")
                    if Comp.tmatx(b) is None:
                        raise Exception
                    match r:
                        case True:
                            if Comp.eqval(len(a), b.collen) is None:
                                raise Exception
                        case False:
                            if Comp.eqval(len(a), b.rowlen) is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: r => bool")
                case _:
                    raise Exception("Invalid argument: chk => bool")
            if r is True:
                b = cls.matlxtox(b, False, True)
                bn = list()
                for i in enumerate(a):
                    bn.append(cls.smult(i[1], b[i[0]], False, True))
                return cls.matxtolx(tuple(bn), False, True)
            else:
                b = cls.matlxtox(cls.tpose(b, False, True), False, True)
                bn = list()
                for i in enumerate(a):
                    bn.append(cls.smult(i[1], b[i[0]], False, True))
                return cls.tpose(cls.matxtolx(tuple(bn), False, True), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns matrix after matrix multiplication
    @classmethod
    def mmult(cls, a: matx, b: matx, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    return matx(tuple([tuple([sum([a.mele(i, j, False, True) * b.mele(j, k, False, True) for j in range(a.rowlen)]) for k in range(b.rowlen)]) for i in range(a.collen)]), False, True)
                case True:
                    if Comp.tmatx([a, b], True) is None:
                        raise Exception
                    alc = a.collen
                    alr = a.rowlen
                    blc = b.collen
                    blr = b.rowlen
                    if Comp.eqval(alr, blc) is None:
                        raise Exception
                    return matx(tuple([tuple([sum([a.mele(i, j, False, True) * b.mele(j, k, False, True) for j in range(alr)]) for k in range(blr)]) for i in range(alc)]), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def uldcompose(cls, a: matx, chk=True, ret=False) -> tuple:
        try:
            match chk:
                case True:
                    if Comp.tmatx(a) is None:
                        raise Exception
                    if a.sqmatx is None:
                        raise Exception
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: chk => bool")
            ut = list()
            lt = list()
            dia = list()
            for i in range(a.collen):
                ut1 = list()
                lt1 = list()
                for j in range(a.rowlen):
                    if j < i:
                        lt1.append(a.mele(i, j, False, True))
                        ut1.append(Decimal('0.0'))
                    elif i == j:
                        dia.append(a.mele(i, j, False, True))
                        lt1.append(Decimal('0.0'))
                        ut1.append(Decimal('0.0'))
                    else:
                        ut1.append(a.mele(i, j, False, True))
                        lt1.append(Decimal('0.0'))
                ut.append(tuple(ut1))
                lt.append(tuple(lt1))
            return matx(tuple(ut), False, True), matx(tuple(lt), False, True), matx((tuple(dia), ), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def dpose(cls, a: matx, li: list | tuple, r=False, chk=True, ret=False) -> tuple:
        try:
            match chk:
                case True:
                    if Comp.tmatx(a) is None:
                        raise Exception
                    match li.__class__.__name__:
                        case 'list':
                            li = Comp.iwlist(li)
                            if li is None:
                                raise Exception
                        case 'tuple':
                            li = Comp.iwtup(li)
                            if li is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: li => list/tuple")
                    match r:
                        case False:
                            if Comp.eqval(sum(li), a.rowlen) is None:
                                raise Exception
                        case True:
                            if Comp.eqval(sum(li), a.collen) is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: r => bool")
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: chk => bool")
            i = 0
            ln = list()
            for j in li:
                ln.append([i+k for k in range(j)])
                i += j
            if r is False:
                return tuple([cls.tpose(cls.gele(a, i, False, False, True), False, True) for i in ln])
            else:
                return tuple([cls.gele(a, i, True, False, True) for i in ln])
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def addmel(cls, a: matx, li: list[list] | tuple[list], r=False, chk=True, ret=False) -> matx:
        try:
            an = list()
            for i in li:
                i1 = list()
                for j in cls.tpose(cls.gele(a, i, r, chk, True), False, True).matx:
                    i1.append(sum(j))
                an.append(tuple(i1))
            return matx(tuple(an), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def multmel(cls, a: matx, li: list[list] | tuple[list], r=False, chk=True, ret=False) -> matx:
        try:
            an = list()
            for i in li:
                i1 = list()
                for j in cls.tpose(cls.gele(a, i, r, chk, True), False, True).matx:
                    k1 = 1
                    for k in j:
                        k1 = k1*k
                    i1.append(k1)
                an.append(tuple(i1))
            return matx(tuple(an), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def powmel(cls, an: list | tuple[Decimal, Decimal], a: matx, li: list, r=False, chk=True, ret=False) -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    match an.__class__.__name__:
                        case 'tuple':
                            an = Comp.dtup(an)
                            if an is None:
                                raise Exception
                        case 'list':
                            an = Comp.dlist(an)
                            if an is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: a => tuple/list")
                    if Comp.eqval(len(an), 2) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            return matx(tuple([tuple([pwr(an[0]*j, an[1], False, True) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def logmel(cls, an: list | tuple[Decimal, Decimal], a: matx, li: list, r=False, chk=True, ret=False) -> matx:
        match chk:
            case False:
                pass
            case True:
                match an.__class__.__name__:
                    case 'tuple':
                        an = Comp.dtup(an)
                        if an is None:
                            raise Exception
                    case 'list':
                        an = Comp.dlist(an)
                        if an is None:
                            raise Exception
                    case _:
                        raise Exception("Invalid argument: a => tuple/list")
                if Comp.eqval(len(an), 2) is None:
                    raise Exception
            case _:
                raise Exception("Invalid argument: chk => bool")
        return matx(tuple([tuple([Decimal(str(math.log(j*an[0], an[1]))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)

    @classmethod
    def expomel(cls, an: list | tuple[Decimal, Decimal], a: matx, li: list, r=False, chk=True, ret=False) -> matx:
        match chk:
            case False:
                pass
            case True:
                match an.__class__.__name__:
                    case 'tuple':
                        an = Comp.dtup(an)
                        if an is None:
                            raise Exception
                    case 'list':
                        an = Comp.dlist(an)
                        if an is None:
                            raise Exception
                    case _:
                        raise Exception("Invalid argument: a => tuple/list")
                if Comp.eqval(len(an), 2) is None:
                    raise Exception
            case _:
                raise Exception("Invalid argument: chk => bool")
        return matx(tuple([tuple([pwr(an[0], j*an[1], False, True) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)

    @classmethod
    def trigmel(cls, n: Decimal, a: matx, li: list, r=False, f='cos', chk=True, ret=False) -> matx:
        match chk:
            case False:
                pass
            case True:
                n = Comp.tdeciml(n)
                if n is None:
                    raise Exception
            case _:
                raise Exception("Invalid argument: chk => bool")
        match f:
            case 'cos':
                return matx(tuple([tuple([Decimal(str(math.cos(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'sin':
                return matx(tuple([tuple([Decimal(str(math.sin(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'tan':
                return matx(tuple([tuple([Decimal(str(math.tan(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'sec':
                return matx(tuple([tuple([1 / Decimal(str(math.cos(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'cosec':
                return matx(tuple([tuple([1 / Decimal(str(math.sin(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'cot':
                return matx(tuple([tuple([1 / Decimal(str(math.tan(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'acos':
                return matx(tuple([tuple([Decimal(str(math.acos(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'asin':
                return matx(tuple([tuple([Decimal(str(math.asin(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'atan':
                return matx(tuple([tuple([Decimal(str(math.atan(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'asec':
                return matx(tuple([tuple([Decimal(str(math.acos(1 / n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'acosec':
                return matx(tuple([tuple([Decimal(str(math.asin(1 / n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'acot':
                return matx(tuple([tuple([Decimal(str(math.atan(1 / n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'sinh':
                return matx(tuple([tuple([Decimal(str(math.sinh(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'cosh':
                return matx(tuple([tuple([Decimal(str(math.cosh(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)
            case 'tanh':
                return matx(tuple([tuple([Decimal(str(math.tanh(n*j))) for j in i]) for i in cls.gele(a, li, r, chk, True).matx]), False, True)


# print("1")
# z = [1, 2, 3]
# a1 = [z, [5, 2, int(6)], [5, 5, 8]]
# b = [[1, 3, 6], [8, 5, 6], [7, 4, 5]]
# a = matx(a1)
# a.pmatx
# matutils.saddcnst((1, 2, 3), a).pmatx
# matutils.addmel(a, [[0,1], [0,1,2]]).pmatx
# matutils.addmel(a, [[0,1], [0,1,2]], True).pmatx
# matutils.powmel([1, 2], a, [0,2]).pmatx
# x = matutils.dpose(a, [1,2], True)
# for i in x:
#     i.pmatx
# a.matx = a.matx
# a.pmatx
# print(a.matxl())
# a.pmatx
# b = matx(b)
# matutils.tpose(a).pmatx
# print(a.mele(0, 0))
# a.pmatx
# print(a.rowlen, a.collen)
# a1 = [0, 0, 0]
# a.pmatx
# c = a.matxl()
# c[0] = [0, 0, 0]
# a.pmatx
# print(c)
# a.matx = [[1, 2, 3], [5, 0, 6], [5, 5, 8]]
# a.pmatx
# print("2")
# matutils.addmatx(a, b).pmatx
# matutils.smultfac(tuple([2, 1, 2]), a).pmatx
# matutils.gele(a, [0, 1]).pmatx
# matutils.gele(a, [1, 0], True).pmatx
# print(a.sqmatx)
# c = [0, 0]
# print(matx(c).sqmatx)
# print(matutils.dnant(a), matutils.dnant(b))
# matutils.invse(a).pmatx
# matutils.invse(b).pmatx
# print(matutils.invsednant(b), matutils.dnant(matutils.invse(b)))
# matutils.madd(a, b).pmatx
# matutils.mmult(a, b).pmatx
# a = matx([11, 10, 100])
# matutils.matlxtox(a)
# matutils.maddval(a, Decimal('1.0')).pmatx
# matutils.matxtolx([matx([1,2,3]), matx([2,3,4])]).pmatx
