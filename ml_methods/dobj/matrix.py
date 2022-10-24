from utils.deciml import deciml, algbra as alg, trig, Decimal
from utils.cmpr import tmatx, eqval, tdeciml, eqllen, tint
from utils.terminate import retrn


class matx:
    
    def __init__(self, li: list | tuple, chk=True, ret='a') -> None:
        def __matrix(li: list[list] | tuple[tuple] | list | tuple, chk=True) -> tuple[tuple[tuple[Decimal, ...], ...], int, int, bool]:
            try:
                tli = li.__class__.__name__
                match chk:
                    case True:
                        if tli == 'list' or tli == 'tuple':
                            if (tli0 := li[0].__class__.__name__) == 'tuple' or tli0 == 'list':
                                if eqllen(li) is None:
                                    raise Exception("Invalid argument: li")
                            else:
                                li = li,
                            if (li := tdeciml.dall(li)) is None:
                                raise Exception("Invalid argument: li")
                        elif tli == 'matx':
                            return li.matx, li.collen, li.rowlen, li.sqmatx
                        else:
                            raise Exception("Invalid argument: li => list/tuple/matx")
                    case False:
                        match tli:
                            case 'tuple':
                                if li[0].__class__.__name__ == 'float':
                                    li = tuple(deciml(i) for i in li),
                                elif li[0].__class__.__name__ == 'Decimal':
                                    li = li,
                                elif li[0].__class__.__name__ == 'tuple':
                                    pass
                                else:
                                    raise Exception("Invalid argument: li")
                            case 'matx':
                                return li.matx, li.collen, li.rowlen, li.sqmatx
                            case _:
                                raise Exception("Invalid argument: li => tuple/matx")
                    case _:
                        raise Exception("Invalid argument: chk => bool")
                lc, lr = len(li), len(li[0])
                if lr == lc:
                    sq = True
                else:
                    sq = False
                return li, lc, lr, sq
            except Exception as e:
                retrn(True, e)
        if (m := __matrix(li, chk)) is not None:
            self.__matx, self.__collen, self.__rowlen, self.__sqmatx = m
            del m
            self.__dnant, self.__invse, self.__invsednant, self.__cofacm, self.__adjnt, self.__tpose = None, None, None, None, None, None
        else:
            retrn(ret, "Error: Invalid matx")

    @property
    def matx(self) -> tuple:
        return self.__matx
    
    @matx.setter
    def matx(self, li: list | tuple) -> None:
        def __matrix(li: list[list] | tuple[tuple] | list | tuple, chk=True) -> tuple[tuple[tuple[Decimal, ...], ...], int, int, bool]:
            try:
                tli = li.__class__.__name__
                match chk:
                    case True:
                        if tli == 'list' or tli == 'tuple':
                            if (tli0 := li[0].__class__.__name__) == 'tuple' or tli0 == 'list':
                                if eqllen(li) is None:
                                    raise Exception("Invalid argument: li")
                            else:
                                li = li,
                            if (li := tdeciml.dall(li)) is None:
                                raise Exception("Invalid argument: li")
                        elif tli == 'matx':
                            return li.matx, li.collen, li.rowlen, li.sqmatx
                        else:
                            raise Exception("Invalid argument: li => list/tuple/matx")
                    case False:
                        match tli:
                            case 'tuple':
                                if li[0].__class__.__name__ == 'float':
                                    li = tuple(deciml(i) for i in li),
                                elif li[0].__class__.__name__ == 'Decimal':
                                    li = li,
                                elif li[0].__class__.__name__ == 'tuple':
                                    pass
                                else:
                                    raise Exception("Invalid argument: li")
                            case 'matx':
                                return li.matx, li.collen, li.rowlen, li.sqmatx
                            case _:
                                raise Exception("Invalid argument: li => tuple/matx")
                    case _:
                        raise Exception("Invalid argument: chk => bool")
                lc, lr = len(li), len(li[0])
                if lr == lc:
                    sq = True
                else:
                    sq = False
                return li, lc, lr, sq
            except Exception as e:
                retrn(True, e)
        if (m := __matrix(li)) is not None:
            self.__matx, self.__collen, self.__rowlen, self.__sqmatx = m
            del m
            self.__dnant, self.__invse, self.__invsednant, self.__cofacm, self.__adjnt, self.__tpose = None, None, None, None, None, None
        else:
            retrn('a', "Error: Invalid matx")
    
    @property
    def collen(self) -> int:
        return self.__collen
    
    @property
    def rowlen(self) -> int:
        return self.__rowlen
    
    @property
    def sqmatx(self) -> bool:
        return self.__sqmatx
    
    # prints the value of matx object
    @matx.getter
    def pmatx(self) -> None:
        print("matx(")
        for k in [[str(j) for j in i] for i in self.__matx]:
            print('|', str(k)[1:-1], '|')
        print(')\n')
    
    def dnant(self) -> Decimal:
        if self.__dnant is None and self.__sqmatx is True:
            self.__dnant = matutils.dnant(matx(self.__matx, False, 'c'), False, 'w')
            return self.__dnant
        else:
            return self.__dnant

    def invsednant(self) -> Decimal:
        if self.__invsednant is None and self.__sqmatx is True:
            self.__invsednant = matutils.invsednant(matx(self.__matx, False, 'c'), False, 'w')
            return self.__invsednant
        else:
            return self.__invsednant
    
    def invse(self) -> matx:
        if self.__invse is None and self.sqmatx is True and self.dnant() != 0:
            self.__invse = matutils.invse(matx(self.__matx, False, 'c'), False, 'w')
            return self.__invse
        else:
            return self.__invse
    
    def adjnt(self) -> matx:
        if self.__adjnt is None and self.__sqmatx is True:
            self.__adjnt = matutils.adjnt(matx(self.__matx, False, 'c'), False, 'w')
            return self.__adjnt
        else:
            return self.__adjnt

    def tpose(self) -> matx:
        if self.__tpose is None:
            self.__tpose = matutils.tpose(matx(self.__matx, False, 'c'), False, 'w')
            return self.__tpose
        else:
            return self.__tpose
    
    def cofacm(self) -> matx:
        if self.__cofacm is None:
            self.__cofacm = matutils.tpose(self.adjnt(), False, 'w')
            return self.__cofacm
        else:
            return self.__cofacm

    # returns matx as a list
    def matxl(self) -> list:
        return [list(i) for i in self.__matx]
    
    def pop(self, i: int, r=True, chk=True, ret='a') -> tuple[Decimal, ...]:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if (i := tint.ele(i, self.__collen)) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            match r:
                case True:
                    m = list(self.__matx)
                    p = m.pop(i)
                    self.__matx, self.__collen = tuple(m), self.__collen - 1
                case False:
                    m = self.matxl()
                    p = list()
                    for j in range(self.__collen):
                        p.append(m[j].pop(i))
                        m[j] = tuple(m[j])
                    self.__matx, self.__rowlen = tuple(m), self.__rowlen - 1
                case _:
                    raise Exception("Invalid argument: r => bool")
            del m
            if self.__collen == self.__rowlen:
                self.__sqmatx = True
            else:
                self.__sqmatx = False
            return tuple(p)
        except Exception as e:
            retrn(ret, e)

    # return element at i,j of matrix
    def mele(self, i: int, j: int, chk=True, ret='a') -> Decimal:
        try:
            match chk:
                case False:
                    return self.__matx[i][j]
                case True:
                    if (i := tint.ele(i, self.__collen)) is None or (j := tint.ele(j, self.__rowlen)) is None:
                        raise Exception
                    return self.__matx[i][j]
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # return tuple of i'th row
    def mrow(self, i: int, chk=True, ret='a') -> tuple[Decimal, ...]:
        try:
            match chk:
                case False:
                    return self.__matx[i]
                case True:
                    if (i := tint.ele(i, self.__collen)) is None:
                        raise Exception
                    return self.__matx[i]
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # returns tuple of i'th column
    def mcol(self, j: int, chk=True, ret='a') -> tuple[Decimal, ...]:
        try:
            match chk:
                case False:
                    return tuple([self.__matx[i][j] for i in range(self.__collen)])
                case True:
                    if (j := tint.ele(j, self.__rowlen)) is None:
                        raise Exception
                    return tuple([self.__matx[i][j] for i in range(self.__collen)])
                case _:
                    raise Exception
        except Exception as e:
            retrn(ret, e)


