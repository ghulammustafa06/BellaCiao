# lang.py

import re

# ----------------------- Lexer ----------------------

token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),
    ('ASSIGN',   r'='),
    ('END',      r';'),
    ('ID',       r'[A-Za-z]+'),
    ('OP',       r'[+\-*/]'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.'),
]

token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

def lex(code):
    tokens = []
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'SKIP' or kind == 'NEWLINE':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value} unexpected')
        tokens.append((kind, value))
    return tokens

# Abstract Syntax Tree (AST) Nodes
class AST:
    pass
class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left  
        self.op = op      
        self.right = right 

class Num(AST):
    def __init__(self, value):
        self.value = value  #

class Assign(AST):
    def __init__(self, name, value):
        self.name = name    
        self.value = value 

class Var(AST):
    def __init__(self, name):
        self.name = name  

class UnaryOp(AST):
    def __init__(self, op, operand):
        self.op = op         
        self.operand = operand 

class Compound(AST):
    def __init__(self):
        self.children = []  

class NoOp(AST):
    pass

class Print(AST):
    def __init__(self, expr):
        self.expr = expr  


assignment = Assign(
    name=Var(name='x'), 
    value=BinOp(left=Num(value=7), op='+', right=Num(value=3))
)

var = Var(name='x')

print_stmt = Print(expr=var)
compound = Compound()
compound.children.append(assignment)
compound.children.append(print_stmt)
