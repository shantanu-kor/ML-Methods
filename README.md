# ml_methods

I. Preferred format of .json file

+ For regression

  - File Format
    > {"points": {"0": [[x0_0, x0_1, ...], y0], "1": [[x1_0, x1_1, ...], y1], ...}, ...}

  - example
    > {"points": {"0": [[2.3540427990642154, 0.7737640403414014], 4.3229493284554055], "1": [[4.095146853312192, 1.2121045560213373], 6.28063295259671], "2": [[5.499491124236799, 2.9536758743198996], 13.495622116377714], ...}, ...}

+ For classification

  - File Format 
    > {"classes": {"0": [x0, x1, x2, ...], "1": [x0, x1, x2, ...], "2": [x0, x1, x2, ...], ...}, ...}

  - example
    > {"classes": {"0": [[32.41887680043604, 29.007435436549528], [16.276096407368083, 20.893094152439435], [5.5432756944200134, 20.894214547335427], [39.793137371769, 19.46886762797499]], "1": [[108.03178873723705, 81.96021796808306], [74.61517535395302, 71.01239724577263], [60.933081835004295, 51.30716182636451], [62.8359692754738, 78.60358571113937]], ...}, ...}

II. To convert data into "data" object

  > from ml_methods.utils import GetData
  
  > GetData.regression("path/to/file/*.json")
  >>  returns "data" object for regression

  > GetData.classification("path/to/file/*.json")
  >> returns {("0", "1"): "data1", ("0", "2"): "data2", ("1", "2"): "data3", ...}

  > GetData.regdata(y, x_0, x_1, x_3, ...)
  >> returns "data" object for regression

  - example
    > d = GetData.regdata([1,2,3,4], [1,2,3,4], [2,4,6,8], [1,4,9,16], [4,5,9,8])
    >
    > d.pdata
    >>
    >> 0: 1, 2, 1, 4 | 1
    >>
    >> 1: 2, 4, 4, 5 | 2
    >>
    >> 2: 3, 6, 9, 9 | 3
    >>
    >> 3: 4, 8, 16, 8 | 4

  > GetData.clasdata(c0: [x0, x1, x2, ...], c1: [x0, x1, x2, ...])
  >> returns "data" object for classification

  - example
    > d = GetData.clasdata([[0,1,2],[2,1,2],[2,1,5]], [[2,4,5],[5,6,8]])
    >
    > d.pdata
    >>
    >> 0: 0, 1, 2 | 0
    >>
    >> 1: 2, 1, 2 | 0
    >>
    >> 2: 2, 1, 5 | 0
    >>
    >> 3: 2, 4, 5 | 1
    >>
    >> 4: 5, 6, 8 | 1

III. To create data object

  > from ml_methods.data import data
  
  > d = data([[x0_0, x0_1, ...], [x1_0, x1_1, ...], x2, ...], [y0, y1, y2, ...])

  - example
    > d = data([[1,2,3],[2,4,6],[3,6,9], [10,12,12], [15,12,10]], [[6],[12],[18],[25],[26]])
    >
    > d.pdata
    >> 0: 1, 2, 3 | 6
    >>
    >> 1: 2, 4, 6 | 12
    >>
    >> 2: 3, 6, 9 | 18
    >>
    >> 3: 10, 12, 12 | 25
    >>
    >> 4: 15, 12, 10 | 26

