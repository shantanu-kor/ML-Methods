import math
from decimal import Decimal
from matrix import matx, matutils, pwr
from cmdexec import Terminate, Comp


class Data:
    @classmethod
    def dataxy(cls, x, y, chk: bool) -> tuple:
        try:
            match chk:
                case True:
                    x = cls.__xcheck(x)
                    if x is None:
                        raise Exception
                    y = cls.__ycheck(y)
                    if y is None:
                        raise Exception
                case False: 
                    pass
                case _:
                    raise Exception
            if len(x) != len(y):
                raise Exception(str(len(x))+" != "+str(len(y)))
            return x, y
        except Exception as e:
            Terminate.retrn(True, e)

    # return False for invalid data
    @classmethod
    def __xcheck(cls, x) -> tuple:
        try:
            if type(x) is tuple:
                if type(x[0]) is matx:
                    xl = x[0].rowlen
                    if Comp.tmatx(x) is None:
                        raise Exception
                    for i in x:
                        if i.collen != 1 or i.rowlen != xl:
                            raise Exception
                    return x
            x = matx(x, True, True)
            if x is None:
                raise Exception
            return matutils.matlxtox(x, False, True)
        except Exception as e:
            Terminate.retrn(True, "Invalid list: x\n"+str(e))

    @classmethod
    def __ycheck(cls, y) -> tuple:
        try:
            if type(y) is tuple:
                if type(y[0]) is matx:
                    if Comp.tmatx(y) is None:
                        raise Exception
                    for i in y:
                        if i.collen != 1 or i.rowlen != 1:
                            raise Exception
                    return y
            y = matx(y, True, True)
            if y is None:
                raise Exception
            if y.collen == 1:
                return matutils.matlxtox(matutils.tpose(y, False, True), False, True)
            else:
                return matutils.matlxtox(y, False, True)
        except Exception as e:
            Terminate.retrn(True, "Invalid list: y\n"+str(e))


class data:
    def __init__(self, x, y, chk=True, ret=False) -> None:
        ndata = Data.dataxy(x, y, chk)
        if ndata is None:
            Terminate.retrn(ret, "Invalid data\n")
        if ndata is not None:
            self._data = ndata
            self.datalen = len(ndata[1])
            self.xvars = ndata[0][0].rowlen
            del ndata

    @property
    def data(self) -> tuple:
        return self._data

    # prints the data
    @data.getter
    def pdata(self) -> None:
        for i in range(self.datalen):
            print(str(i) + ": " + str([float(j) for j in self.data[0][i].matx[0]])[1:-1] + " | " + str(
                self.data[1][i].mele(0, 0, False, True)))
        print("\n")

    # returns all x
    def getax(self) -> matx:
        return matutils.matxtolx(self.data[0], False, True)

    # returns all y
    def getay(self) -> matx:
        return matutils.matxtolx(self.data[1], False, True)

    # returns x values from data
    def getx(self, li, chk=True, ret=False) -> tuple:
        try:
            match chk:
                case True:
                    li = Comp.intele(li, self.datalen)
                    if li is None:
                        raise Exception
                case False:
                    pass
                case _:
                    raise Exception
            return tuple([self.data[1][i] for i in li])
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns y values from data
    def gety(self, li, chk=True, ret=False) -> tuple:
        try:
            match chk:
                case True:
                    li = Comp.intele(li, self.datalen)
                    if li is None:
                        raise Exception
                case False:
                    pass
                case _:
                    raise Exception
            return tuple([self.data[1][i] for i in li])
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns data values from data
    def getd(self, li: list, chk=True, ret=False) -> tuple:
        try:
            match chk:
                case True:
                    li = Comp.intele(li, self.datalen)
                    if li is None:
                        raise Exception
                case False:
                    pass
                case _:
                    raise Exception
            return tuple([(self.data[0][i], self.data[1][i]) for i in range(len(li))])
        except Exception as e:
            Terminate.retrn(ret, e)

    # return listed x
    def getlx(self, li: list, chk=True, ret=False) -> tuple:
        try:
            match chk:
                case True:
                    li = Comp.intele(li, self.datalen)
                    if li is None:
                        raise Exception
                case False:
                    pass
                case _:
                    raise Exception
            return tuple([tuple([i.mele(0, j, False, True) for j in li]) for i in self.data[0]])
        except Exception as e:
            Terminate.retrn(ret, e)


