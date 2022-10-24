from utils.deciml import deciml, algbra as alg, constant as cnst, stat, Decimal
from utils.cmpr import eqval, eqllen, tdict, tdata, tdeciml, tint
from utils.terminate import retrn
from dobj.matrix import matx, matutils, melutils
from dobj.data import data, datautils
from algoutils import Scale, Calculate


class _Predict:

    @staticmethod
    def _py(x: matx, p: matx, const: tuple[bool, bool], ret='a') -> int:
        try:
            match const[1]:
                case True:
                    x = matutils.maddval(x, deciml('1.0'), False, 'c')
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            match const[0]:
                case False:
                    e = cnst.e()
                    h =  alg.div(1, alg.add(1, alg.pwr(e, alg.mul(-1, matutils.mmult(p, matutils.tpose(x, False, 'c'), False, 'c').matx[0][0]))))
                    if h is None:
                        raise Exception
                    if h < 0.5:
                        return False
                    else:
                        return True
                case True:
                    p = matx(p, False, 'c')
                    p0 = p.pop(0, False, False, 'c')[0]
                    e = cnst.e()
                    h =  alg.div(1, alg.add(1, alg.pwr(e, alg.mul(-1, p0, matutils.mmult(p, matutils.tpose(x, False, 'c'), False, 'c').matx[0][0]))))
                    if h is None:
                        raise Exception
                    if h < 0.5:
                        return 0
                    else:
                        return 1
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
        except Exception as e:
            retrn(ret, e)
    
    @staticmethod
    def _pally(x: matx, p: matx, const: tuple[bool, bool], ret='a') -> tuple[bool, ...]:
        try:
            match const[1]:
                case True:
                    x = matutils.maddval(x, deciml('1.0'), False, 'c')
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            match const[0]:
                case False:
                    e = cnst.e()
                    h = [alg.div(1, alg.add(1, alg.pwr(e, alg.mul(-1, i[0])))) for i in matutils.mmult(x, matutils.tpose(p, False, 'c'), False, 'c').matx]
                case True:
                    p = matx(p, False, 'c')
                    p0 = p.pop(0, False, False, 'c')[0]
                    e = cnst.e()
                    h = [alg.div(1, alg.add(1, alg.pwr(e, alg.mul(-1, p0, i[0])))) for i in matutils.mmult(x, matutils.tpose(p, False, 'c'), False, 'c').matx]
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            li = list()
            for i in h:
                if i < 0.5:
                    li.append(0)
                else:
                    li.append(1)
            return tuple(li)
        except Exception as e:
            retrn(ret, e)


class PLogReg(_Predict):
    
    @classmethod
    def y(cls, x: list, p: list, const=(False, True), ret='a') -> int:
        try:
            if (p := matx(p, ret='c')) is None:
                raise Exception
            if (x := matx(x, ret='c')) is None:
                raise Exception
            match const:
                case (True, True):
                    if p.rowlen != x.rowlen + 2:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                case (False, True):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (True, False):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (False, False):
                    if p.rowlen != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._py(x, p, const, 'c')
        except Exception as e:
            retrn(ret, e)
    
    @classmethod
    def ally(cls, x: list[list | tuple] | tuple[list | tuple], p: list, const=(False, True), ret='a') -> matx:
        try:
            if (x := matx(x, ret='c')) is None or (p := matx(p, ret='c')) is None:
                raise Exception
            match const:
                case (True, True):
                    if p.rowlen != x.rowlen + 2:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                case (False, True):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (True, False):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (False, False):
                    if p.rowlen != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._pally(x, p, const, 'c')
        except Exception as e:
            retrn(ret, e)

    @classmethod
    def clas(cls, x: list, d: dict, const=(False, True), ret='a') -> int:
        try:
            if tdict.dic(d) is None:
                raise Exception
            c = dict()
            for i in d.items():
                cl = cls.y(i[1]["parameters"], x, const, 'c')
                if cl is None:
                    raise Exception
                if cl == 1:
                    c[i[0][1]] = c.setdefault(i[0][1], 0) + 1
                else:
                    c[i[0][0]] = c.setdefault(i[0][0], 0) + 1
            mx = 0
            mc = 0
            for i in c.items():
                if i[1] > mx:
                    mx = i[1]
                    mc = i[0]
            return mc
        except Exception as e:
            retrn(ret, e)
    
    @classmethod
    def allclas(cls, x: tuple[list | tuple] | list[list | tuple], d: dict, ret='a') -> dict:
        try:
            if tdict.dic(d) is None:
                raise Exception
            r1 = dict()
            x = matutils.matlxtox(x, False, 'c')
            for i in d.items():
                if (cl := cls.ally(x, i[1], 'c')) is not None:
                    for j in enumerate(cl):
                        r1[x[j[0]]] =  r1.setdefault(x[j[0]], []) + [i[0][j[1]], ]
                else:
                    raise Exception
            r = list()
            return tuple([stat.mode(r1[tuple(i)]) for i in x])
        except Exception as e:
            retrn(ret, e)


