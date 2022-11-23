# Scheduling term paper presentations through optimization

[![GitHub license](https://img.shields.io/github/license/andremaravilha/tpp-scheduling)](https://github.com/andremaravilha/tpp-scheduling/blob/main/LICENSE) 
[![Build Status](https://travis-ci.org/andremaravilha/cxxtimer.svg?branch=master)](https://travis-ci.org/andremaravilha/cxxtimer) 
![Lines of code](https://img.shields.io/tokei/lines/github/andremaravilha/cxxtimer) 
![GitHub repo size](https://img.shields.io/github/repo-size/andremaravilha/cxxtimer) 

> Prof. André L. Maravilha, D.Sc.  
> *Dept. of Informatics, Management and Design - Centro Fed. de Edu. Tecnológica de Minas Gerais ([url](https://www.cefetmg.br/))*  


## 1. Overview

This is a Python command-line application that automatically schedules and assigns evaluators to term paper presentations according to the availability of the people involved and other constraints. Furthermore, scheduling is carried out in such a way as to balance the number of evaluation tasks assigned to each evaluator. Finally, scheduling also considers the suggestions of wanted and unwanted evaluators for each work, but with a lower priority in relation to the balancing criterion.

To perform scheduling as described above, the application models the problem as a Mixed Integer Linear Programming Problem (MIP), which is solved with [gurobipy](https://pypi.org/project/gurobipy/), the Python API for [Gurobi Optimizer](https://www.gurobi.com/).


## 2. How to prepare your machine to run this application

Some important comments before using this project:  
* This project was developed with Python 3.10 and it requires the modules gurobipy (v. 9.5.1) to run. Other requirements, and their respective versions, are listed at file `requirements.txt`.
* Command in sections bellow assumes your python executable is `python` and the Package Installer for Python (pip) is `pip`.
* Besides, it assumes the `venv` module is installed, since it will be used to build the Python Virtual Environment to run the project.
* As this project uses the `gurobipy` module, a license for Gurobi Optimizer is required. The Gurobi Optimizer license is not included with this project and must be obtained by the user.

### 2.1. Create and activate a Python Virtual Environment (venv)

First, you need to clone this repository or download it in your machine. Then, inside the root directory of the project, create a Python Virtual Environment (venv):
```
python -m venv ./venv
```

After that, you need to activate the virtual environment (venv) to run the `tppscheduling` module.

In Linux machines, it is usually achieved by running the following command: 
```
source venv/bin/activate
```

On Windows:
```
.\venv\Scripts\activate
```

If you want to leave the virtual environment, simple run:
```
deactivate
```

### 2.2. Installing dependencies

Now that your virtual environment is installed, you need to install the dependencies required by this project: 
```
python -m pip install -r requirements.txt
```


## 3. Running the application

### 3.1. Show the help message of the program:

```
python -m tppscheduling --help
```

### 3.2. General structure of the command line

```
python -m tppscheduling FILE
```  
in which:  

`FILE`  
(Required)  
Path to the file with input data.


## License
The code in this repository is licensed under the [MIT License](https://github.com/andremaravilha/tpp-scheduling/blob/main/LICENSE). The packages required to compile and run this project are licensed under the terms of their original authors.


## References
[1] Öncan, T.; Altınel, I. K.; Laporte, G. A comparative analysis of several asymmetric traveling salesman problem formulations. Computers & Operations Research, v. 36, pp. 637-654, 2009.

[2] Miller, C. E.; Tucker, A. W.; Zemlin, R. A. Integer programming formulations and travelling salesman problems. Journal of the Association for Computing Machinery, v.7, pp. 326-329, 1960.

[3] Desrochers, M.; Laporte, G.; Improvements and extensions to the Miller-Tucker-Zemlin subtour elimination constraints. Operations Research Letters, v. 10, pp. 27-36, 1991.

[4] Dantzig, G. B; Fulkerson, D. R.; Johnson, S. M. Solutions of a large-scale traveling-salesman problem. Operations Research, v. 2, pp. 363-410, 1954.
