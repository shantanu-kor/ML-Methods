# import math
from decimal import Decimal
from matrix import matx, matutils
from cmdexec import Terminate, Comp


class Data(matutils, matx):
    
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
            if Comp.tmatx([x, y], True) is None or Comp.eqval(x.collen, y.collen) is None or Comp.eqval(y.rowlen, 1) is None:
                raise Exception
            return x, y
        except Exception as e:
            Terminate.retrn(True, e)

    # return False for invalid data
    @classmethod
    def __xcheck(cls, x) -> tuple:
        try:
            if x.__class__.__name__ == 'tuple' and x[0].__class__.__name__ == 'matx':
                return matutils.matxtolx(x, True, True)
            x = matx(x, True, True)
            if x is None:
                raise Exception
            return x
        except Exception as e:
            Terminate.retrn(True, "Invalid list: x\n"+str(e))

    @classmethod
    def __ycheck(cls, y) -> tuple:
        try:
            if y.__class__.__name__ == 'tuple' and y[0].__class__.__name__ == 'matx':
                return matutils.matxtolx(y, True, True)
            y = matx(y, True, True)
            if y is None:
                raise Exception
            if y.collen == 1:
                return matutils.tpose(y, False, True)
            else:
                return y
        except Exception as e:
            Terminate.retrn(True, "Invalid list: y\n"+str(e))


class data(Data, matutils, matx):
    
    def __init__(self, x, y, chk=True, ret=False) -> None:
        ndata = Data.dataxy(x, y, chk)
        if ndata is None:
            Terminate.retrn(ret, "Invalid data\n")
        if ndata is not None:
            self._data = ndata
            self.datalen = ndata[0].collen
            self.xvars = ndata[0].rowlen
            del ndata

    @property
    def data(self) -> tuple:
        return self._data

    # prints the data
    @data.getter
    def pdata(self) -> None:
        x = self.data[0].matx
        y = self.data[1].matx
        for i in range(self.datalen):
            print(str(i) + ": " + str([float(j) for j in x[i]])[1:-1] + " | " + str(float(y[i][0])))
        print("\n")

    # returns all x
    def getax(self) -> matx:
        return matx(self.data[0].matx, False, True)

    # returns all y
    def getay(self) -> matx:
        return matx(self.data[1].matx, False, True)

    # returns x values from data
    def getx(self, li, chk=True, ret=False) -> matx:
        try:
            return matutils.gele(self.getax(), li, True, chk, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns y values from data
    def gety(self, li, chk=True, ret=False) -> matx:
        try:
            return matutils.gele(self.getay(), li, True, chk, True)
        except Exception as e:
            Terminate.retrn(ret, e)

    # returns data values from data
    def getd(self, li: list, chk=True, ret=False) -> tuple:
        try:
            return tuple([matutils.gele(self.getax(), li, True, chk, True), matutils.gele(self.getay(), li, True, chk, True)])
        except Exception as e:
            Terminate.retrn(ret, e)

    # return listed x
    def getlx(self, li: list, chk=True, ret=False) -> matx:
        try:
            return matutils.tpose(matutils.gele(self.getax(), li, False, chk, True), False, True)
        except Exception as e:
            Terminate.retrn(ret, e)


class datautils(data, matutils, matx, Comp):
    
    @classmethod
    def dataval(cls, d: data, x: Decimal, chk=True, ret=False) -> data:
        try:
            match chk:
                case False:
                    return data(matutils.maddval(d.getax(), x, False, True), d.getay(), False, True)
                case True:
                    if Comp.tdata(d) is None:
                        raise Exception
                    x = Comp.tdeciml(x)
                    if x is None:
                        raise Exception
                    return data(matutils.maddval(d.getax(), x, False, True), d.getay(), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    # add the listed x to data
    @classmethod
    def addata(cls, d: data, a: matx, chk=True, ret=False) -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), a, False, False, True), d.getay(), False, True)
                case True:
                    if Comp.tdata(d) is None or Comp.tmatx(a) is None or Comp.eqval(d.datalen, a.collen) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), a, False, False, True), d.getay(), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    # retuns a new data object with x of listed positions
    @classmethod
    def datalx(cls, d: data, li: list, chk=True, ret=False) -> data:
        try:
            match chk:
                case False:
                    return data(d.getlx(li, False, True), d.getay(), False, True)
                case True:
                    if Comp.tdata(d) is None:
                        raise Exception
                    return data(d.getlx(li, True, True), d.getay(), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    # add multiplication of x at listed positions to data
    @classmethod
    def multlx(cls, d: data, li: list[list], chk=True, ret=False) -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.multmel(d.getax(), li, False, False, True)), False, False, True), d.getay(), False, True)
                case True:
                    if Comp.tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.multmel(d.getax(), li, False, True, True)), False, False, True), d.getay(), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    # add addition of x at listed positions to data
    @classmethod
    def addlx(cls, d: data, li: list[list], chk=True, ret=False) -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.addmel(d.getax(), li, False, False, True)), False, False, True), d.getay(), False, True)
                case True:
                    if Comp.tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.addmel(d.getax(), li, False, True, True)), False, False, True), d.getay(), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    # add powers of x at listed positions to data
    @classmethod
    def powlx(cls, d: data, an: list[Decimal], li: list, chk=True, ret=False) -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.powmel(an, d.getax(), li, False, False, True)), False, False, True), d.getay(), False, True)
                case True:
                    if Comp.tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.powmel(an, d.getax(), li, False, True, True)), False, False, True), d.getay(), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    # append log of x at listed positions to data
    @classmethod
    def loglx(cls, d: data, an: list[Decimal], li: list, chk=True, ret=False) -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.logmel(an, d.getax(), li, False, False, True)), False, False, True), d.getay(), False, True)
                case True:
                    if Comp.tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.logmel(an, d.getax(), li, False, True, True)), False, False, True), d.getay(), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)

    # append x at listed positions as a power to data
    @classmethod
    def expolx(cls, d: data, an: list[Decimal], li: list, chk=True, ret=False) -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.expomel(an, d.getax(), li, False, False, True)), False, False, True), d.getay(), False, True)
                case True:
                    if Comp.tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.expomel(an, d.getax(), li, False, True, True)), False, False, True), d.getay(), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            Terminate.retrn(ret, e)
    
    @classmethod
    def triglx(cls, d: data, n: Decimal, li: list, f='cos', chk=True, ret=False) -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.trigmel(n, d.getax(), li, False, f, False, True)), False, False, True), d.getay(), False, True)
                case True:
                    if Comp.tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(matutils.trigmel(n, d.getax(), li, False, f, True, True)), False, False, True), d.getay(), False, True)
                case _:
                    raise Exception("Invalid argument: chk => bool")
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
# q = datautils.addata(y, z)
# q.pdata
# y = datautils.powlx(y, [1, 2], [1, 0])
# y.pdata
# y = datautils.multlx(y, [[1, 0], ])
# y.pdata
# y = datautils.addlx(y, [[0, 4], ])
# y.pdata
# y = datautils.loglx(y, [1, 10], [5, 6])
# y.pdata
# y = datautils.expolx(y, [2, 1], [1, 8])
# y = datautils.triglx(y, 1, [1, 8])
# n = datautils.datalx(y, [7, 8, 10])
# y.pdata
# n.pdata