class _ScalePar:

    # scale parameter values for logistic regression
    @staticmethod
    def _0to1(c: matx, f: matx, p: matx, const=True, ret='a') -> matx:
        try:
            p = matx(p, False, 'c')
            match const:
                case True:
                    p0 = (alg.add(p.pop(0, False, False, 'c')[0], alg.addl(matutils.smultfac(p.matx[0], c, False, False, 'c').matx[0])), )
                    p = p0 + matutils.smultfac(f.matx[0], p, False, False, 'c').matx[0]
                    return matx(p, False, 'c')
                case False:
                    p = matutils.smultfac(f.matx[0], p, False, False, 'c').matx[0]
                    return matx(p, False, 'c')
                case _:
                    raise Exception("Invalid argument: const => bool")
        except Exception as e:
            retrn(ret, e)
    
    @staticmethod
    def _orignl(c: matx, f: matx, p: matx, const=True, ret='a') -> matx:
        try:
            p = matx(p, False, 'c')
            match const:
                case True:
                    p0 = p.pop(0, False, False, 'c')[0]
                    p = matutils.smultfac(tuple([alg.div(1, i) for i in f.matx[0]]), p, False, False, 'c')
                    p0 -= matutils.mmult(p, matutils.tpose(c, False, 'c'), False, 'c').matx[0][0]
                    return matx((p0, ) + p.matx[0], False, 'c')
                case False:
                    p = matutils.smultfac(tuple([alg.div(1, i) for i in f.matx[0]]), p, False, False, 'c')
                    return matx(p, False, 'c')
                case _:
                    raise Exception("Invalid argument: const => bool")
        except Exception as e:
            retrn(ret, e)


class _Calculate(_Predict):

    # misclassifications after classification
    @classmethod
    def _misclassed(cls, d: tuple, p: matx, const: tuple[bool, bool], ret='a') -> dict:
        try:
            dic = dict()
            dic.setdefault('0', [0, 0, []])
            dic.setdefault('1', [0, 0, []])
            py = _Predict._pally(d[0], p, const, 'c')
            for i in enumerate(py):
                y = str(d[1].mele(i[0], 0, False, 'c'))
                if i[1] == 0:
                    dic[y][0] += 1
                    if y == '1':
                        dic[y][1] += 1
                        dic[y][2].append(tuple([str(j) for j in d[0].mrow(i[0], False, 'c')]))
                else:
                    dic[y][0] += 1
                    if y == '0':
                        dic[y][1] += 1
                        dic[y][2].append(tuple([str(j) for j in d[0].mrow(i[0], False, 'c')]))
            return dic
        except Exception as e:
            retrn(ret, e)