class matutils:

    # returns scalar matrix of size nxn
    @staticmethod
    def sclrm(n: int, el: Decimal, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if (n := tint.intn(n)) is None or (el := deciml(el)) == Decimal('NaN'):
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
                        l1.append(deciml('0.0'))
                m.append(tuple(l1))
            return matx(tuple(m), False, 'c')
        except Exception as e:
            retrn(ret, e)

    # returns matrix of size mxn with equal elements
    @staticmethod
    def eqelm(m: int, n: int, i: Decimal, chk=True, ret='a') -> matx:
        try:
            match chk:
                case True:
                    return matx(tuple([tuple([i for _ in range(n)]) for _ in range(m)]), False, 'c')
                case False:
                    if (n := tint.intn(n)) is None or (m := tint.intn(m)) is None or (i := deciml(i)) == Decimal('NaN'):
                        raise Exception
                    return matx(tuple([tuple([i for _ in range(n)]) for _ in range(m)]), False, 'c')
        except Exception as e:
            retrn(ret, e)

    @staticmethod
    def addmatx(a: matx, b: matx, r=False, chk=True, ret='a') -> matx:
        try:
            match chk:
                case True:
                    if tmatx([a, b], True) is None:
                        raise Exception
                    match r:
                        case False:
                            if eqval(b.collen, a.collen) is None:
                                raise Exception
                        case True:
                            if eqval(b.rowlen, a.rowlen) is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: r => bool")
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: chk => bool")
            match r:
                case False:
                    r = list()
                    for i in range(a.collen):
                        r.append(a.mrow(i, False, 'c') + b.mrow(i, False, 'c'))
                    return matx(tuple(r), False, 'c')
                case True:
                    return matx(a.matx + b.matx, False, 'c')
                case _:
                    raise Exception("Invalid argument: r => bool")
        except Exception as e:
            retrn(ret, e)

    @classmethod
    def maddval(cls, a: matx, x: Decimal, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    return cls.addmatx(cls.eqelm(a.collen, 1, x, False, 'c'), a, False, False, 'c')
                case True:
                    if tmatx(a) is None:
                        raise Exception
                    if (x := deciml(x)) == Decimal('NaN'):
                        raise Exception
                    return cls.addmatx(cls.eqelm(a.collen, 1, x, False, 'c'), a, False, False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # convert list x to x
    @staticmethod
    def matlxtox(a: matx, chk=True, ret='a') -> tuple:
        try:
            match chk:
                case False:
                    return tuple([matx(i, False, 'c') for i in a.matx])
                case True:
                    if tmatx(a) is None:
                        raise Exception
                    return tuple([matx(i, False, 'c') for i in a.matx])
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    @staticmethod
    def matxtolx(a: tuple[matx, ...] | list, chk=True, ret='a') -> matx:
        try:
            x = list()
            match chk:
                case False:
                    return matx(tuple([i.matx[0] for i in a]), False, 'c')
                case True:
                    if tmatx(a, True) is None:
                        raise Exception
                    ar = a[0].rowlen
                    for i in a:
                        if eqval(i.collen, 1) is None or eqval(i.rowlen, ar) is None:
                            raise Exception
                        x.append(i.matx[0])
                    return matx(tuple(x), False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # returns row or column elements of the matrix
    @staticmethod
    def gele(a: matx, b: list, r=False, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if tmatx(a) is None or b is None:
                        raise Exception
                    match r:
                        case True:
                            b = tint.ele(b, a.collen)
                        case False:
                            b = tint.ele(b, a.rowlen)
                        case _:
                            raise Exception("Invalid argument: r => bool")
                case _:
                    raise Exception("Invalid argument: chk => bool")
            match r:
                case True:
                    m = tuple([a.mrow(i, False, 'c') for i in b])
                case False:
                    m = tuple([a.mcol(i, False, 'c') for i in b])
                case _:
                    raise Exception("Invalid argument: r => bool")
            return matx(m, False, 'c')
        except Exception as e:
            retrn(ret, e)

    # returns the transpose of the matrix
    @classmethod
    def tpose(cls, a: matx, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    return cls.gele(a, [i for i in range(a.rowlen)], False, False, 'c')
                case True:
                    if tmatx(a) is None:
                        raise Exception
                    return cls.gele(a, [i for i in range(a.rowlen)], False, False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # returns the co-factor of the matrix element
    @classmethod
    def cofac(cls, a: matx, b: int, c: int, chk=True, ret='a') -> Decimal:
        try:
            match chk:
                case True:
                    if tmatx(a) is None:
                        raise Exception
                    if a.sqmatx is False:
                        raise Exception("Error: Not a square matrix")
                    if (b, c := tint.ele([b, c], a.rowlen)) is None:
                        raise Exception
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: chk => bool")
            a = matx(a, False, 'c')
            a.pop(c, False, False, 'c')
            a.pop(b, chk=False, ret='c')
            if (p := alg.div((b + c), 2)) == int(p):
                return cls.dnant(a, False, 'c')
            else:
                return alg.mul(-1, cls.dnant(a, False, 'c'))
        except Exception as e:
            retrn(ret, e)

    # returns the determinant of the matrix
    @classmethod
    def dnant(cls, a: matx, chk=True, ret='a') -> Decimal:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if tmatx(a) is None:
                        raise Exception
                    if a.sqmatx is False:
                        raise Exception("Error: Not a square matrix")
                case _:
                    raise Exception("Invalid argument: chk => bool")
            a = matx(a, False, 'c')
            if (lr := a.rowlen) == 1:
                return a.mele(0, 0, False, 'c')
            else:
                ep = None
                ele = a.mele(0, 0, False, 'c')
                li = a.mrow(0, False, 'c')
                if ele == 0:
                    for i in range(lr):
                        if i > 0:
                            if li[i] != 0:
                                e = li[i]
                                ep = i
                    if ep is None:
                        return deciml('0')
                else:
                    ep = 0
                    e = ele
                for i in range(lr):
                    if i != ep:
                        ele = li[i]
                        fac = alg.div(alg.mul(-1, ele), e)
                        a.matx = cls.tform(a, i, ep, fac, False, False, 'c')
                return alg.mul(e, cls.cofac(a, 0, ep, False, 'c'))
        except Exception as e:
            retrn(ret, e)

    # returns adjoint matrix of the matrix
    @classmethod
    def adjnt(cls, a: matx, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    return matx(tuple([tuple([cls.cofac(a, j, i, False, 'c') for j in range(a.collen)]) for i in range(a.rowlen)]), False, 'c')
                case True:
                    if tmatx(a) is None:
                        raise Exception
                    if a.sqmatx is False:
                        raise Exception("Error: Not a square matrix")
                    return matx(tuple([tuple([cls.cofac(a, j, i, False, 'c') for j in range(a.collen)]) for i in range(a.rowlen)]), False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # returns inverse matrix of the matrix
    @classmethod
    def invse(cls, a: matx, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if tmatx(a) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            if (det := cls.dnant(a, False, 'c')) is None:
                raise Exception
            if det == 0:
                raise Exception("Error: Determinant is 0,\nInverse DNE!")
            return cls.smult(alg.div(1, det), cls.adjnt(a, False, 'c'), False, 'c')
        except Exception as e:
            retrn(ret, e)

    # returns inverse matrix of the matrix using matrix transformation
    @classmethod
    def invsednant(cls, a: matx, chk=True, ret='a') -> Decimal:
        try:
            match chk:
                case True:
                    if tmatx(a) is None:
                        raise Exception
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: chk => bool")
            a = matx(a, False, 'c')
            det = cls.dnant(a, False, 'c')
            if det is None:
                raise Exception
            if det == 0:
                raise Exception("Error: Determinant is 0,\nInverse DNE!")
            elif det > 0:
                a.matx = cls.smult(alg.pwr(det, alg.div(-1, a.collen)), a, False, 'c')
            else:
                a.matx = cls.smult(alg.mul(-1, alg.pwr(alg.mul(-1, det), alg.div(-1, a.collen))), a, False, 'c')
            b = cls.sclrm(a.rowlen, deciml('1.0'), False, 'c')
            for i in range(a.collen):
                ele = a.mele(i, i, False, 'c')
                if ele != 1:
                    for j in range(a.rowlen):
                        if j > i:
                            el = a.mele(i, j, False, 'c')
                            if el != 0:
                                a.matx = cls.tform(a, i, j, alg.div(alg.sub(1, ele), el), False, False, 'c')
                                b.matx = cls.tform(b, i, j, alg.div(alg.sub(1, ele), el), False, False, 'c')
                                break
                            else:
                                if j == a.rowlen - 1:
                                    if ele != 0:
                                        a.matx = cls.tform(a, i + 1, i, deciml('1'), False, False, 'c')
                                        a.matx = cls.tform(a, i, i + 1, alg.sub(alg.div(1, ele), 1), False, False, 'c')
                                        b.matx = cls.tform(b, i + 1, i, deciml('1'), False, False, 'c')
                                        b.matx = cls.tform(b, i, i + 1, alg.sub(alg.div(1, ele), 1), False, False, 'c')
                                    else:
                                        raise Exception("Error: Invalid Matrix Inverse")
                ele = a.mele(i, i, False, 'c')
                row = a.mrow(i, False, 'c')
                col = a.mcol(i, False, 'c')
                for j in range(a.rowlen):
                    if j > i:
                        el = row[j]
                        e = col[j]
                        a.matx = cls.tform(a, j, i, alg.div(alg.mul(-1, el), ele), False, False, 'c')
                        b.matx = cls.tform(b, j, i, alg.div(alg.mul(-1, el), ele), False, False, 'c')
                        a.matx = cls.tform(a, j, i, alg.div(alg.mul(-1, e), ele), True, False, 'c')
                        b.matx = cls.tform(b, j, i, alg.div(alg.mul(-1, e), ele), True, False, 'c')
                        del e
                        del el
                del ele
            if det > 0:
                b.matx = cls.smult(alg.pwr(det, alg.div(-1, a.collen)), b, False, 'c')
            if det < 0:
                b.matx = cls.smult(alg.mul(-1, alg.pwr(alg.mul(-1, det), alg.div(-1, a.collen))), b, False, 'c')
            return cls.dnant(b, False, 'c')
        except Exception as e:
            retrn(ret, e)

    # returns matrix after row or column tranformation
    @classmethod
    def tform(cls, a: matx, b: int, c: int, d: Decimal, r=False, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if tmatx(a) is None or (d := deciml(d)) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            if (m := cls.gele(a, [b, c], r, chk, 'c')) is None:
                raise Exception
            m = m.matx
            match r:
                case True:
                    a = list(a.matx)
                    a[b] = alg.ladd(m[0], [alg.mul(d, j) for j in m[1]])
                    return matx(tuple(a), False, 'c')
                case False:
                    a = list(a.matx)
                    for i in enumerate(alg.ladd(m[0], [alg.mul(d, j) for j in m[1]])):
                        a1 = list(a[i[0]])
                        a1[b] = i[1]
                        a[i[0]] = tuple(a1)
                    return matx(tuple(a), False, 'c')
                case _:
                    raise Exception
        except Exception as e:
            retrn(ret, e)

    # returns sum of two matrices
    @staticmethod
    def madd(a: matx, b: matx, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    alc = a.collen
                case True:
                    if tmatx([a, b], True) is None:
                        raise Exception
                    if eqval([(alc := a.collen), a.rowlen], [b.collen, b.rowlen]) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            a, b, r = b.matx, a.matx, list()
            for i in range(alc):
                r.append(alg.ladd(a[i], b[i]))
            return matx(tuple(r), False, 'c')
        except Exception as e:
            retrn(ret, e)
    
    @classmethod
    def saddcnst(cls, a: tuple | list | Decimal, b: matx, r=False, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if r is not None:
                        if (a := tdeciml.dall(a)) is None:
                            raise Exception
                    else:
                        if (a := deciml(a)) == Decimal('NaN'):
                            raise Exception
                    if tmatx(b) is None:
                        raise Exception
                    match r:
                        case True:
                            if eqval(len(a), b.collen) is None:
                                raise Exception
                        case False:
                            if eqval(len(a), b.rowlen) is None:
                                raise Exception
                        case None:
                            pass
                        case _:
                            raise Exception("Invalid argument: r => bool/None")
                case _:
                    raise Exception("Invalid argument: chk => bool")
            match r:
                case True:
                    return matx(tuple([alg.ladd(a, b.mcol(i, False, 'c')) for i in range(b.rowlen)]), False, 'c')
                case False:
                    return matx(tuple([alg.ladd(a, b.mrow(i, False, 'c')) for i in range(b.collen)]), False, 'c')
                case None:
                    return matx(tuple([tuple([alg.add(a, j) for j in i]) for i in b.matx]), False, 'c')
                case _:
                    raise Exception("Invalid argument: r => bool/None")
        except Exception as e:
            retrn(ret, e)

    # returns difference of two matrices
    @staticmethod
    def msub(a: matx, b: matx, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    alc = a.collen
                case True:
                    if tmatx([a, b], True) is None:
                        raise Exception
                    if eqval([(alc := a.collen), a.rowlen], [b.collen, b.rowlen]) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            a, b, r = a.matx, b.matx, list()
            for i in range(alc):
                r.append(alg.lsub(a[i], b[i]))
            return matx(tuple(r), False, 'c')
        except Exception as e:
            retrn(ret, e)

    # returns matrix after scalar multiplication
    @staticmethod
    def smult(a: Decimal, b: matx, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if (a := deciml(a)) == Decimal('NaN'):
                        raise Exception
                    if tmatx(b) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            r = list()
            for i in b.matx:
                r1 = list()
                for j in i:
                    r1.append(alg.mul(j, a))
                r.append(tuple(r1))
            return matx(tuple(r), False, 'c')
        except Exception as e:
            retrn(ret, e)

    @classmethod
    def smultfac(cls, a: tuple | list, b: matx, r=True, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    match a.__class__.__name__:
                        case 'tuple':
                            if (a := tdeciml.dall(a)) is None:
                                raise Exception
                        case 'list':
                            if (a := tdeciml.dall(a)) is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: a => tuple/list")
                    if tmatx(b) is None:
                        raise Exception
                    match r:
                        case True:
                            if eqval(len(a), b.collen) is None:
                                raise Exception
                        case False:
                            if eqval(len(a), b.rowlen) is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: r => bool")
                case _:
                    raise Exception("Invalid argument: chk => bool")
            if r is True:
                r = list()
                for i in range(b.rowlen):
                    r.append(alg.lmul(a, b.mcol(i, False, 'c')))
                return matutils.tpose(matx(tuple(r), False, 'c'), False, 'c')
            else:
                r = list()
                for i in range(b.collen):
                    r.append(alg.lmul(a, b.mrow(i, False, 'c')))
                return matx(tuple(r), False, 'c')
        except Exception as e:
            retrn(ret, e)

    # returns matrix after matrix multiplication
    @classmethod
    def mmult(cls, a: matx, b: matx, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if tmatx([a, b], True) is None:
                        raise Exception
                    if eqval(a.rowlen, b.collen) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            r = list()
            a = a.matx
            b = cls.tpose(b).matx
            for i in a:
                r1 = list()
                for j in b:
                    r1.append(alg.addl(alg.lmul(i, j)))
                r.append(tuple(r1))
            return matx(tuple(r), False, 'c')
        except Exception as e:
            retrn(ret, e)

    @staticmethod
    def uldcompose(a: matx, chk=True, ret='a') -> tuple:
        try:
            match chk:
                case True:
                    if tmatx(a) is None:
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
                        lt1.append(a.mele(i, j, False, 'c'))
                        ut1.append(deciml('0.0'))
                    elif i == j:
                        dia.append(a.mele(i, j, False, 'c'))
                        lt1.append(deciml('0.0'))
                        ut1.append(deciml('0.0'))
                    else:
                        ut1.append(a.mele(i, j, False, 'c'))
                        lt1.append(deciml('0.0'))
                ut.append(tuple(ut1))
                lt.append(tuple(lt1))
            return matx(tuple(ut), False, 'c'), matx(tuple(lt), False, 'c'), matx((tuple(dia), ), False, 'c')
        except Exception as e:
            retrn(ret, e)
    
    @classmethod
    def dpose(cls, a: matx, li: list | tuple, r=False, chk=True, ret='a') -> tuple:
        try:
            match chk:
                case True:
                    if tmatx(a) is None:
                        raise Exception
                    match li.__class__.__name__:
                        case 'list':
                            if (li := tint.iwgrp(li)) is None:
                                raise Exception
                    match r:
                        case False:
                            if eqval(sum(li), a.rowlen) is None:
                                raise Exception
                        case True:
                            if eqval(sum(li), a.collen) is None:
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
                return tuple([cls.tpose(cls.gele(a, i, False, False, 'c'), False, 'c') for i in ln])
            else:
                return tuple([cls.gele(a, i, True, False, 'c') for i in ln])
        except Exception as e:
            retrn(ret, e)


class melutils:

    @staticmethod
    def add(a: matx, li: list[list] | tuple[list] | str, r=False, chk=True, ret='a') -> matx:
        try:
            if li != 'all':
                l = list()
                for i in li:
                    for j in i:
                        if j not in l:
                            l.append(j)
                d = dict()
                for i in enumerate(matutils.gele(a, l, r, chk, 'c').matx):
                    d[l[i[0]]] = i[1]
                li = [matx(tuple([d[j] for j in i]), False, 'c') for i in li]
                return matx(tuple([tuple([alg.addl(i.mcol(j, False, 'c')) for j in range(i.rowlen)]) for i in li]), False, 'c')
            else:
                match r:
                    case False:
                        return matx(tuple([alg.addl(i) for i in a.matx]), False, 'c')
                    case True:
                        return matx(tuple([alg.addl(a.mcol(i, False, 'c')) for i in range(a.rowlen)]), False, 'c')
                    case _:
                        raise Exception("Invalid argument: r => bool")
        except Exception as e:
            retrn(ret, e)
    
    @staticmethod
    def mult(a: matx, li: list[list] | tuple[list] | str, r=False, chk=True, ret='a') -> matx:
        try:
            if li != 'all':
                l = list()
                for i in li:
                    for j in i:
                        if j not in l:
                            l.append(j)
                d = dict()
                for i in enumerate(matutils.gele(a, l, r, chk, 'c').matx):
                    d[l[i[0]]] = i[1]
                li = [matx(tuple([d[j] for j in i]), False, 'c') for i in li]
                return matx(tuple([tuple([alg.mull(i.mcol(j, False, 'c')) for j in range(i.rowlen)]) for i in li]), False, 'c')
            else:
                match r:
                    case False:
                        return matx(tuple([alg.mull(i) for i in a.matx]), False, 'c')
                    case True:
                        return matx(tuple([alg.mull(a.mcol(i, False, 'c')) for i in range(a.rowlen)]), False, 'c')
                    case _:
                        raise Exception("Invalid argument: r => bool")
        except Exception as e:
            retrn(ret, e)

    @staticmethod
    def pow(an: list | tuple[Decimal, Decimal], a: matx, li: list[list] | tuple[list] | str, r=False, chk=True, ret='a') -> matx:
        try:
            match chk:
                case False:
                    pass
                case True:
                    match an.__class__.__name__:
                        case 'tuple':
                            if (an := tdeciml.dall(an)) is None:
                                raise Exception
                        case 'list':
                            if (an := tdeciml.dall(an)) is None:
                                raise Exception
                        case _:
                            raise Exception("Invalid argument: a => tuple/list")
                    if eqval(len(an), 2) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: chk => bool")
            if li != 'all':
                if an[0] != 1:
                    return matx(tuple([tuple([alg.pwr(alg.mul(an[0], j), an[1]) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                else:
                    return matx(tuple([tuple([alg.pwr(j, an[1]) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
            else:
                if an[0] != 1:
                    return matx(tuple([tuple([alg.pwr(alg.mul(an[0], j), an[1]) for j in i]) for i in a.matx]), False, 'c')
                else:
                    return matx(tuple([tuple([alg.pwr(j, an[1]) for j in i]) for i in a.matx]), False, 'c')
        except Exception as e:
            retrn(ret, e)

    @staticmethod
    def log(an: list | tuple[Decimal, Decimal], a: matx, li: list[list] | tuple[list] | str, r=False, chk=True, ret='a') -> matx:
        match chk:
            case False:
                pass
            case True:
                match an.__class__.__name__:
                    case 'tuple':
                        if (an := tdeciml.dall(an)) is None:
                            raise Exception
                    case 'list':
                        if (an := tdeciml.dall(an)) is None:
                            raise Exception
                    case _:
                        raise Exception("Invalid argument: a => tuple/list")
                if eqval(len(an), 2) is None:
                    raise Exception
            case _:
                raise Exception("Invalid argument: chk => bool")
        if li != 'all':
            if an[0] != 1:
                return matx(tuple([tuple([alg.log(alg.mul(j, an[0]), an[1]) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
            else:
                return matx(tuple([tuple([alg.log(j, an[1]) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
        else:
            if an[0] != 1:
                return matx(tuple([tuple([alg.log(alg.mul(j, an[0]), an[1]) for j in i]) for i in a.matx]), False, 'c')
            else:
                return matx(tuple([tuple([alg.log(j, an[1]) for j in i]) for i in a.matx]), False, 'c')

    @staticmethod
    def expo(an: list | tuple[Decimal, Decimal], a: matx, li: list[list] | tuple[list] | str, r=False, chk=True, ret='a') -> matx:
        match chk:
            case False:
                pass
            case True:
                match an.__class__.__name__:
                    case 'tuple':
                        if (an := tdeciml.dall(an)) is None:
                            raise Exception
                    case 'list':
                        if (an := tdeciml.dall(an)) is None:
                            raise Exception
                    case _:
                        raise Exception("Invalid argument: a => tuple/list")
                if eqval(len(an), 2) is None:
                    raise Exception
            case _:
                raise Exception("Invalid argument: chk => bool")
        if li!= 'all':
            if an[1] != 1:
                return matx(tuple([tuple([alg.pwr(an[0], alg.mul(j, an[1])) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
            else:
                return matx(tuple([tuple([alg.pwr(an[0], j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
        else:
            if an[1] != 1:
                return matx(tuple([tuple([alg.pwr(an[0], alg.mul(j, an[1])) for j in i]) for i in a.matx]), False, 'c')
            else:
                return matx(tuple([tuple([alg.pwr(an[0], j) for j in i]) for i in a.matx]), False, 'c')

    @staticmethod
    def trig(n: Decimal, a: matx, li: list[list] | tuple[list] | str, r=False, f='cos', chk=True, ret='a') -> matx:
        match chk:
            case False:
                pass
            case True:
                if (n := deciml(n)) == Decimal('NaN'):
                    raise Exception
            case _:
                raise Exception("Invalid argument: chk => bool")
        if li != 'all':
            if n != 1:
                match f:
                    case 'cos':
                        return matx(tuple([tuple([trig.cos(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'sin':
                        return matx(tuple([tuple([trig.sin(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'tan':
                        return matx(tuple([tuple([trig.tan(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'sec':
                        return matx(tuple([tuple([trig.sec(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'cosec':
                        return matx(tuple([tuple([trig.cosec(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'cot':
                        return matx(tuple([tuple([trig.cot(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'acos':
                        return matx(tuple([tuple([trig.acos(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'asin':
                        return matx(tuple([tuple([trig.asin(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'atan':
                        return matx(tuple([tuple([trig.atan(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'asec':
                        return matx(tuple([tuple([trig.asec(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'acosec':
                        return matx(tuple([tuple([trig.acosec(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'acot':
                        return matx(tuple([tuple([trig.acot(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'sinh':
                        return matx(tuple([tuple([trig.sinh(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'cosh':
                        return matx(tuple([tuple([trig.cosh(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'tanh':
                        return matx(tuple([tuple([trig.tanh(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'cosech':
                        return matx(tuple([tuple([trig.cosech(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'sech':
                        return matx(tuple([tuple([trig.sech(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'coth':
                        return matx(tuple([tuple([trig.coth(alg.mul(n, j)) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
            else:
                match f:
                    case 'cos':
                        return matx(tuple([tuple([trig.cos(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'sin':
                        return matx(tuple([tuple([trig.sin(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'tan':
                        return matx(tuple([tuple([trig.tan(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'sec':
                        return matx(tuple([tuple([trig.sec(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'cosec':
                        return matx(tuple([tuple([trig.cosec(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'cot':
                        return matx(tuple([tuple([trig.cot(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'acos':
                        return matx(tuple([tuple([trig.acos(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'asin':
                        return matx(tuple([tuple([trig.asin(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'atan':
                        return matx(tuple([tuple([trig.atan(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'asec':
                        return matx(tuple([tuple([trig.asec(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'acosec':
                        return matx(tuple([tuple([trig.acosec(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'acot':
                        return matx(tuple([tuple([trig.acot(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'sinh':
                        return matx(tuple([tuple([trig.sinh(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'cosh':
                        return matx(tuple([tuple([trig.cosh(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'tanh':
                        return matx(tuple([tuple([trig.tanh(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'cosech':
                        return matx(tuple([tuple([trig.cosech(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'sech':
                        return matx(tuple([tuple([trig.sech(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
                    case 'coth':
                        return matx(tuple([tuple([trig.coth(j) for j in i]) for i in matutils.gele(a, li, r, chk, 'c').matx]), False, 'c')
        else:
            if n != 1:
                match f:
                    case 'cos':
                        return matx(tuple([tuple([trig.cos(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'sin':
                        return matx(tuple([tuple([trig.sin(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'tan':
                        return matx(tuple([tuple([trig.tan(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'sec':
                        return matx(tuple([tuple([trig.sec(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'cosec':
                        return matx(tuple([tuple([trig.cosec(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'cot':
                        return matx(tuple([tuple([trig.cot(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'acos':
                        return matx(tuple([tuple([trig.acos(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'asin':
                        return matx(tuple([tuple([trig.asin(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'atan':
                        return matx(tuple([tuple([trig.atan(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'asec':
                        return matx(tuple([tuple([trig.asec(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'acosec':
                        return matx(tuple([tuple([trig.acosec(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'acot':
                        return matx(tuple([tuple([trig.acot(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'sinh':
                        return matx(tuple([tuple([trig.sinh(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'cosh':
                        return matx(tuple([tuple([trig.cosh(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'tanh':
                        return matx(tuple([tuple([trig.tanh(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'cosech':
                        return matx(tuple([tuple([trig.cosech(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'sech':
                        return matx(tuple([tuple([trig.sech(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
                    case 'coth':
                        return matx(tuple([tuple([trig.coth(alg.mul(n, j)) for j in i]) for i in a.matx]), False, 'c')
            else:
                match f:
                    case 'cos':
                        return matx(tuple([tuple([trig.cos(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'sin':
                        return matx(tuple([tuple([trig.sin(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'tan':
                        return matx(tuple([tuple([trig.tan(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'sec':
                        return matx(tuple([tuple([trig.sec(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'cosec':
                        return matx(tuple([tuple([trig.cosec(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'cot':
                        return matx(tuple([tuple([trig.cot(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'acos':
                        return matx(tuple([tuple([trig.acos(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'asin':
                        return matx(tuple([tuple([trig.asin(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'atan':
                        return matx(tuple([tuple([trig.atan(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'asec':
                        return matx(tuple([tuple([trig.asec(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'acosec':
                        return matx(tuple([tuple([trig.acosec(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'acot':
                        return matx(tuple([tuple([trig.acot(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'sinh':
                        return matx(tuple([tuple([trig.sinh(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'cosh':
                        return matx(tuple([tuple([trig.cosh(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'tanh':
                        return matx(tuple([tuple([trig.tanh(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'cosech':
                        return matx(tuple([tuple([trig.cosech(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'sech':
                        return matx(tuple([tuple([trig.sech(j) for j in i]) for i in a.matx]), False, 'c')
                    case 'coth':
                        return matx(tuple([tuple([trig.coth(j) for j in i]) for i in a.matx]), False, 'c')


class matstat:
    
    @staticmethod
    def amean(a: matx, el='row', chk=True, ret='a') -> tuple[Decimal, ...] | Decimal:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if tmatx(a) is None: 
                        raise Exception
                case _:
                    raise Exception("Invalid argument: a => matx")
            match el:
                case 'row':
                    return matutils.smult(alg.div(1, a.rowlen), melutils.add(a, 'all', False, False, 'c')).matx[0]
                case 'col':
                    return matutils.smult(alg.div(1, a.collen), melutils.add(a, 'all', True, False, 'c')).matx[0]
                case 'all':
                    return alg.div(alg.addl(melutils.add(a, 'all', chk=False, ret='c').matx[0]), a.rowlen * a.collen)
                case _:
                    raise Exception("Invalid argument: el => 'row'/'col'/'all")
        except Exception as e:
            retrn(ret, e)
    
    @classmethod
    def gmean(cls, a: matx, el='row', chk=True, ret='a') -> tuple[Decimal, ...] | Decimal:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if tmatx(a) is None: 
                        raise Exception
                case _:
                    raise Exception("Invalid argument: a => matx")
            match el:
                case 'row':
                    return melutils.pow([Decimal('1.0'), alg.div(1, a.rowlen)], melutils.mult(a, 'all', False, False, 'c'), 'all', chk=False, ret='c').matx[0]
                case 'col':
                    return melutils.pow([Decimal('1.0'), alg.div(1, a.collen)], melutils.mult(a, 'all', True, False, 'c'), 'all', chk=False, ret='c').matx[0]
                case 'all':
                    return alg.pwr(melutils.mult(melutils.mult(a, 'all', True, False, 'c'), 'all', False, False, 'c').matx[0][0], alg.div(1, (a.rowlen * a.collen)))
                case _:
                    raise Exception("Invalid argument: el => 'row'/'col'/'all")
        except Exception as e:
            retrn(ret, e)

    @classmethod
    def hmean(cls, a: matx, el='row', chk=True, ret='a') -> tuple[Decimal, ...] | Decimal:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if tmatx(a) is None: 
                        raise Exception
                case _:
                    raise Exception("Invalid argument: a => matx")
            match el:
                case 'row':
                    return melutils.pow([alg.div(1, a.rowlen), Decimal('-1.0')], melutils.add(melutils.pow([Decimal('1'), Decimal('-1')], a, 'all', chk=False, ret='c'), 'all', False, False, 'c'), 'all', chk=False, ret='c').matx[0]
                case 'col':
                    return melutils.pow([alg.div(1, a.collen), Decimal('-1.0')], melutils.add(melutils.pow([Decimal('1'), Decimal('-1')], a, 'all', chk=False, ret='c'), 'all', True, False, 'c'), 'all', chk=False, ret='c').matx[0]
                case 'all':
                    return alg.div(a.rowlen * a.collen, melutils.add(melutils.add(melutils.pow([Decimal('1'), Decimal('-1')], a, 'all', chk=False, ret='c'), 'all', True, False, 'c'), 'all', False, False, 'c').matx[0][0])
                case _:
                    raise Exception("Invalid argument: el => 'row'/'col'/'all")
        except Exception as e:
            retrn(ret, e)

    @classmethod
    def qmean(cls, a: matx, el='row', chk=True, ret='a') -> tuple[Decimal, ...] | Decimal:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if tmatx(a) is None: 
                        raise Exception
                case _:
                    raise Exception("Invalid argument: a => matx")
            match el:
                case 'row':
                    return melutils.pow([alg.div(1, a.rowlen), Decimal('0.5')], melutils.add(melutils.pow([Decimal('1.0'), Decimal('2.0')], a, 'all', chk=False, ret='c'), 'all', False, False, 'c'), 'all', chk=False, ret='c').matx[0]
                case 'col':
                    return melutils.pow([alg.div(1, a.collen), Decimal('0.5')], melutils.add(melutils.pow([Decimal('1.0'), Decimal('2.0')], a, 'all', chk=False, ret='c'), 'all', True, False, 'c'), 'all', chk=False, ret='c').matx[0]
                case 'all':
                    return alg.pwr(alg.div(melutils.add(melutils.add(melutils.pow([Decimal('1.0'), Decimal('2.0')], a, 'all', chk=False, ret='c'), 'all', True, False, 'c'), 'all', False, False, 'c').matx[0][0], a.rowlen * a.collen), 0.5)
                case _:
                    raise Exception("Invalid argument: el => 'row'/'col'/'all")
        except Exception as e:
            retrn(ret, e)
    
    @classmethod
    def var(cls, a: matx, el='row', samp=True, chk=True, ret='a') -> tuple[Decimal, ...] | Decimal:
        try:
            match chk:
                case False:
                    pass
                case True:
                    if tmatx(a) is None: 
                        raise Exception
                case _:
                    raise Exception("Invalid argument: a => matx")
            match el:
                case 'row':
                    match samp:
                        case True:
                            lr = a.rowlen - 1
                        case False:
                            lr = a.rowlen
                        case _:
                            raise Exception("Invalid argument: samp => bool")
                    return matutils.smult(alg.div(1, lr), melutils.add(melutils.pow([Decimal('1.0'), Decimal('2.0')], matutils.saddcnst([alg.mul(-1, i) for i in cls.amean(a, 'row', False, 'c')], a, True, False, 'c'), 'all', chk=False, ret='c'), 'all', False, False, 'c'), False, 'c').matx[0]
                case 'col':
                    a = matutils.saddcnst([alg.mul(-1, i) for i in cls.amean(a, 'col', False, 'c')], a, False,  False, 'c')
                    match samp:
                        case True:
                            lc = a.collen - 1
                        case False:
                            lc = a.collen
                        case _:
                            raise Exception("Invalid argument: samp => bool")
                    return matutils.smult(alg.div(1, lc), melutils.add(melutils.pow([Decimal('1.0'), Decimal('2.0')], matutils.saddcnst([alg.mul(-1, i) for i in cls.amean(a, 'col', False, 'c')], a, False, False, 'c'), 'all', chk=False, ret='c'), 'all', True, False, 'c'), False, 'c').matx[0]
                case 'all':
                    match samp:
                        case True:
                            l = (a.rowlen * a.collen) - 1
                        case False:
                            l = a.rowlen * a.collen
                        case _:
                            raise Exception("Invalid argument: samp => bool")
                    return alg.div(melutils.add(melutils.add(melutils.pow([Decimal('1.0'), Decimal('2.0')], matutils.saddcnst(alg.mul(-1, cls.amean(a, 'all', False, 'c')), a, None, False, 'c'), 'all', chk=False, ret='c'), 'all', False, False, 'c'), 'all', False, False, 'c').matx[0][0], l)
                case _:
                    raise Exception("Invalid argument: el => 'row'/'col'/'all")
        except Exception as e:
            retrn(ret, e)
    
    @classmethod
    def sd(cls, a: matx, el='row', samp=True, chk=True, ret='a') -> tuple[Decimal, ...] | Decimal:
        try:
            if el != 'all':
                return tuple([alg.pwr(i, 0.5) for i in cls.var(a, el, samp, chk, 'c')])
            else:
                return alg.pwr(cls.var(a, el, samp, chk, 'c'), 0.5)
        except Exception as e:
            retrn(ret, e)