class datautils:
    @staticmethod
    def data1(d: data, ret=False) -> data:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            return data(tuple([matutils.maddone(i, False, True) for i in d.data[0]]), d.data[1], False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # add the listed x to data
    @staticmethod
    def addata(d: data, a: tuple, chk=True, ret=False) -> data:
        try:
            return data(tuple([matutils.addmatx(d.data[0][i], a[i], False, chk, True) for i in range(d.datalen)]), d.data[1], False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # retuns a new data object with x of listed positions
    @staticmethod
    def datalx(d: data, p: list, ret=False) -> data:
        try:
            p = Comp.intele(p, d.xvars)
            if p is None:
                raise Exception
            return data(tuple([matx(i, False, True) for i in d.getlx(p, False, True)]), d.data[1], False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # add powers of x at listed positions to data
    @classmethod
    def powlx(cls, d: data, p: list, pw: float, a=1.0, ret=False) -> data:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = Comp.intele(p, d.xvars)
            if p is None:
                raise Exception
            pw = Comp.tdeciml(pw)
            if pw is None:
                raise Exception
            a = Comp.tdeciml(a)
            if a is None:
                raise Exception
            return cls.addata(d, tuple(
                [matx(tuple([pwr(a*j, pw) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # add multiplication of x at listed positions to data
    @classmethod
    def multlx(cls, d: data, p: list, ret=False) -> data:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = Comp.intele(p, d.xvars)
            if p is None:
                raise Exception
            x = d.getlx(p, False, True)
            xn = list()
            for i in x:
                m = 1
                for j in i:
                    m = m * j
                xn.append(matx((m,)))
            return cls.addata(d, tuple(xn), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # add addition of x at listed positions to data
    @classmethod
    def addlx(cls, d: data, p: list, ret=False) -> data:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = Comp.intele(p, d.xvars)
            if p is None:
                raise Exception
            return cls.addata(d, tuple([matx((sum(i),), False, True) for i in d.getlx(p, False, True)]), False,
                              True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # append log of x at listed positions to data
    @classmethod
    def loglx(cls, d: data, p: list, a=1.0, b=math.e, ret=False) -> data:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = Comp.intele(p, d.xvars)
            if p is None:
                raise Exception
            a = Comp.tdeciml(a)
            if a is None:
                raise Exception
            b = Comp.tdecimlp(b)
            if b is None:
                raise Exception
            return cls.addata(d, tuple(
                [matx(tuple([Decimal(str(math.log(a*j, b))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # append x at listed positions as a power to data
    @classmethod
    def expolx(cls, d: data, p: list, a=math.e, t=1.0, ret=False) -> data:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = Comp.intele(p, d.xvars)
            if p is None:
                raise Exception
            a = Comp.tdeciml(a)
            if a is None:
                raise Exception
            t = Comp.tdeciml(t)
            if t is None:
                raise Exception
            return cls.addata(d, tuple(
                [matx(tuple([pwr(a, t*j) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def triglx(cls, d: data, p: list, f='cos', a=1.0, ret=False) -> data:
        try:
            if Comp.tdata(d) is None:
                raise Exception
            p = Comp.intele(p, d.xvars)
            if p is None:
                raise Exception
            a = Comp.tdeciml(a)
            if a is None:
                raise Exception
            match f:
                case 'cos':
                    return cls.addata(d, tuple([matx(tuple([Decimal(str(math.cos(a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
                case 'sin':
                    return cls.addata(d, tuple([matx(tuple([Decimal(str(math.sin(a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
                case 'tan':
                    return cls.addata(d, tuple([matx(tuple([Decimal(str(math.tan(a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
                case 'sec':
                    return cls.addata(d, tuple([matx(tuple([1 / Decimal(str(math.cos(a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
                case 'cosec':
                    return cls.addata(d, tuple([matx(tuple([1 / Decimal(str(math.sin(a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
                case 'cot':
                    return cls.addata(d, tuple([matx(tuple([1 / Decimal(str(math.tan(a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
                case 'acos':
                    return cls.addata(d, tuple([matx(tuple([Decimal(str(math.acos(a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
                case 'asin':
                    return cls.addata(d, tuple([matx(tuple([Decimal(str(math.asin(a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
                case 'atan':
                    return cls.addata(d, tuple([matx(tuple([Decimal(str(math.atan(a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
                case 'asec':
                    return cls.addata(d, tuple([matx(tuple([Decimal(str(math.acos(1 / a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
                case 'acosec':
                    return cls.addata(d, tuple([matx(tuple([Decimal(str(math.asin(1 / a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
                case 'acot':
                    return cls.addata(d, tuple([matx(tuple([Decimal(str(math.atan(1 / a*j))) for j in i]), False, True) for i in d.getlx(p, False, True)]), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)
    

# a = [[1, 2, 2], [2, 3, 4], [7.9999999, 3, 2]]
# b = [3, ]
# c = [2, ]
# y = data(a, [2, 3, 4])
# y.pdata
# y = datautils.data1(y)
# y.pdata
# z = y.getlx([1, 0])
# q = datautils.addata(y, tuple([matx(i) for i in z]))
# q.pdata
# y = datautils.powlx(y, [1, 0], 2)
# y.pdata
# y = datautils.multlx(y, [1, 0])
# y.pdata
# y = datautils.addlx(y, [0, 4])
# y.pdata
# y = datautils.loglx(y, [5, 6], 10)
# y.pdata
# y = datautils.expolx(y, [1, 8], 2)
# y = datautils.triglx(y, [1, 8])
# n = datautils.datalx(y, [7, 8, 10])
# y.pdata
# n.pdata