class _Grades(_ScalePar, Calculate):
    
    @classmethod
    def _logreg(cls, d: tuple, p: matx, a: Decimal, m: int, pr: Decimal, const: tuple[bool, bool], ret='a') -> tuple[matx, int]:
        try:
            c, a = 0, alg.mul(-1, a)
            m += 1
            while (c := c + 1) != m:
                match const[0]:
                    case False:
                        e = cnst.e()
                        h = melutils.pow((Decimal('1.0'), Decimal('-1.0')), matutils.madd(matutils.eqelm(1, d[0].rowlen, Decimal('1.0'), False, 'c'), melutils.expo((e, Decimal('-1.0')), matutils.mmult(p, d[0], False, 'c'), [0, ], True, False, 'c'), False, 'c'), [0, ], True, False, 'c')
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.mmult(d[0], matutils.tpose(matutils.msub(h, d[1], False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case True:
                        p1 = matx(p, False, 'c')
                        p0 = p1.pop(0, False, False, 'c')[0]
                        e = cnst.e()
                        h = melutils.pow((Decimal('1.0'), Decimal('-1.0')), matutils.madd(matutils.eqelm(1, d[0].rowlen, Decimal('1.0'), False, 'c'), melutils.expo((e, Decimal('-1.0')), matutils.smult(p0, matutils.mmult(p1, d[0], False, 'c'), False, 'c'), [0, ], True, False, 'c'), False, 'c'), [0, ], True, False, 'c')
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.addmatx(matutils.mmult(matutils.mmult(p1, d[0], False, 'c'), matutils.tpose(matutils.msub(h, d[1], False, 'c'), False, 'c'), False, 'c'), matutils.mmult(matutils.smult(p0, d[0], False, 'c'), matutils.tpose(matutils.msub(h, d[1], False, 'c'), False, 'c'), False, 'c'), True, False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")        
                if pn is None:
                    raise Exception
                err = Calculate._cmperrpr(p, pn, pr)
                match err:
                    case True:
                        p.matx = pn
                        return p, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return p, c - 1
        except Exception as e:
            retrn(ret, e)
    
    @classmethod
    def _logregsp(cls, d: tuple, p: matx, a, m, pr, cf: tuple[matx, matx], const: tuple[bool, bool], ret='a') -> tuple[matx, int]:
        try:
            scc = cf[0]
            scf = cf[1]
            c, a = 0, alg.mul(-1, a)
            m += 1
            while (c := c + 1) != m:
                match const[0]:
                    case False:
                        e = cnst.e()
                        h = melutils.pow((Decimal('1.0'), Decimal('-1.0')), matutils.madd(matutils.eqelm(1, d[0].rowlen, Decimal('1.0'), False, 'c'), melutils.expo((e, Decimal('-1.0')), matutils.mmult(p, d[0], False, 'c'), [0, ], True, False, 'c'), False, 'c'), [0, ], True, False, 'c')
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.mmult(d[0], matutils.tpose(matutils.msub(h, d[1], False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case True:
                        p1 = matx(p, False, 'c')
                        p0 = p1.pop(0, False, False, 'c')[0]
                        e = cnst.e()
                        h = melutils.pow((Decimal('1.0'), Decimal('-1.0')), matutils.madd(matutils.eqelm(1, d[0].rowlen, Decimal('1.0'), False, 'c'), melutils.expo((e, Decimal('-1.0')), matutils.smult(p0, matutils.mmult(p1, d[0], False, 'c'), False, 'c'), [0, ], True, False, 'c'), False, 'c'), [0, ], True, False, 'c')
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.addmatx(matutils.mmult(matutils.mmult(p1, d[0], False, 'c'), matutils.tpose(matutils.msub(h, d[1], False, 'c'), False, 'c'), False, 'c'), matutils.mmult(matutils.smult(p0, d[0], False, 'c'), matutils.tpose(matutils.msub(h, d[1], False, 'c'), False, 'c'), False, 'c'), True, False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")       
                if pn is None:
                    raise Exception
                match const[0]:
                    case False:
                        op = _ScalePar._orignl(scc, scf, p, const[1], 'c')
                        opn = _ScalePar._orignl(scc, scf, pn, const[1], 'c')
                        if op is None or opn is None:
                            raise Exception
                    case True:
                        op = matutils.maddval(_ScalePar._orignl(scc, scf, matx(p.matx[0][1:], False, 'c'), const[1], 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                        opn = matutils.maddval(_ScalePar._orignl(scc, scf, matx(pn.matx[0][1:], False, 'c'), const[1], 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                        if op is None or opn is None:
                            raise Exception
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                err = Calculate._cmperrpr(op, opn, pr)
                match err:
                    case True:
                        p.matx = pn
                        return p, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return p, c - 1
        except Exception as e:
            retrn(ret, e)


def _grades(d: data, p: matx, a: Decimal, m: int, pr: Decimal, scale: bool, const: tuple[bool, bool], ret='a') -> dict:
    try:
        da = d.data
        match scale:
            case True:
                sc = Scale._scale0to1x(d.getax(), 'c')
                if sc is None:
                    raise Exception
                d, scc, scf = data(sc["values"], d.getay(), False, 'c'), sc["constant"], sc["factor"]
                del sc
                match const[0]:
                    case False:
                        match const[1]:
                            case True:
                                d = datautils.dataval(d, Decimal('1.0'), False, 'c')
                            case False:
                                c = matutils.smultfac([alg.div(1, i) for i in scf.matx[0]], scc, False, False, 'c')
                                d = data(matutils.saddcnst(c, d.getax(), False, False, 'c'), d.getay(), False, 'c')
                            case _:
                                raise Exception("Invalid argument: const => (bool, bool)")
                    case True:
                        match const[1]:
                            case True:
                                d = datautils.dataval(d, Decimal('1.0'), False, 'c')
                            case False:
                                c = matutils.smultfac([alg.div(1, i) for i in scf.matx[0]], scc, False, False, 'c')
                                d = data(matutils.saddcnst(c, d.getax(), False, False, 'c'), d.getay(), False, 'c')
                            case _:
                                raise Exception("Invalid argument: const => (bool, bool)")
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                match const[0]:
                    case False:
                        p = _ScalePar._0to1(scc, scf, p, const[1], 'c')
                        if p is None:
                            raise Exception
                    case True:
                        p = matutils.maddval(_ScalePar._0to1(scc, scf, matx(p.matx[0][1:], False, 'c'), const[1], 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                        if p is None:
                            raise Exception
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
            case False:
                match const[1]:
                    case True:
                        d = datautils.dataval(d, deciml('1.0'), False, 'c')
                    case False:
                        pass
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
            case _:
                raise Exception("Invalid argument: scale => bool")
        d1 = (matutils.tpose(d.getax()), matutils.tpose(d.getay()))
        match scale:
            case True:
                p1 = _Grades._logregsp(d1, p, a, m, pr, (scc, scf), const, 'c')
            case False:
                p1 = _Grades._logreg(d1, p, a, m, pr, const, 'c')
            case _:
                raise Exception("Invalid argument: scale => bool")
        if p is None:
            raise Exception
        p, c = p1
        del p1
        match scale:
            case True:
                match const[0]:
                    case False:
                        p = _ScalePar._orignl(scc, scf, p, const[1], 'c')
                        if p is None:
                            raise Exception
                    case True:
                        p = matutils.maddval(_ScalePar._orignl(scc, scf, matx(p.matx[0][1:], False, 'c'), const[1], 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                        if p is None:
                            raise Exception
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
            case False:
                pass
            case _:
                raise Exception("Invalid argument: scale => bool")
        dic = {"parameters": p.matxl()[0], "iterations": c, }
        miscl = _Calculate._misclassed(da, p, const, 'c')
        if miscl is None:
            raise Exception
        dic.update({"misclassifications": miscl})
        dic.update({"parameters": [str(i) for i in dic["parameters"]]})
        return dic
    except Exception as e:
        retrn(ret, e)


class LogReg:
    
    @staticmethod
    def grades(d: data, p: list, a: float, m=100, pr=0.01, scale=False, const=(False, True), ret='a') -> dict:
        try:
            if tdata(d) is None:
                raise Exception
            if (p := matx(p, True, 'c')) is None or eqval(p.collen, 1) is None or (a := tdeciml.decip(a)) == Decimal('NaN') or (pr := tdeciml.decip(pr)) == Decimal('NaN') or (m := tint.intn(m)) is None:
                raise Exception
            if const == (True, True):
                if p.rowlen != d.xvars + 2:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
            elif const == (True, False) or const == (False, True):
                if p.rowlen != d.xvars + 1:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
            elif const == (False, False):
                if p.rowlen != d.xvars:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
            else:
                raise Exception("Invalid argument: const => (bool, bool)")
            return _grades(d, p, a, m, pr, scale, const, 'c')
        except Exception as e:
            retrn(ret, e)

    @classmethod
    def gradesgc(cls, d: dict, p: dict, a: float, m=100, pr=0.01, scale=False, const=(False, True), ret='a') -> dict:
        try:
            if tdict.matchkeys(d, p) is None or  eqllen(list(p.values())) is None or tdata(list(d.values()), True) is None:
                raise Exception
            dic = dict()
            match scale:
                case False:
                    for i in d.items():
                        dic[i[0]] = cls.grades(i[1], p[i[0]], a, m, pr, False, const, 'c')
                    return dic
                case True:
                    for i in d.items():
                        dic[i[0]] = cls.grades(i[1], p[i[0]], a, m, pr, True, const, 'c')
                    return dic
                case _:
                    raise Exception
        except Exception as e:
            retrn(ret, e)