IV. To save "dict" object to .json file

  > from ml_methods.utils import Results
  
  > Results.save(d: dict, l: /path/to/file/*json, k: key for d)

V. ALGORITHMS

1. To perform linear regression

  > from ml_methods.algorithms.linreg import LinReg

  + Using gradient descent

    > r = LinReg.grades(d: "data" object, p: list of initial parameters, a: alpha, m: maximum iterations, pr: minimum value of rms(relative error), scale=True to scale x and y values between [0, 1], const=(True to multiply constant, True to add constant))

    - returns 
      > {"parameters": list of final parameters, "iterations": total iterations, "r^2": coefficient of determination, "r^2_adj": adjusted coefficient of determination}

    - example output
      > {'parameters': [0.891520289610992, 0.5821756051997802, -0.07635530662814724, 1.6739062514462162], 'iterations': 404, 'r^2': 0.9974110476265238, 'r^2_adj': 0.9896441905060951}

  + Using matrix method

    > r = LinReg.matrix(d: data, p: list of parameters if method='gauseidel', m: maximum iterations if method='gauseidel', pr: minimum value of rms(relative error of parameters) if method='gauseidel', method: 'inverse' (matrix inverse), 'uttform' (convert to upper triangular matrix), 'gauseidel' (perform Gauss-Seidel iterations), 'tridia' (Convert to tri-diagonal matrix), const=True to add constant)

    - returns
      > {"parameters": list of final parameters, "r^2": coefficient of determination, "r^2_adj": adjusted coefficient of determination}

    - example output
      > {'parameters': [-7.048583938740194e-12, 1.2727272727275363, -1.659090909092015, 2.6818181818197786], 'r^2': 0.9854, 'r^2_adj': 0.9541}

2. To perform weighted linear regression

  > from ml_methods.algorithms.linreg import WeiLinReg

  + Using gradient descent

    > r = WeiLinReg.grades(d: data, p: list of initial parameters, a: alpha, x: list of x values at mean, t: standard deviation of weights, m: maximum iterations, pr: minimum value of rms(relative error of parameters), scale: bool, const: (bool, bool))

    - returns 
      > {"parameters": list of final parameters, "iterations": total iterations, "r^2": coefficient of determination, "r^2_adj": adjusted coefficient of determination}

    - example output
      > {'parameters': [0.891520289610992, 0.5821756051997802, -0.07635530662814724, 1.6739062514462162], 'iterations': 404, 'r^2': 0.9974110476265238, 'r^2_adj': 0.9896441905060951}

  + Using matrix method

    > r = WeiLinReg.matrix(d: data, x: list of x values at mean, t: standard deviation of weights, p: list of parameters if method='gauseidel', m: maximum iterations if method='gauseidel', pr: minimum value of rms(relative error of parameters) if method='gauseidel', method: 'inverse' (matrix inverse), 'uttform' (convert to upper triangular matrix), 'gauseidel' (perform Gauss-Seidel iterations), 'tridia' (Convert to tri-diagonal matrix), const: bool)

    - returns
      > {"parameters": list of final parameters, "iterations": total iterations, "r^2": coefficient of determination}

      - example output
      > {'parameters': [-7.048583938740194e-12, 1.2727272727275363, -1.659090909092015, 2.6818181818197786], 'r^2': 0.9854, 'r^2_adj': 0.9541}

3. To perform logistic regression

  > from ml_methods.algorithms.logreg import LogReg

  + Using gradient descent

    > c = LogReg.grades(d: data, p: list of initial parameters, a: alpha, m: maximum iterations, pr: minimum value of rms(relative error of parameters), scale: bool, const: (bool, bool))

    - returns
      > {"parameters": list of final parameters, "iterations": total iterations, "misclassifications": {"0": [number of points in class, number of misclassified points in class, list of misclassified points], "1": [ ...]}

    - example output
      > {'parameters': [-0.07304315681567916, 0.000724933710071927, 0.000686518905177974], 'iterations': 248, 'misclassifications': {'0': [20, 0, []], '1': [15, 0, []]}}

  + For "dict" with multiple combinations of classes; Using gradient descent

    > c = LogReg.gradesgc(d: dict, p: {("0", "1"): {"parameters": [list of parameters]}, ("0", "2"): ...}, a: alpha, m: maximum iterations, pr: minimum value of rms(relative error of parameters), scale: bool, const: (bool, bool))

    - returns 
      > {('0', '1'): {"parameters": list of final parameters, "iterations": total iterations, "misclassifications": {"0": [number of points in class, number of misclassified points in class, list of misclassified points], ...}}, ('0', '2'): ...}

    - example output
      > {('0', '1'): {'parameters': [-12.589653400309972, 0.233307861859726, 0.012958330133487328], 'iterations': 2890, 'misclassifications': {'0': [20, 0, []], '1': [15, 0, []]}}}

  + To make a "dict" of parameters for .gradesgc and .gradessvgc

    > import utils

    - Same starting parameters for all groups

      > p = utils.parlogreg(d: dict, p: [list of parameters])

      - returns 
        > {("0", "1"): {"parameters": [list of parameters]}, ("0", "2"): ...}

    - Different starting parameters for all groups from terminal
   
      > p = utils.parlogregter(d: dict)

      - enter parameters in terminal

      - returns
        > {("0", "1"): {"parameters": [list of parameters]}, ("0", "2"): ...}

4. To perform gaussian discriminant analysis

  > from ml_methods.algorithms.gda import GDA

  + GDA for 2 classes

    > c = GDA.gda(d: data)

    - returns
      > {"mean": [E(x_class0), E(x_class1)], "phi": [phi_c0, phi_c1], "cov": Cov(X, X), "n": number of independent variables}

    - example output
      > {'mean': [(21.7614897845058, 28.536074158247267), [84.97363451177574, 71.6873834727597]], 'phi': [0.5714285714285714, 0.42857142857142855], 'cov': [[239.8146684608749, 3.335434223573996], [3.335434223573996, 149.664159418036]], 'n': 2, 'misclassifications': {'0': [20, 0, []], '1': [15, 0, []]}}

  + For "dict" with multiple combination of classes

    > c = GDA.gdagc(d: dict)

    - returns
      > {('0', '1'): {"mean": [E(x_class0), E(x_class1)], "phi": [phi_c0, phi_c1], "cov": Cov(X, X), "n": number of independent variables}, ('0', '2'): ...}

    - example output:
      > {('0', '1'): {'mean': [(21.7614897845058, 28.536074158247267), [84.97363451177574, 71.6873834727597]], 'phi': [0.5714285714285714, 0.42857142857142855], 'cov': [[239.8146684608749, 3.335434223573996], [3.335434223573996, 149.664159418036]], 'n': 2, 'misclassifications': {'0': [20, 0, []], '1': [15, 0, []]}}}

5. To get output of predicted values

  + For linear regression
    > from ml_methods.algorithms.linreg import PLinReg
    > PLinReg.y(x: list of variable values, p: list of parameters, const: (bool, bool))
    >> returns predicted value

    - example
      > PLinreg.y([250, ], [316.01954165944966, -1.0586299193986866], (False, True))
      >> 51.36206180977803
    
  + For logistic regression
    > from ml_methods.algorithms.logreg import PLogReg
    > PLogReg(x: list of variable values, p: list of parameters, const: (bool, bool))
    >> returns predicted value

    - example
      > Predict.logreg([100, 10], [-12.589653400309972, 0.233307861859726, 0.012958330133487328], (False, True))
      >> 1
    
    > PLogReg.clas(x: list, d: dict, const: (bool, bool))
    >> returns predicted class

    - example
      > PLogReg.clas([100, 10], {('0', '1'): {'parameters': [-12.589653400309972, 0.233307861859726, 0.012958330133487328], 'iterations': 2890, 'misclassifications': {'0': [20, 0, []], '1': [15, 0, []]}}}, (False, True))
      >> '1'

  + For gda
    > from ml_methods.algorithms.gda import PGDA
    > PGDA.y(x: list, d: dict)
    >> returns predicted value

    - example
      > PGDA.y([100, 10], {'mean': [(21.7614897845058, 28.536074158247267), [84.97363451177574, 71.6873834727597]], 'phi': [0.5714285714285714, 0.42857142857142855], 'cov': [[239.8146684608749, 3.335434223573996], [3.335434223573996, 149.664159418036]], 'n': 2, 'misclassifications': {'0': [20, 0, []], '1': [15, 0, []]}})
      >> 1

    > PGDA.clas(x: list, d: dict)
    >> returns predicted class

    - example
      > Predict.gdagc([100, 10], {('0', '1'): {'mean': [(21.7614897845058, 28.536074158247267), [84.97363451177574, 71.6873834727597]], 'phi': [0.5714285714285714, 0.42857142857142855], 'cov': [[239.8146684608749, 3.335434223573996], [3.335434223573996, 149.664159418036]], 'n': 2, 'misclassifications': {'0': [20, 0, []], '1': [15, 0, []]}}})
      >> '1'