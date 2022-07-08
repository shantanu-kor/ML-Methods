from time import sleep
from decimal import Decimal


class _terminate:
    @staticmethod
    def _stop() -> None:
        exit(1)

    @classmethod
    def _ask(cls, q: str) -> None:
        if q == 'n':
            pass
        elif q == 'y':
            cls._stop()
        else:
            print("Invalid Input!\n")
            cls._stop()

    @classmethod
    def _wait(cls, t: int) -> None:
        try:
            if type(t) != int or t < 0:
                cls._stop()
            print("Press Ctrl+C to continue...")
            for i in range(t):
                if i == t - 1:
                    print("1")
                    sleep(0.5)
                    print("exiting...")
                    sleep(0.5)
                else:
                    print(t - i)
                    sleep(1)
            cls._stop()
        except KeyboardInterrupt:
            print("\n")


class Terminate(_terminate):
    @classmethod
    def stop(cls) -> None:
        cls._stop()

    @classmethod
    def ask(cls, a='n') -> None:
        cls._ask(a)

    @classmethod
    def wait(cls, t=5) -> None:
        cls._wait(t)

    @classmethod
    def retrn(cls, r: bool, e: str | TypeError | Exception):
        if r is False:
            print(e)
            print("Invalid command!\n")
            cls.wait()
        if r is True:
            print(e)
            pass
        if type(r) != bool:
            print(str(type(r)) + " is not bool")
            cls.stop()


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
    def dlist(cls, li: list) -> list:
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

    # return true if data
    @staticmethod
    def tdata(d) -> bool:
        try:
            if type(d) is list:
                for i in d:
                    if i.__class__.__name__ != 'data':
                        raise Exception(str(type(i)) + " is not data")
                return True
            if d.__class__.__name__ != 'data':
                raise Exception(str(type(d)) + " is not data")
            else:
                return True
        except Exception as e:
            Terminate.retrn(True, e)

    # return if positive float
    @classmethod
    def tdecimlp(cls, a: float | int) -> Decimal:
        try:
            an = cls.tdeciml(a)
            if an is None:
                raise Exception
            if an <= 0:
                raise Exception(str(a) + " is not positive")
            return an
        except Exception as e:
            print(e)

    @staticmethod
    def tdict(a: dict) -> bool:
        try:
            if type(a) is dict:
                return True
            else:
                raise Exception(str(type(a)) + " is not dict")
        except Exception as e:
            print(e)

    @classmethod
    def matchkeys(cls, a: dict, b: dict) -> bool:
        try:
            if cls.tdict(a) is None or cls.tdict(b) is None:
                raise Exception
            a = a.keys()
            b = list(b.keys())
            if len(a) != len(b):
                raise Exception(str(len(a)) + " != " + str(len(b)))
            for i in a:
                if i in b:
                    b.remove(i)
                else:
                    raise Exception("Keys are not same")
            return True
        except Exception as e:
            print(e)

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
