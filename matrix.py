from decimal import Decimal
from cmdexec import Terminate


class Comp:
    # return True if matx
    @staticmethod
    def tmatx(a) -> bool:
        try:
            if type(a) is list or type(a) is tuple:
                for i in a:
                    if i.__class__.__name__ != 'matx':
                        raise Exception(str(type(i)) + " is not matx")
                return True
            if a.__class__.__name__ != 'matx':
                raise Exception(str(type(a)) + " is not matx")
            else:
                return True
        except Exception as e:
            Terminate.retrn(True, e)

    # return True if bool
    @staticmethod
    def tbool(a: bool | list[bool] | tuple[bool]) -> bool:
        try:
            if type(a) is list or type(a) is tuple:
                for i in a:
                    if type(i) is not bool:
                        raise Exception(str(type(i)) + " is not bool")
                return True
            if type(a) is not bool:
                raise Exception(str(type(a)) + " is not bool")
            else:
                return True
        except Exception as e:
            Terminate.retrn(True, e)

    # return True if tuple
    @staticmethod
    def ttup(a: tuple | tuple[tuple]) -> bool:
        try:
            if type(a) is tuple:
                if type(a[0]) is tuple:
                    for i in a:
                        if type(i) is not tuple:
                            raise Exception(str(type(i)) + " is not tuple")
                    return True
                else:
                    return True
            else:
                raise Exception(str(type(a)) + " is not tuple")
        except Exception as e:
            Terminate.retrn(True, e)

    # return list if list
    @staticmethod
    def tlist(a: list | list[list]) -> bool:
        try:
            if type(a) is list:
                if type(a[0]) is list:
                    for i in a:
                        if type(i) is not list:
                            raise Exception(str(type(i)) + " is not list")
                    return True
                else:
                    return True
            else:
                raise Exception(str(type(a)) + " is not list")
        except Exception as e:
            Terminate.retrn(True, e)

    # return True if lengths of lists are equal
    @classmethod
    def lenlist(cls, a: list[list]) -> bool:
        try:
            if cls.tlist(a) is None:
                raise Exception
            l1 = a[0]
            for i in range(len(a)):
                if i > 0:
                    if len(l1) != len(a[i]):
                        raise Exception(str(len(l1)) + " != " + str(len(a[i])))
            else:
                return True
        except Exception as e:
            Terminate.retrn(True, e)

    # return True if lengths of tuple are equal
    @classmethod
    def lentup(cls, a: tuple[tuple]) -> bool:
        try:
            if cls.ttup(a) is None:
                raise Exception
            l1 = a[0]
            for i in range(len(a)):
                if i > 0:
                    if len(l1) != len(a[i]):
                        raise Exception(str(len(l1)) + " != " + str(len(a[i])))
            else:
                return True
        except Exception as e:
            Terminate.retrn(True, e)

    # return true if i is valid element index
    @classmethod
    def intele(cls, i: int | float | list, ln: int | float) -> list:
        try:
            ln = cls.tintn(ln)
            if ln is None:
                raise Exception
            if type(i) is int:
                i = [i, ]
            i = cls.iwlist(i)
            if i is None:
                raise Exception
            for j in i:
                if j > ln - 1:
                    raise Exception(str(j) + " is more than " + str(ln - 1))
            return i
        except Exception as e:
            Terminate.retrn(True, e)

    # check and return whole numbers
    @classmethod
    def tintw(cls, i: int | float) -> int:
        try:
            i = cls.tint(i)
            if i is None:
                raise Exception
            else:
                if i < 0:
                    raise Exception(str(i) + " is less than 0")
                else:
                    return i
        except Exception as e:
            Terminate.retrn(True, e)

    # check and return natural numbers
    @classmethod
    def tintn(cls, i: int | float) -> int:
        try:
            i = cls.tint(i)
            if i is None:
                raise Exception
            else:
                if i > 0:
                    return i
                else:
                    raise Exception(str(i) + " is less than 0")
        except Exception as e:
            Terminate.retrn(True, e)

    # check and return int
    @staticmethod
    def tint(i: int | float) -> int:
        try:
            if type(i) is not int:
                if type(i) is not float:
                    raise Exception(str(type(i)) + " is not int")
                else:
                    if i == int(i):
                        return int(i)
                    else:
                        raise Exception(str(type(i)) + " is not int")
            else:
                return i
        except Exception as e:
            Terminate.retrn(True, e)

    # check and return float
    @staticmethod
    def tdeciml(a: float | int | Decimal) -> Decimal:
        try:
            return Decimal(str(a))
        except Exception as e:
            Terminate.retrn(True, e)

    # check and return list with float elements
    @classmethod
    def dlist(cls, li: list, d=True) -> list:
        try:
            if cls.tlist(li) is not None:
                ln = list()
                if type(li[0]) is list:
                    for i in li:
                        ln1 = list()
                        if type(i) is not list:
                            raise Exception(str(type(i))+" is not list")
                        for j in i:
                            a = cls.tdeciml(j)
                            if a is None:
                                raise Exception(str(j) + " is not float")
                            else:
                                ln1.append(a)
                        ln.append(ln1)
                    return ln
                else:
                    for i in li:
                        a = cls.tdeciml(i)
                        if a is None:
                            raise Exception(str(i[0]) + " is not float")
                        else:
                            ln.append(a)
                    return ln
            else:
                raise Exception
        except Exception as e:
            Terminate.retrn(True, e)

    # check and return tuple with float elements
    @classmethod
    def dtup(cls, li: tuple) -> tuple:
        try:
            if cls.ttup(li) is not None:
                ln = list()
                if type(li[0]) is tuple:
                    for i in li:
                        ln1 = list()
                        for j in i:
                            a = cls.tdeciml(j)
                            if a is None:
                                raise Exception(str(j) + " is not float")
                            else:
                                ln1.append(a)
                        ln.append(tuple(ln1))
                    return tuple(ln)
                else:
                    for i in li:
                        a = cls.tdeciml(i)
                        if a is None:
                            raise Exception(str(i) + " is not float")
                        else:
                            ln.append(a)
                    return tuple(ln)
            else:
                raise Exception
        except Exception as e:
            Terminate.retrn(True, e)

    # check and return list with int elements
    @classmethod
    def iwlist(cls, li: list) -> list:
        try:
            if cls.tlist(li) is not None:
                ln = list()
                for i in li:
                    a = cls.tintw(i)
                    if a is None:
                        raise Exception(str(i) + " is not a whole number")
                    else:
                        ln.append(a)
                return ln
            else:
                raise Exception
        except Exception as e:
            Terminate.retrn(True, e)


