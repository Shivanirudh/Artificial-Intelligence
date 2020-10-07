import random

class Clause():
    def __init__(self, no_literals, literals):
        self.no_literals = no_literals
        self.literals = [i for i in literals]
        self.values = dict()
        for i in self.literals:
            self.values[i] = None
    
    def __str__(self):
        clause = "{ "
        for i in range(0, self.no_literals):
            clause += (self.literals[i] + " ")
            if i != self.no_literals - 1:
                clause += ", "
        clause += "}"
        return clause
    
    def assign(self, model):
        i = 0
        while i < self.no_literals:
            symbol = self.literals[i][:2]
            if symbol in model.keys():
                val = model[symbol]
            else:
                i += 1
                continue
            if self.literals[i][-1] == "'":
                val = not val
            self.values[self.literals[i]] = val 
            i += 1
            
    def evaluate(self, model):
        self.assign(model)
        result = False
        for j in self.values.values():
            if j == True:
                return True
            if j == None:
                return None
        for j in self.values.values():
            result = result or j
        return result

class Formula():
    def __init__(self, no_clauses, clauses):
        self.no_clauses = no_clauses
        self.clauses = [i for i in clauses]
    
    def __str__(self):
        formula = "{ "
        for i in range(0, self.no_clauses):
            formula += (str(self.clauses[i]) + " ")
            if i != self.no_clauses - 1:
                formula += ", "
        formula += "}"
        return formula

def generate_clause():
    literals = []
    no_literals = random.randint(1, 5)
    base_var = "A"
    i = 0
    while i < no_literals:
        var_no = random.randint(1, 5)
        var_name = base_var+str(var_no)
        var_complement = random.randint(0, 1)
        if var_complement == 1:
            var_name += "'"
        if var_name in literals:
            i -= 1
        else:
            literals.append(var_name)
        i+=1
    clause = Clause(no_literals, literals)
    return clause

def generate_formula():
    clauses = []
    no_clauses = random.randint(1, 10)
    i = 0
    while i < no_clauses:
        clause = generate_clause()
        if clause in clauses:
            i -= 1
        else:
            clauses.append(clause)
        i += 1
    formula = Formula(no_clauses, clauses)
    return formula

def generate_parameters(formula):
    clauses = formula.clauses
    symbols = []
    for clause in formula.clauses:
        for literal in clause.literals:
            symbol = literal[:2]
            if symbol not in symbols:
                symbols.append(symbol)
    return clauses, symbols

def generate_model(symbols):
    assignment = dict()
    for i in range(len(symbols)):
        val = random.randint(0, 1)
        x = True if val == 1 else False
        assignment[symbols[i]] = x
    return assignment

def find_pure_symbols(clauses, symbols, model):
    pure = []
    assn = dict()
    literals = []
    
    for clause in clauses:
        if clause.evaluate(model) == True:
            continue
        for l in clause.literals:
            literals.append(l)
    for s in symbols:
        sym = (s + "'")
        if (s in literals and sym not in literals) or (s not in literals and sym in literals):
            pure.append(s)
    for i in pure:
        assn[i] = None
    for s in pure:
        for clause in clauses:
            tmp_model = model
            if s in clause.literals:
                symbol = s[:2]
                tmp_model[symbol] = True
                clause_result = clause.evaluate(tmp_model)
                if clause_result == True:
                    assn[symbol] = True
                else:
                    tmp_model[symbol] = False
                    clause_result = clause.evaluate(tmp_model)
                    if clause_result == True:
                        assn[symbol] = False
    return pure, assn

def find_unit_clauses(clauses, model):
    unit = []
    for clause in clauses:
        if clause.no_literals == 1:
            unit.append(clause.literals[0][:2])
        else:
            Fcount, Ncount = 0, 0
            for l,v in clause.values.items():
                if v == False:
                    Fcount += 1
                elif v == None:
                    sym = l[:2]
                    Ncount += 1
            if Fcount == clause.no_literals - 1 and Ncount == 1:
                unit.append(sym)
    assn = dict()
    for i in unit:
        assn[i] = True

    return unit, assn
    
def DPLL(clauses, symbols, model):
    
    #If every clause in clauses is True, return True
    #If some clause in clauses is False, return False
    check_clause_all_true = True
    for clause in clauses:
        clause_check = clause.evaluate(model)
        if clause_check == False:
            return False, None
        elif clause_check == None:
            check_clause_all_true = False
            continue

    if check_clause_all_true:
        return True, model
    
    #Find pure symbols
    pure, assn = find_pure_symbols(clauses, symbols, model)
    P = None
    if len(pure) > 0:
        P, value = pure[0], assn[pure[0]]
    
    if P:
        tmp_model = model
        tmp_model[P]=value
        tmp_symbols = [i for i in symbols]
        if P in tmp_symbols:
            tmp_symbols.remove(P)
        return DPLL(clauses, tmp_symbols, tmp_model)
    
    #Find unit symbols
    unit, assn =  find_unit_clauses(clauses, model)
    P = None
    if len(unit) > 0:
        P, value = unit[0], assn[unit[0]]
    if P:
        tmp_model = model
        tmp_model[P]=value
        tmp_symbols = [i for i in symbols]
        if P in tmp_symbols:
            tmp_symbols.remove(P)
        return DPLL(clauses, tmp_symbols, tmp_model)
    P = symbols[0]
    rest = symbols[1:]
    tmp1, tmp2 = model, model
    tmp1[P], tmp2[P] = True, False

    return DPLL(clauses, rest, tmp1) or DPLL(clauses, rest, tmp2)
    
formula = generate_formula()
print(formula)

clauses, symbols = generate_parameters(formula)

solution, model = DPLL(clauses, symbols, {})

if solution:
    print(model)
else:
    print("Not satisfiable")

'''
Output:

{ { A4 , A3 , A5' , A1 , A3' } , { A4 } , { A3 } }
{'A4': True, 'A1': True, 'A3': True}
{'A4': True, 'A1': True, 'A3': True}


{ { A4 , A5' } , { A5 , A1 , A2 } , { A3 , A4 , A4' } }
{'A1': None, 'A2': True, 'A3': True, 'A4': True, 'A5': True}


{ { A3' , A1' , A5 , A4 } , { A4' } , { A1 , A5' } , { A1 } , { A3' , A1 , A4' } , { A1 , A1' , A3' } , { A5' , A3' } }
Not satisfiable
'''