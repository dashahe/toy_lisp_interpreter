# 2018-02-02
# by xvvx

from environment import Environment
from procedure import Procedure


###############################################################################
#parser   
              
def tokenizer(chars: str) -> list:
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse_tokens(tokens: list, inner: bool) -> list:
    res = []
    while len(tokens) > 0:
        current = tokens.pop(0)
        if current == '(':
            res.append(parse_tokens(tokens, True))
        elif current == ')':
            if inner: return res
            else: IOError("unmatched close paren %s" % current)
        else:
            res.append(current)
        
    if inner: IOError("unmatched open paren %s" % current)
    else: return res       

def parser(chars: str) -> list:
    return parse_tokens(tokenizer(chars), False)

###############################################################################


#evaluator
def meval(expr, env):
    if is_primitive(expr):
        return eval_primitive(expr)
    elif is_if(expr):
        return eval_if(expr)
    elif is_definition(expr):
        return eval_definition(expr, env)
    elif is_name(expr):
        return eval_name(expr, env)
    elif is_lambda(expr):
        return eval_lambda(expr, env)
    elif is_application(expr):
        return eval_application(expr, env)
    else:
        TypeError("Unexpected expression type: %s" % str(expr))

def is_primitive(expr) -> bool:
    return is_number(expr) or is_primitive_procedure(expr)

def is_number(expr) -> bool:
    return isinstance(expr, str) and expr.isdigit()

def is_primitive_procedure(expr) -> bool:
    return callable(expr)

def eval_primitive(expr):
    if is_number(expr): return int(expr)
    else: return expr

"""
primitive procedures
"""
def check_operands(operands: list, num: int, prim: str):
    if len(operands) != num: 
       print("Error: Primitive %s expected %s operands, given %s: %s" %
         (prim,num,len(operands),str(operands)))

#implementation of primitive procedure: + 
def primitive_plus(operands: list):
    if len(operands) == 0: return 0
    else: return operands[0] + primitive_plus(operands[1:])

#implementation of primitive procedure: -
def primitive_minus(operands: list):
    if len(operands) == 1:  return -1 * operands[0]
    elif len(operands) == 2: return operands[0] - operands[1]
    else: raise Exception("− expects 1 or 2 operands, given %s: %s" %
                len(operands), str(operands))

#implementation of primitive procedure: *
def primitive_times(operands: list):
    if len(operands) == 0: return 1
    else: return operands[0] * primitive_times(operands[1:])

#implementation of primitive procedure: =
def primitive_equal(operands: list):
    check_operands(operands, 2, "=")
    return operands[0] == operands[1]

#implementation of primitive procedure: <
def primitive_less(operands: list):
    check_operands(operands, 2, "<")
    return operands[0] < operands[1]

"""
if statement
"""
# judge whether expr is a special form(if statement, and others)
def is_special_form(expr: list, keywords: str) -> bool:
    return isinstance(expr, list) and len(expr) > 0 and expr[0] == keywords

# judge whether expr is "if" statement
def is_if(expr: list) -> bool:
    return is_special_form(expr, "if")

# if-statement: if a b c. (if a if true, return b. else, return c)
def eval_if(expr: list, env: Environment):
    if meval(expr[1], env): return meval(expr[2], env)
    else: return meval(expr[3], env)


"""
definition and names
"""
def is_definition(expr: list) -> bool:
    return is_special_form(expr, "define")

def eval_definition(expr: list, env: Environment):
    name = expr[1]
    value = meval(expr[2], env)
    if is_number(value): value = int(value)
    env.add_variable(name, value)

def is_name(expr) -> bool:
    return isinstance(expr, str)

def eval_name(expr, env):
    return env.get_variable(expr)

"""
procedures
"""
def is_lambda(expr):
    return is_special_form(expr, "lambda")

def eval_lambda(expr, env):
    return Procedure(expr[1], expr[2], env)

"""
application
"""
def is_application(expr):
    return isinstance(expr, list)

def eval_application(expr, env):
    subexprs = expr
    subexpr_vals = list(map(lambda sexpr: meval(sexpr, env), subexprs))
    #evaluate all sub expressions
    return mapply(subexpr_vals[0], subexpr_vals[1:], env)

def mapply(procedure, operands, env):
    if is_primitive(procedure): 
        for i in range(len(operands)):
            if env.get_variable(operands[i]) != False:
                operands[i] = env.get_variable(operands[i])
        return procedure(operands)
    elif isinstance(procedure, Procedure):
        params = procedure.get_params()
        new_env = Environment(procedure.get_environment())
        if len(params) != len(operands):
            print("Error: Parameter length mismatch: %s given operands %s" 
                % (str(proc),str(operands)))
        for (name, operand) in zip(params, operands):
            new_env.add_variable(name, operand)
        return meval(procedure.get_body(), new_env)
    else:
        print("Error: Unexpected procedure: %s" % (procedure))


"""
evaluate loop
"""
def run():
    env = Environment(None)
    env.add_variable('true', True)
    env.add_variable('false', False)
    env.add_variable('+', primitive_plus)
    env.add_variable('-', primitive_minus)
    env.add_variable('*', primitive_times)
    env.add_variable('=', primitive_equal)
    env.add_variable('<', primitive_less)
    while True:
        input_code = input("Tiny Lisp> ")
        if input_code == "quit": break
        for each_expr in parser(input_code):
            print (str(meval(each_expr, env)))


###############################################################################
if __name__ == '__main__':
    run()