def pwr(a: Decimal | int, b: Decimal | int) -> Decimal:
    try:
        return Decimal(str(pow(a, b)))
    except:
        if a == 0 and b == 0:
            return Decimal('1')
        else:
            return Decimal('NaN')


class Matx:
    @staticmethod
    def matrix(li: list | tuple, chk=True) -> tuple[tuple]:
        try:
            tli = li.__class__.__name__
            match chk:
                case True:
                    match tli:
                        case 'list':
                            li = Comp.dlist(li)
                            if li is None:
                                raise Exception
                            if type(li[0]) is list:
                                if Comp.lenlist(li) is None:
                                    raise Exception
                                return tuple([tuple(i) for i in li])
                            else:
                                return tuple(li),
                        case 'tuple':
                            li = Comp.dtup(li)
                            if li is None:
                                raise Exception
                            if type(li[0]) is tuple:
                                if Comp.lentup(li) is None:
                                    raise Exception
                                return li
                            else:
                                return li,
                        case 'matx':
                            return li.matx
                        case _:
                            raise Exception
                case False:
                    match tli:
                        case 'tuple':
                            if type(li[0]) is float:
                                return tuple(Decimal(str(i)) for i in li)
                            if type(li[0]) is Decimal:
                                return li,
                            if type(li[0]) is tuple:
                                return li
                            else:
                                raise Exception
                        case 'matx':
                            return li.matx
                        case _:
                            raise Exception
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(True, e)


