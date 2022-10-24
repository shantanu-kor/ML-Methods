import json
from utils.deciml import deciml, algbra as alg,  Decimal
from utils.cmpr import eqval, tdeciml, tdata, tdict, tmatx
from utils.terminate import retrn
from dobj.matrix import matx, matutils
from dobj.data import data


class apn:
    def __init__(self, apn: tuple[Decimal | Decimal], chk=True, ret='a') -> None:
        try:
            match chk:
                case False:
                    self.__apn = matx(apn, False, 'c')
                case True:
                    apn = matx(apn, True, 'c')
                    if apn is None or eqval(apn.rowlen, 2) is None or eqval(apn.collen, 1) is None:
                        raise Exception
                    self.__apn = apn
                case _:
                    raise Exception("Invalid argument: chk => bool")
            if self.__apn.mele(0, 1, False, 'c') == 0:
                self.__dapn = None
            else:
                self.__dapn = matx(tuple([alg.mul(self.__apn.mele(0, 0, False, 'c'), self.__apn.mele(0, 1, False, 'c')), alg.sub(self.__apn.mele(0, 1, False, 'c'), 1)]), False, 'c')
            del apn
            self.val = lambda p: self.__fval(p)
            self.dval = lambda p: self.__fdval(p)
        except Exception as e:
            retrn(ret, e)

    def __fval(self, p: Decimal) -> Decimal:
        if self.__apn.mele(0, 1, False, 'c') == 0:
            return self.__apn.mele(0, 0, False, 'c')
        else:
            return alg.mul(self.__apn.mele(0, 0, False, 'c'), alg.pwr(p, self.__apn.mele(0, 1, False, 'c')))

    def __fdval(self, p: Decimal) -> Decimal:
        if self.__dapn == None:
            return Decimal('0.0')
        else:
            return alg.mul(self.__dapn.mele(0, 0, False, 'c'), alg.pwr(p, self.__dapn.mele(0, 1, False, 'c')))


class parameter:
    def __init__(self, li: list[list[list]] | tuple[tuple[tuple[Decimal, Decimal], ...], ...], chk=True, ret='a') -> None:
        try:
            par = list()
            n = list()
            for i in li:
                par1 = list()
                for j in i:
                    par1.append(apn(j, chk, 'c'))
                n.append(len(par1))
                par.append(tuple(par1))
            self.__par = tuple(par)
            self.n = tuple(n)
            del par, n
            self.val = lambda p: self.__fval(p)
            self.dval = lambda p: self.__fdval(p)
        except Exception as e:
            retrn(ret, e)
    
    def __fval(self, p: matx) -> tuple[matx, ...]:
        l = list()
        for i in enumerate(self.__par):
            pv = p.mele(0, i[0], False, 'c')
            li = list()
            for j in i[1]:
                li.append(j.val(pv))
            l.append(matx(tuple(li), False, 'c'))
        return tuple(l)
    
    def __fdval(self, p: matx) -> tuple[matx, ...]:
        l = list()
        for i in enumerate(self.__par):
            pv = p.mele(0, i[0], False, 'c')
            li = list()
            for j in i[1]:
                li.append(j.dval(pv))
            l.append(matx(tuple(li), False, 'c'))
        return tuple(l)


class function:
    def __init__(self, li: tuple, chk=True, ret='a') -> None:
        try:
            match chk:
                case True:
                    if tmatx(li, True) is None:
                        raise Exception
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: chk => bool")
            self.__x = li
            self.val = lambda p: self.__fval(p)
            del li
        except Exception as e:
            retrn(ret, e)
    
    def __fval(self, p: tuple[matx, ...]) -> matx:
        for i in enumerate([matutils.mmult(i[1], matutils.tpose(p[i[0]]), False, 'c') for i in enumerate(self.__x)]):
            if i[0] == 0:
                x = i[1]
            else:
                x = matutils.addmatx(x, i[1], False, False, 'c')
        return x


class Calculate:

    @classmethod
    def _cmperrpr(cls, p: matx, pn: matx, pr: Decimal, ret='a') -> bool:
        try:
            for i in range(pn.rowlen):
                if float(pn.mele(0, i, False, 'c')) == float("nan") or float(pn.mele(0, i, False, 'c')) == float(deciml("inf")) or float(pn.mele(0, i, False, 'c')) == float("-inf"):
                    for j in range(pn.rowlen):
                            print("parameter " + str(j) + " is " + str(float(pn.mele(0, j, False, 'c'))))
                    raise Exception
            err = alg.pwr(alg.div(alg.addl([alg.pwr(alg.div(alg.sub(i[1], p.mele(0, i[0], False, 'c')), i[1]), 2) for i in enumerate(pn.matx[0])]), p.rowlen), 0.5)
            if err < pr:
                return True
            else:
                return False
        except Exception as e:
            retrn(ret, e)


