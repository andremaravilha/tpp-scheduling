import gurobipy as gp
from gurobipy import GRB


def solve(data):

    # Get problem data
    I = [i for i in range(0, len(data['works']))]
    J = [j for j in range(0, len(data['evaluators']))]
    H = [h for h in range(0, len(data['datetimes']))]
    S = [s for s in range(0, len(data['rooms']))]

    nHI = [evaluator['constraints']['unavailable-datetimes'] for evaluator in data['works']]
    nHJ = [evaluator['constraints']['unavailable-datetimes'] for evaluator in data['evaluators']]
    HS = [room['available-datetimes'] for room in data['rooms']]
    nHS = [[h for h in H if h not in HS[s]] for s in S]
    
    JI = [work['constraints']['required-evaluators'] for work in data['works']]
    nJI = [work['constraints']['forbidden-evaluators'] for work in data['works']]
    JIX = [work['suggestions']['wanted-evaluators'] for work in data['works']]
    nJIX = [work['suggestions']['unwanted-evaluators'] for work in data['works']]

    q = [work['constraints']['number-evaluators'] for work in data['works']]
    

    # Initialize Gurobi model
    model = gp.Model()

    # Create decision variables
    x = [[model.addVar(lb=0, ub=1, vtype=GRB.BINARY) for j in J] for i in I]
    y = [[model.addVar(lb=0, ub=1, vtype=GRB.BINARY) for s in S] for i in I]
    z = [[model.addVar(lb=0, ub=1, vtype=GRB.BINARY) for h in H] for i in I]
    w = [[model.addVar(lb=0, ub=1, vtype=GRB.CONTINUOUS) for i2 in I] for i1 in I]
    f = [[model.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS) for j2 in J]for j1 in J]
    g = model.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS)

    # Set objective functions
    objective1 = gp.LinExpr()
    for j1 in J:
        for j2 in J:
            objective1 = objective1 + f[j1][j2]

    objective2 = gp.LinExpr()
    objective2 = objective2 + g

    model.setObjectiveN(objective1, 0, 10)
    model.setObjectiveN(objective2, 1, 5)
    model.setAttr(GRB.Attr.ModelSense, GRB.MINIMIZE)

    # Add constraints (1)
    for i in I:
        expr = gp.LinExpr()
        for j in J:
            expr = expr + x[i][j]
        model.addConstr(expr == q[i])

    # Add constraints (2)
    for i in I:
        expr = gp.LinExpr()
        for j in JI[i]:
            model.addConstr(x[i][j] == 1)
    
    # Add constraints (3)
    for i in I:
        expr = gp.LinExpr()
        for j in nJI[i]:
            model.addConstr(x[i][j] == 0)

    # Add constraints (4)
    for i in I:
        expr = gp.LinExpr()
        for s in S:
            expr = expr + y[i][s]
        model.addConstr(expr == 1)

    # Add constraints (5)
    for i in I:
        expr = gp.LinExpr()
        for h in H:
            expr = expr + z[i][h]
        model.addConstr(expr == 1)

    # Add constraints (6)
    for i in I:
        expr = gp.LinExpr()
        for h in nHI[i]:
            expr = expr + z[i][h]
        model.addConstr(expr <= 0)

    # Add constraints (7)
    for i in I:
        for j in J:
            expr = gp.LinExpr()
            for h in nHJ[j]:
                expr = expr + z[i][h]
            model.addConstr(expr <= 1 - x[i][j])

    # Add constraints (8)
    for i in I:
        for s in S:
            expr = gp.LinExpr()
            for h in nHS[s]:
                expr = expr + z[i][h]
            model.addConstr(expr <= 1 - y[i][s])

    # Add constraints (9)
    for i1 in I:
        for i2 in I:
            if i1 != i2:
                for h in H:
                    model.addConstr(w[i1][i2] >= z[i1][h] + z[i2][h] - 1)

    # Add constraints (10)
    for i1 in I:
        for i2 in I:
            if i1 != i2:
                for j in J:
                    model.addConstr(x[i1][j] + x[i2][j] <= 2 - w[i1][i2])

    # Add constraints (11)
    for i1 in I:
        for i2 in I:
            if i1 != i2:
                for s in S:
                    model.addConstr(y[i1][s] + y[i2][s] <= 2 - w[i1][i2])

    # Add constraints (12)
    for j1 in J:
        for j2 in J:
            if j1 != j2:
                expr_j1 = gp.LinExpr()
                expr_j2 = gp.LinExpr()
                for i in I:
                    expr_j1 = expr_j1 + x[i][j1]
                    expr_j2 = expr_j2 + x[i][j2]
                model.addConstr(f[j1][j2] >= expr_j1 - expr_j2)

    # Add constraints (13)
    expr = gp.LinExpr()
    for i in I:
        for j in JIX[i]:
            expr = expr + 1 - x[i][j]
        for j in nJIX[i]:
            expr = expr + x[i][j]
    model.addConstr(g >= expr)

    # Solve the model
    model.optimize()

    # Get the result and return it
    result = []
    for i in I:
        schedule = {}
        schedule['work'] = i
        schedule['room'] = [s for s in S if y[i][s].X > 0.5][0]
        schedule['datetime'] = [h for h in H if z[i][h].X > 0.5][0]
        schedule['evaluators'] = [j for j in J if x[i][j].X > 0.5]
        result.append(schedule)
    
    return result