class matx:
    def __init__(self, li: list | tuple, chk=True, ret=False) -> None:
        matrix = Matx.matrix(li, chk)
        if matrix is None:
            Terminate.retrn(ret, "Invalid matrix!\n")
        if matrix is not None:
            self._matx = matrix
            self.collen = len(matrix)
            self.rowlen = len(matrix[0])
            del matrix
            if self.rowlen == self.collen:
                self.sqmatx = True
            else:
                self.sqmatx = False

    @property
    def matx(self) -> tuple:
        return self._matx

    @matx.setter
    def matx(self, li: list | tuple) -> None:
        matrix = Matx.matrix(li)
        if matrix is None:
            if li.__class__.__name__ == 'matx':
                matrix = li.matx
            else: 
                Terminate.retrn(False, "Invalid matrix!\n")
        self._matx = matrix
        self.collen = len(matrix)
        self.rowlen = len(matrix[0])
        del matrix
        if self.rowlen == self.collen:
            self.sqmatx = True
        else:
            self.sqmatx = False
    
    # prints the value of matx object
    @matx.getter
    def pmatx(self) -> None:
        mat = [[float(j) for j in i] for i in self.matx]
        print("matx(")
        for i in mat:
            print('|', str(i)[1:-1], '|')
        print(')\n')
    
    def rowpop(self, li: list, chk=True, ret=False) -> tuple:
        try:
            match chk:
                case False:
                    pass
                case True:
                    li = Comp.intele(li, self.collen)
                    if li is None:
                        raise Exception
                case _:
                    raise Exception
            retu = [i[1] for i in enumerate(list(self._matx)) if i[0] in li]
            self.matx = tuple([i[1] for i in enumerate(list(self.matx)) if i[0] not in li])
            return tuple(retu)
        except Exception as e:
            Terminate.retrn(ret, e)

    def colpop(self, li: list, chk=True, ret=False) -> tuple:
        try:
            match chk:
                case False:
                    pass
                case True:
                    li = Comp.intele(li, self.collen)
                    if li is None:
                        raise Exception
                case _:
                    raise Exception
            matrix = list()
            retu = list()
            for i in self.matx:
                retu1 = list()
                matrix1 = list()
                for j in enumerate(i):
                    if j[0] in li:
                        retu1.append(j[1])
                    else:
                        matrix1.append(j[1])
                matrix.append(tuple(matrix1))
                retu.append(tuple(retu1))
            self.matx = tuple(matrix)
            del matrix
            return tuple(retu)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns matx as a list
    def matxl(self) -> list:
        return [list(i) for i in self.matx]

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
                    i = i[0]
                    j = Comp.intele(j, self.rowlen)
                    if j is None:
                        raise Exception
                    j = j[0]
                    return self.matx[i][j]
                case _:
                    raise Exception
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
                    i = i[0]
                    return self.matx[i]
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns tuple of i'th column
    def mcol(self, j: int, chk=True, ret=False) -> tuple[Decimal]:
        try:
            match chk:
                case False:
                    return tuple([self.mele(i, j, chk, True) for i in range(self.collen)])
                case True:
                    j = Comp.intele(j, self.rowlen)
                    if j is None:
                        raise Exception
                    j = j[0]
                    return tuple([self.mele(i, j, False, True) for i in range(self.collen)])
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns row or column elements of the matrix
    def gele(self, b: list, r: bool, chk=True, ret=False) -> tuple[tuple[Decimal]]:
        try:
            match r:
                case True:
                    return tuple([self.mrow(i, chk, True) for i in b])
                case False:
                    return tuple([self.mcol(i, chk, True) for i in b])
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(ret, e)

    # add 1 at [0] to matx rows
    def laddone(self) -> tuple[tuple[Decimal]]:
        return tuple([tuple([Decimal('1.0'), ] + list(i)) for i in self.matx])