class Scale:

    # scale matx between [0, 1]
    @classmethod
    def _scale0to1x(cls, x: matx, ret='a') -> dict:
        try:
            x = matutils.tpose(x, False, 'c')
            mx = list()
            mn = list()
            for i in x.matx:
                mn.append(min(i))
            x = matutils.msub(x, matx(tuple([tuple([mn[i] for _ in range(x.rowlen)]) for i in range(x.collen)]), False, 'c'), False, 'c')
            for i in x.matx:
                mx.append(max(i))
            x = matutils.tpose(matutils.smultfac(tuple([1/ i for i in mx]), x, True, False, 'c'), False, 'c')
            if x is None:
                raise Exception
            return {"constant": matx(tuple(mn), False, 'c'), "factor": matx(tuple(mx), False, 'c'), "values": x}
        except Exception as e:
            retrn(ret, e)

    # scale data values between [0,1]
    @classmethod
    def _scale0to1(cls, d: data, ret='a') -> dict:
        try:
            x = cls._scale0to1x(d.getax(), 'c')
            y = cls._scale0to1x(d.getay(), 'c')
            if x is None or y is None:
                raise Exception
            return {"constant": matutils.addmatx(x["constant"], y["constant"], chk=False, ret='c'),
                    "factor": matutils.addmatx(x["factor"], y["factor"], chk=False, ret='c'),
                    "data": data(x["values"], y["values"], False, 'c')}
        except Exception as e:
            retrn(ret, e)


class _Output:
    # save the regression output
    @classmethod
    def _save(cls, li: str, d: dict, k: str) -> None:
        try:
            with open(li, 'r') as f:
                dic = json.load(f)
            dic[k] = cls.__chktuple(d)
            with open(li, 'w') as f:
                json.dump(dic, f)
        except Exception as e:
            retrn('c', e)

    @classmethod
    def __chktuple(cls, d: dict) -> dict:
        try:
            dic = dict()
            for i in d.keys():
                if type(d[i]) == dict:
                    if type(i) != tuple:
                        dic.update({i: cls.__chktuple(d[i])})
                    else:
                        dic.update({str(i): cls.__chktuple(d[i])})
                else:
                    if type(i) != tuple:
                        dic.update({i: d[i]})
                    else:
                        dic.update({str(i): d[i]})
            return dic
        except Exception as e:
            retrn('c', e)


class _getData:
    # transform json data into data object for regression
    @staticmethod
    def _regression(li: str) -> data:
        try:
            with open(li, 'r') as f:
                dic = json.load(f)
            x = list()
            y = list()
            for i in dic["points"].values():
                x.append(i[0])
                y.append([i[1]])
            return data(x, y)
        except Exception as e:
            retrn('c', e)

    # transform json data into data object for classification
    @classmethod
    def _classification(cls, li: str) -> dict:
        try:
            with open(li, 'r') as f:
                dic = json.load(f)
            d = dict()
            for i, j in dic["classes"].items():
                for k, l in dic["classes"].items():
                    if k > i:
                        d[(i, k)] = cls._clasdata(j, l)
            return d
        except Exception as e:
            retrn('c', e)

    @staticmethod
    def _clasdata(x1: list, x2: list) -> data:
        try:
            return data(x1 + x2, [[0.0] for _ in range(len(x1))] + [[1.0] for _ in range(len(x2))])
        except Exception as e:
            retrn('c', e)

    @staticmethod
    def _regdata(y: list, x: tuple) -> data:
        try:
            lx = list()
            for i in x:
                lx.append(i)
            return data(matutils.tpose(matx(lx)).matx, y)
        except Exception as e:
            retrn('c', e)


class Results(_Output):
    @classmethod
    def save(cls, d: dict, li: str, k: str, ret='a') -> None:
        try:
            _Output._save(li, d, k)
        except Exception as e:
            retrn(ret, e)


class GetData(_getData):
    @classmethod
    def regression(cls, li: str, ret='a') -> data:
        try:
            return _getData._regression(li)
        except Exception as e:
            retrn(ret, e)

    @classmethod
    def classification(cls, li: str, ret='a') -> dict:
        try:
            return _getData._classification(li)
        except Exception as e:
            retrn(ret, e)

    @classmethod
    def regdata(cls, y: list, *x: list, ret='a') -> data:
        try:
            return _getData._regdata(y, x)
        except Exception as e:
            retrn(ret, e)

    @classmethod
    def clasdata(cls, c0: list, c1: list, ret='a') -> data:
        try:
            return _getData._clasdata(c0, c1)
        except Exception as e:
            retrn(ret, e)


class Parameter:
    @staticmethod
    def parlogreg(d: dict, p: list, ret='a') -> dict:
        try:
            if tdict.dic(d) is None:
                raise Exception
            if (p := tdeciml.dall(p)) is None:
                raise Exception
            if tdata(list(d.values()), True) is None:
                raise Exception
            pd = dict()
            for i in enumerate(d.keys()):
                pd[i[1]] = p[i[0]]
            return pd
        except Exception as e:
            retrn(ret, e)

    @staticmethod
    def parlogregter(d: dict, ret='a') -> dict:
        try:
            if tdict.dic(d) is None:
                raise Exception
            if tdata(list(d.values()), True) is None:
                raise Exception
            pd = dict()
            for i in d.keys():
                print("class: " + str(i) + "\n")
                p = list()
                for j in range(d[i].xvars + 1):
                    par = input("parameter " + str(j) + "\n")
                    try:
                        par = deciml(str(par))
                    except ValueError:
                        raise Exception(str(par) + " is not float")
                    if par is None:
                        raise Exception
                    p.append(par)
                if p is None:
                    raise Exception
                pd[i] = p
            return pd
        except Exception as e:
            retrn(ret, e)
