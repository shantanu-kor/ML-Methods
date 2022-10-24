from matrix import matx, matutils, melutils
from utils.deciml import deciml, Decimal
from utils.cmpr import tmatx, eqval, tdata
from utils.terminate import retrn

class data:
    
    def __init__(self, x, y, chk=True, ret='a') -> None:
        def __dataxy(x, y, chk: bool) -> tuple:
            try:
                # return False for invalid data
                def __xcheck(x) -> tuple:
                    try:
                        if x.__class__.__name__ == 'tuple' and x[0].__class__.__name__ == 'matx':
                            return matutils.matxtolx(x, True, 'c')
                        x = matx(x, True, 'c')
                        if x is None:
                            raise Exception
                        return x
                    except Exception as e:
                        retrn(True, "Invalid list: x\n"+str(e))
                def __ycheck(y) -> tuple:
                    try:
                        if y.__class__.__name__ == 'tuple' and y[0].__class__.__name__ == 'matx':
                            return matutils.matxtolx(y, True, 'c')
                        y = matx(y, True, 'c')
                        if y is None:
                            raise Exception
                        if y.collen == 1:
                            return matutils.tpose(y, False, 'c')
                        else:
                            return y
                    except Exception as e:
                        retrn(True, "Invalid list: y\n"+str(e))
                match chk:
                    case True:
                        x = __xcheck(x)
                        if x is None:
                            raise Exception
                        y = __ycheck(y)
                        if y is None:
                            raise Exception
                    case False: 
                        pass
                    case _:
                        raise Exception
                if tmatx([x, y], True) is None or eqval(x.collen, y.collen) is None or eqval(y.rowlen, 1) is None:
                    raise Exception
                return (x, y), x.collen, x.rowlen
            except Exception as e:
                retrn(True, e)
        if (ndata := __dataxy(x, y, chk)) is not None:
            self.__data, self.__datalen, self.__xvars = ndata
            del ndata
        else:
            retrn(ret, "Invalid data\n")

    @property
    def data(self) -> tuple[matx, matx]:
        return (self.getax(), self.getay())
    
    @property
    def datalen(self) -> int:
        return self.__datalen
    
    @property
    def xvars(self) -> int:
        return self.__xvars

    # prints the data
    @data.getter
    def pdata(self) -> None:
        x = self.__data[0].matx
        y = self.__data[1].matx
        for i in range(self.datalen):
            print(str(i) + ": " + str([str(j) for j in x[i]])[1:-1] + " | " + str(str(y[i][0])))
        print("\n")

    # returns all x
    def getax(self) -> matx:
        return matx(self.__data[0].matx, False, 'c')

    # returns all y
    def getay(self) -> matx:
        return matx(self.__data[1].matx, False, 'c')

    # returns x values from data
    def getx(self, li, chk=True, ret='a') -> matx:
        try:
            return matutils.gele(self.getax(), li, True, chk, 'c')
        except Exception as e:
            retrn(ret, e)

    # returns y values from data
    def gety(self, li, chk=True, ret='a') -> matx:
        try:
            return matutils.gele(self.getay(), li, True, chk, 'c')
        except Exception as e:
            retrn(ret, e)

    # returns data values from data
    def getd(self, li: list, chk=True, ret='a') -> tuple:
        try:
            return tuple([matutils.gele(self.getax(), li, True, chk, 'c'), matutils.gele(self.getay(), li, True, chk, 'c')])
        except Exception as e:
            retrn(ret, e)

    # return listed x
    def getlx(self, li: list, chk=True, ret='a') -> matx:
        try:
            return matutils.tpose(matutils.gele(self.getax(), li, False, chk, 'c'), False, 'c')
        except Exception as e:
            retrn(ret, e)


class datautils:
    
    @staticmethod
    def dataval(d: data, x: Decimal, chk=True, ret='a') -> data:
        try:
            match chk:
                case False:
                    return data(matutils.maddval(d.getax(), x, False, 'c'), d.getay(), False, 'c')
                case True:
                    if tdata(d) is None:
                        raise Exception
                    if (x := deciml(x)) == Decimal('NaN'):
                        raise Exception
                    return data(matutils.maddval(d.getax(), x, False, 'c'), d.getay(), False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # add the listed x to data
    @staticmethod
    def addata(d: data, a: matx, chk=True, ret='a') -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), a, False, False, 'c'), d.getay(), False, 'c')
                case True:
                    if tdata(d) is None or tmatx(a) is None or eqval(d.datalen, a.collen) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), a, False, False, 'c'), d.getay(), False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # retuns a new data object with x of listed positions
    @staticmethod
    def datalx(d: data, li: list, chk=True, ret='a') -> data:
        try:
            match chk:
                case False:
                    return data(d.getlx(li, False, 'c'), d.getay(), False, 'c')
                case True:
                    if tdata(d) is None:
                        raise Exception
                    return data(d.getlx(li, True, 'c'), d.getay(), False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # add multiplication of x at listed positions to data
    @staticmethod
    def multlx(d: data, li: list[list], chk=True, ret='a') -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.mult(d.getax(), li, False, False, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case True:
                    if tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.mult(d.getax(), li, False, True, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # add addition of x at listed positions to data
    @staticmethod
    def addlx(d: data, li: list[list], chk=True, ret='a') -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.add(d.getax(), li, False, False, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case True:
                    if tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.add(d.getax(), li, False, True, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # add powers of x at listed positions to data
    @staticmethod
    def powlx(d: data, an: list[Decimal], li: list, chk=True, ret='a') -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.pow(an, d.getax(), li, False, False, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case True:
                    if tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.pow(an, d.getax(), li, False, True, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # append log of x at listed positions to data
    @staticmethod
    def loglx(d: data, an: list[Decimal], li: list, chk=True, ret='a') -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.log(an, d.getax(), li, False, False, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case True:
                    if tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.log(an, d.getax(), li, False, True, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)

    # append x at listed positions as a power to data
    @staticmethod
    def expolx(d: data, an: list[Decimal], li: list, chk=True, ret='a') -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.expo(an, d.getax(), li, False, False, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case True:
                    if tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.expo(an, d.getax(), li, False, True, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)
    
    @staticmethod
    def triglx(d: data, n: Decimal, li: list, f='cos', chk=True, ret='a') -> data:
        try:
            match chk:
                case False:
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.trig(n, d.getax(), li, False, f, False, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case True:
                    if tdata(d) is None:
                        raise Exception
                    return data(matutils.addmatx(d.getax(), matutils.tpose(melutils.trig(n, d.getax(), li, False, f, True, 'c')), False, False, 'c'), d.getay(), False, 'c')
                case _:
                    raise Exception("Invalid argument: chk => bool")
        except Exception as e:
            retrn(ret, e)