class matutils:
    @staticmethod
    def addmatx(a: matx, b: matx, r=False, ret=False) -> matx:
        try:
            if Comp.tmatx([a, b]) is None:
                raise Exception
            match r:
                case False:
                    if b.collen != a.collen:
                        raise Exception(str(a.collen) + " != " + str(b.collen))
                    return matx(tuple([tuple(list(a.mrow(i, False, True)) + list(b.mrow(i, False, True))) for i in range(a.collen)]), False, True)
                case True:
                    if b.rowlen != a.rowlen:
                        raise Exception(str(a.rowlen) + " != " + str(b.rowlen))
                    return matx(tuple(list(a.matx) + list(b.matx)), False, True)
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(ret, e)

    @staticmethod
    def maddone(a: matx, ret=False) -> matx:
        try:
            if Comp.tmatx(a) is None:
                raise Exception
            else:
                return matx(a.laddone(), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # convert list x to x
    @staticmethod
    def matlxtox(a: matx, ret=False) -> tuple:
        try:
            if Comp.tmatx(a) is None:
                raise Exception
            return tuple([matx(i, False, True) for i in a.matx])
        except Exception as e:
            Terminate.retrn(ret, e)

    @staticmethod
    def matxtolx(a: tuple, ret=False) -> matx:
        try:
            if Comp.ttup(a) is None:
                raise Exception
            x = list()
            for i in a:
                if Comp.tmatx(i) is None:
                    raise Exception
                if i.collen != 1:
                    raise Exception(str(i.collen) + " != 1")
                x.append(i.matx[0])
            return matx(tuple(x), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns identity matrix of size nxn
    @staticmethod
    def idm(n: int, ret=False) -> matx:
        try:
            n = Comp.tintn(n)
            if n is None:
                raise Exception
            m = list()
            for i in range(n):
                l1 = list()
                for j in range(n):
                    if i == j:
                        l1.append(Decimal('1.0'))
                    else:
                        l1.append(Decimal('0.0'))
                m.append(tuple(l1))
            return matx(tuple(m), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns 0 matrix of size mxn
    @staticmethod
    def zerom(m: int, n: int, ret=False) -> matx:
        try:
            n = Comp.tintn(n)
            m = Comp.tintn(m)
            if m is None or n is None:
                raise Exception
            return matx(tuple([tuple([Decimal('0.0') for _ in range(n)]) for _ in range(m)]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns row or column elements of the matrix
    @staticmethod
    def gele(a: matx, b: list, r=False, ret=False) -> matx:
        try:
            if Comp.tbool(r) is None:
                raise Exception
            if r is True:
                b = Comp.intele(b, a.collen)
            else:
                b = Comp.intele(b, a.rowlen)
            if Comp.tmatx(a) is None or b is None:
                raise Exception
            return matx(a.gele(b, r, False, True), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns the transpose of the matrix
    @staticmethod
    def tpose(a: matx, ret=False) -> matx:
        try:
            if Comp.tmatx(a) is None:
                raise Exception
            lr = a.rowlen
            return matx(a.gele([i for i in range(lr)], False, False, True), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns the co-factor of the matrix element
    @classmethod
    def cofac(cls, a: matx, b: int, c: int, chk=True, ret=False) -> Decimal:
        try:
            match chk:
                case True:
                    x = Comp.intele([b, c], a.collen)
                    if x is None:
                        raise Exception
                    b = x[0]
                    c = x[1]
                    del x
                    if Comp.tmatx(a) is None:
                        raise Exception
                    if a.sqmatx is False:
                        raise Exception("must be a square matrix!")
                case False:
                    pass
                case _:
                    raise Exception
            p = pwr(-1, b + c)
            lc = a.collen
            co = a.matxl()
            for i in range(lc):
                if i != b:
                    co[i].pop(c)
            co.pop(b)
            dn = cls.dnant(matx(tuple([tuple(i) for i in co]), False, True), True)
            cfc = p * dn
            return cfc
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns the determinant of the matrix
    @classmethod
    def dnant(cls, a: matx, ret=False) -> Decimal:
        try:
            if Comp.tmatx(a) is None:
                raise Exception
            if a.sqmatx is False:
                raise Exception("must be a square matrix!")
            a = matx(a, True, True)
            lr = a.rowlen
            if lr == 1:
                d = a.mele(0, 0, False, True)
            else:
                d = 0
                ep = int()
                ele = a.mele(0, 0, False, True)
                li = a.mrow(0, True)
                if ele == 0:
                    for i in range(lr):
                        if i > 0:
                            if li[i] != 0:
                                e = li[i]
                                ep = i
                    if ep is None:
                        return 0
                else:
                    ep = 0
                    e = ele
                for i in range(lr):
                    if i != ep:
                        ele = li[i]
                        fac = -1 * ele / e
                        a.matx = cls.tform(a, i, ep, fac, False, True)
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
    def adjnt(cls, a: matx, ret=False) -> matx:
        try:
            if Comp.tmatx(a) is None:
                raise Exception
            if a.sqmatx is False:
                raise Exception("must be a square matrix!")
            lc = a.collen
            lr = a.rowlen
            return cls.tpose(
                matx(tuple([tuple([cls.cofac(a, i, j, False, True) for j in range(lr)]) for i in range(lc)]), False,
                     True), True)
        except Exception as e:
            print(e)
            Terminate.retrn(ret, e)

    # returns inverse matrix of the matrix
    @classmethod
    def invse(cls, a: matx, ret=False) -> matx:
        try:
            if Comp.tmatx(a) is None:
                raise Exception
            det = cls.dnant(a, True)
            if det is None:
                raise Exception
            if det == 0:
                raise Exception("determinant is 0,\ninverse DNE!")
            return cls.smult(1 / det, cls.adjnt(a, True), True)
        except Exception as e:
            print(e)
            Terminate.retrn(ret, e)

    # returns inverse matrix of the matrix using matrix transformation
    @classmethod
    def invsednant(cls, a: matx, ret=False) -> Decimal:
        try:
            if Comp.tmatx(a) is None:
                raise Exception
            a = matx(a)
            det = cls.dnant(a, True)
            if det is None:
                raise Exception
            if det == 0:
                raise Exception("determinant is 0,\ninverse DNE!")
            elif det > 0:
                a.matx = cls.smult(pwr(det, Decimal(-1 / a.collen)), a, True)
            else:
                a.matx = cls.smult(-pwr(-det, Decimal(-1 / a.collen)), a, True)
            b = cls.idm(a.rowlen, True)
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
                                        a.matx = cls.tform(a, i + 1, i, 1, False, False, True)
                                        a.matx = cls.tform(a, i, i + 1, (1 / ele) - 1, False, False, True)
                                        b.matx = cls.tform(b, i + 1, i, 1, False, False, True)
                                        b.matx = cls.tform(b, i, i + 1, (1 / ele) - 1, False, False, True)
                                    else:
                                        raise Exception("Invalid Matrix Inverse")
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
                b.matx = cls.smult(pwr(det, Decimal(-1 / a.collen)), b, True)
            if det < 0:
                b.matx = cls.smult(-pwr(-det, Decimal(-1 / a.collen)), b, True)
            return cls.dnant(b, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns matrix after row or column tranformation
    @classmethod
    def tform(cls, a: matx, b: int, c: int, d: Decimal, r=False, chk=True, ret=False) -> matx:
        try:
            match chk:
                case True:
                    d = Comp.tdeciml(d)
                    if Comp.tmatx(a) is None or d is None:
                        raise Exception
                    match r:
                        case True:
                            x = Comp.intele([b, c], a.collen)
                            if x is None:
                                raise Exception
                        case False:
                            x = Comp.intele([b, c], a.rowlen)
                            if x is None:
                                raise Exception
                        case _:
                            raise Exception
                    b = x[0]
                    c = x[1]
                case False:
                    pass
                case _:
                    raise Exception
            match r:
                case True:
                    lr = a.rowlen
                    row = a.gele([b, c], True, False, True)
                    a = list(a.matx)
                    a[b] = tuple([row[0][i] + (d * row[1][i]) for i in range(lr)])
                    del row
                    return matx(tuple(a), False, True)
                case False:
                    lc = a.collen
                    col = a.gele([b, c], False, False, True)
                    a = list(cls.tpose(a, True).matx)
                    a[b] = tuple([col[0][i] + (d * col[1][i]) for i in range(lc)])
                    del col
                    return matx(cls.tpose(matx(tuple(a), False, True), True), True, True)
                case _:
                    raise Exception
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns sum of two matrices
    @staticmethod
    def madd(a: matx, b: matx, ret=False) -> matx:
        try:
            if Comp.tmatx([a, b]) is None:
                raise Exception
            alc = a.collen
            alr = a.rowlen
            blc = b.collen
            blr = b.rowlen
            if alc != blc or alr != blr:
                raise Exception(
                    "matrix 1 is " + str(alc) + "X" + str(alr) + "\nmatrix 2 is " + str(blc) + "X" + str(blr))
            return matx(tuple(
                [tuple([a.mele(i, j, False, True) + b.mele(i, j, False, True) for j in range(alr)]) for i in
                 range(alc)]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns difference of two matrices
    @staticmethod
    def msub(a: matx, b: matx, ret=False) -> matx:
        try:
            if Comp.tmatx([a, b]) is None:
                raise Exception
            alc = a.collen
            alr = a.rowlen
            blc = b.collen
            blr = b.rowlen
            if alc != blc or alr != blr:
                raise Exception(
                    "matrix 1 is " + str(alc) + "X" + str(alr) + "\nmatrix 2 is " + str(blc) + "X" + str(blr))
            return matx(tuple(
                [tuple([a.mele(i, j, False, True) - b.mele(i, j, False, True) for j in range(alr)]) for i in
                 range(alc)]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns matrix after scalar multiplication
    @staticmethod
    def smult(a: Decimal, b: matx, ret=False) -> matx:
        try:
            a = Comp.tdeciml(a)
            if a is None:
                raise Exception
            if Comp.tmatx(b) is None:
                raise Exception
            blc = b.collen
            blr = b.rowlen
            return matx(tuple([tuple([a * b.mele(i, j, False, True) for j in range(blr)]) for i in range(blc)]), False,
                        True)
        except Exception as e:
            Terminate.retrn(ret, e)

    @classmethod
    def smultfac(cls, a: tuple, b: matx, r=True, ret=False) -> matx:
        try:
            a = Comp.dtup(a)
            if a is None:
                raise Exception
            if Comp.tmatx(b) is None:
                raise Exception
            if r is True:
                if len(a) != b.collen:
                    raise Exception(str(len(a)) + " != " + str(b.collen))
            else:
                if len(a) != b.rowlen:
                    raise Exception(str(len(a)) + " != " + str(b.rowlen))
            if r is True:
                b = cls.matlxtox(b, True)
                bn = list()
                for i in enumerate(a):
                    bn.append(cls.smult(i[1], b[i[0]], True))
                return cls.matxtolx(tuple(bn), True)
            else:
                b = cls.matlxtox(cls.tpose(b, True), True)
                bn = list()
                for i in enumerate(a):
                    bn.append(cls.smult(i[1], b[i[0]], True))
                return cls.tpose(cls.matxtolx(tuple(bn), True), True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns matrix after matrix multiplication
    @staticmethod
    def mmult(a: matx, b: matx, ret=False) -> matx:
        try:
            if Comp.tmatx([a, b]) is None:
                raise Exception
            alc = a.collen
            alr = a.rowlen
            blc = b.collen
            blr = b.rowlen
            if alr != blc:
                raise Exception(str(alr) + " != " + str(blc))
            return matx(tuple([tuple(
                [sum([a.mele(i, j, False, True) * b.mele(j, k, False, True) for j in range(alr)]) for k in range(blr)])
                for i in range(alc)]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

# print("1")
# z = [1, 2, 3]
# a1 = [z, [5, 2, int(6)], [5, 5, 8]]
# b = [[1, 3, 6], [8, 5, 6], [7, 4, 5]]
# a = matx(a1)
# a.matx = a.matx
# print(a.matxl())
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
# print(a.laddone())
