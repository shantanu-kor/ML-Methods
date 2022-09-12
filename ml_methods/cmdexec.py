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
        _terminate._stop()

    @classmethod
    def ask(cls, a='n') -> None:
        _terminate._ask(a)

    @classmethod
    def wait(cls, t=5) -> None:
        _terminate._wait(t)

    @classmethod
    def retrn(cls, r: bool, e: str | TypeError | Exception, ask=False):
        try:
            if r is False:
                print(e)
                print("Invalid command!\n")
                match ask:
                    case False:
                        cls.wait()
                    case True:
                        a = input("Exit: y/n")
                        cls.ask(a)
                    case _:
                        print(ask.__class__.__name__ + " is not bool")
                        raise Exception   
            if r is True:
                print(e)
                pass
            if type(r) != bool:
                print(r.__class__.__name__ + " is not bool")
                raise Exception
        except:
            cls.stop()


class Comp:

    @staticmethod
    def eqval(a, b) -> bool:
        try:
            if a == b:
                return True
            else:
                raise Exception(str(a) + " != " + str(b))
        except Exception as e:
            Terminate.retrn(True, e)

    # return True if matx
    @staticmethod
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
            Terminate.retrn(True, e)

    # return True if bool
    @staticmethod
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
            Terminate.retrn(True, e)

    # return True if tuple
    @staticmethod
    def ttup(a: tuple | tuple[tuple]) -> bool:
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
            Terminate.retrn(True, e)

    # return list if list
    @staticmethod
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
            Terminate.retrn(True, e)

    # return True if lengths of lists are equal
    @classmethod
    def lenlist(cls, a: list[list] | tuple[list]) -> bool:
        try:
            if (ta := a.__class__.__name__) == 'tuple' or ta == 'list':
                for i in range(len(a)):
                    if i == 0:
                        l0 = len(a[i])
                    if i > 0:
                        if (li := len(a[i])) != l0:
                            raise Exception(li + " != " + l0)
                else:
                    return True
            else:
                raise Exception("Invalid argument: a => list/tuple")
        except Exception as e:
            Terminate.retrn(True, e)

    # return True if lengths of tuple are equal
    @classmethod
    def lentup(cls, a: tuple[tuple] | list[tuple]) -> bool:
        try:
            if (ta := a.__class__.__name__) == 'tuple' or ta == 'list':
                for i in range(len(a)):
                    if i == 0:
                        l0 = len(a[i])
                    if i > 0:
                        if (li := len(a[i])) != l0:
                            raise Exception(li + " != " + l0)
                else:
                    return True
            else:
                raise Exception("Invalid argument: a => list/tuple")
        except Exception as e:
            Terminate.retrn(True, e)

    # return true if i is valid element index
    @classmethod
    def intele(cls, i: int | float | list[int | float] | tuple[int | float], ln: int | float) -> int | list[int] | tuple[int]:
        try:
            ln = cls.tintn(ln)
            if ln is None:
                raise Exception
            if (ti := i.__class__.__name__) == 'int' or ti == 'float':
                i = cls.tintw(i)
                if i > ln - 1:
                    raise Exception(str(i) + " is more than " + str(ln - 1))
                return i
            elif ti == 'list':
                i = cls.iwlist(i)
                if i is None:
                    raise Exception
            elif ti == 'tuple':
                i = cls.iwtup(i)
                if i is None:
                    raise Exception
            else:
                raise Exception("Invalid argument: i => int/float")
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
            if (ti := i.__class__.__name__) != 'int':
                if ti != 'float':
                    raise Exception(ti + " is not int")
                else:
                    if i == int(i):
                        return int(i)
                    else:
                        raise Exception(ti + " is not int")
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

    @classmethod
    def dlist(cls, li: list | list[list]) -> list[Decimal] | list[list[Decimal]]:
        try:
            if cls.tlist(li) is not None:
                if li[0].__class__.__name__ == 'list':
                    return [[cls.tdeciml(j) for j in i] for i in li]
                else:
                    return [cls.tdeciml(i) for i in li]
            else:
                raise Exception
        except Exception as e:
            Terminate.retrn(True, str(e) + "Error: Cannot convert to Decimal")

    @classmethod
    def dtup(cls, li: tuple | tuple[tuple]) -> tuple[Decimal, ...] | tuple[tuple[Decimal, ...]]:
        try:
            if cls.ttup(li) is not None:
                if li[0].__class__.__name__ == 'tuple':
                    return tuple([tuple([cls.tdeciml(j) for j in i]) for i in li])
                else:
                    return tuple([cls.tdeciml(i) for i in li])
            else:
                raise Exception
        except Exception as e:
            Terminate.retrn(True, str(e) + "Error: Cannot convert to Decimal")

    @classmethod
    def iwlist(cls, li: list) -> list[int]:
        try:
            if cls.tlist(li) is not None:
                ln = list()
                for i in li:
                    ln.append((vi := cls.tintw(i)))
                    if vi is None:
                        raise Exception(str(i) + " is not a whole number")    
                return ln
            else:
                raise Exception
        except Exception as e:
            Terminate.retrn(True, e)
    
    @classmethod
    def iwtup(cls, li: tuple) -> tuple[int]:
        try:
            if cls.ttup(li) is not None:
                ln = list()
                for i in li:
                    ln.append((vi := cls.tintw(i)))
                    if vi is None:
                        raise Exception(str(i) + " is not a whole number")
                return tuple(ln)
            else:
                raise Exception
        except Exception as e:
            Terminate.retrn(True, e)

    # return true if data
    @staticmethod
    def tdata(d) -> bool:
        try:
            if (td := d.__class__.__name__) == 'list':
                for i in d:
                    if (ti := i.__class__.__name__) != 'data':
                        raise Exception(ti + " is not data")
                return True
            if td != 'data':
                raise Exception(td + " is not data")
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
            Terminate.retrn(True, e)

    @staticmethod
    def tdict(a: dict) -> bool:
        try:
            if (ta := a.__class__.__name__) == 'dict':
                return True
            else:
                raise Exception(ta + " is not dict")
        except Exception as e:
            Terminate.retrn(True, e)

    @classmethod
    def matchkeys(cls, a: dict, b: dict) -> bool:
        try:
            if cls.tdict(a) is None or cls.tdict(b) is None:
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
            Terminate.retrn(True, "Keys are not same")

    @staticmethod
    def taxn(a) -> bool:
        try:
            if (ta := a.__class__.__name__) != 'axn':
                raise Exception(True, ta + " is not axn")
            else:
                return True
        except Exception as e:
            Terminate.retrn(True, e)

    @staticmethod
    def tpoly(a) -> bool:
        try:
            if (ta := a.__class__.__name__) != 'poly':
                raise Exception(True, ta + " is not poly")
            else:
                return True
        except Exception as e:
            Terminate.retrn(True, e)

    @staticmethod
    def tapolyn(a) -> bool:
        try:
            if (ta := a.__class__.__name__) != 'apolyn':
                raise Exception(True, ta + " is not apolyn")
            else:
                return True
        except Exception as e:
            Terminate.retrn(True, e)
