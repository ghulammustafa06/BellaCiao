# lang.py

import re

# Lexer
token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),
    ('ASSIGN',   r'='),
    ('END',      r';'),
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
    ('OP',       r'[+\-*/]'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('PRINT',    r'print'),
    ('HEIST',    r'heist'),
    ('PLAN',     r'plan'),
    ('EXECUTE',  r'execute'),
    ('STRING',   r'"[^"]*"'),
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
        elif kind == 'STRING':
            value = value[1:-1]  # Remove quotes
        elif kind in ['SKIP', 'NEWLINE']:
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value} unexpected')
        tokens.append((kind, value))
    return tokens

# AST Nodes
class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, value):
        self.value = value

class String(AST):
    def __init__(self, value):
        self.value = value

class Assign(AST):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Var(AST):
    def __init__(self, name):
        self.name = name

class Print(AST):
    def __init__(self, expr):
        self.expr = expr

class Heist(AST):
    def __init__(self, name, plan):
        self.name = name
        self.plan = plan

class Plan(AST):
    def __init__(self):
        self.steps = []

class Execute(AST):
    def __init__(self, name):
        self.name = name

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type):
        if self.pos < len(self.tokens):
            token_type, token_value = self.tokens[self.pos]
            if token_type == expected_type:
                self.pos += 1
                return token_value
        raise RuntimeError(f'Expected {expected_type}')

    def factor(self):
        token_type, token_value = self.tokens[self.pos]
        if token_type == 'NUMBER':
            self.consume('NUMBER')
            return Num(token_value)
        elif token_type == 'STRING':
            self.consume('STRING')
            return String(token_value)
        elif token_type == 'ID':
            self.consume('ID')
            return Var(token_value)
        elif token_type == 'LPAREN':
            self.consume('LPAREN')
            node = self.expr()
            self.consume('RPAREN')
            return node
        else:
            raise RuntimeError(f'Unexpected token: {token_type}')

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
        statements = []
        while self.pos < len(self.tokens):
            statements.append(self.statement())
            if self.pos < len(self.tokens):
                self.consume('END')
        return statements

# Interpreter
class Interpreter:
    def __init__(self):
        self.env = {}
        self.heists = {}

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise RuntimeError(f'No visit_{type(node).__name__} method')

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right

    def visit_Num(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Assign(self, node):
        value = self.visit(node.value)
        self.env[node.name] = value
        return value

    def visit_Var(self, node):
        if node.name in self.env:
            return self.env[node.name]
        raise RuntimeError(f'Variable {node.name} not found')

    def visit_Print(self, node):
        value = self.visit(node.expr)
        print(value)
        return value

    def visit_Heist(self, node):
        self.heists[node.name] = node.plan
        return f"Heist '{node.name}' planned"

    def visit_Plan(self, node):
        results = []
        for step in node.steps:
            results.append(self.visit(step))
        return results

    def visit_Execute(self, node):
        if node.name in self.heists:
            plan = self.heists[node.name]
            return self.visit(plan)
        raise RuntimeError(f"Heist '{node.name}' not found")

    def interpret(self, nodes):
        results = []
        for node in nodes:
            results.append(self.visit(node))
        return results

