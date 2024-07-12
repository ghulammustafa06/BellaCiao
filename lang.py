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

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type):
        token_type, token_value = self.tokens[self.pos]
        if token_type == expected_type:
            self.pos += 1
            return token_value
        else:
            raise RuntimeError(f'Expected {expected_type} but got {token_type}')

    def factor(self):
        token_type, token_value = self.tokens[self.pos]
        if token_type == 'NUMBER':
            self.consume('NUMBER')
            return Num(token_value)
        elif token_type == 'ID':
            self.consume('ID')
            return Var(token_value)
        else:
            raise RuntimeError('Unexpected token: {}'.format(token_type))

    def term(self):
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'OP' and self.tokens[self.pos][1] in '*/':
            op = self.consume('OP')
            node = BinOp(left=node, op=op, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'OP' and self.tokens[self.pos][1] in '+-':
            op = self.consume('OP')
            node = BinOp(left=node, op=op, right=self.term())
        return node

    def assignment(self):
        name = self.consume('ID')
        self.consume('ASSIGN')
        value = self.expr()
        return Assign(name, value)

    def parse(self):
        node = self.assignment()
        self.consume('END')
        return node
