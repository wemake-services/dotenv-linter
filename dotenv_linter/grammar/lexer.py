# -*- coding: utf-8 -*-

from ply import lex

# List of token names.   This is always required
tokens = (
    'COMMENT',
    'NAME',
    'EQUAL',
    'VALUE',
)

states = (
    ('comment', 'exclusive'),
    ('def', 'exclusive'),
    ('value', 'exclusive'),
)

def t_begin_comment(t):
    r'\#'
    t.lexer.push_state('comment')


def t_begin_def(t):
    r'\w'
    t.lexer._def_start = t.value
    t.lexer.push_state('def')


def t_def_NAME(t):
    r'\w+'
    t.value = t.lexer._def_start + t.value
    t.lexer._def_start = ''
    return t


def t_def_EQUAL(t):
    r'='
    t.lexer.push_state('value')
    return t


def t_value_VALUE(t):
    r'.+'
    t.lexer.pop_state()
    return t


def t_comment_COMMENT(t):
    r'.+'
    t.value = '#' + t.value
    t.lexer.pop_state()
    return t

# Define a rule so we can track line numbers
def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.begin('INITIAL')

# A string containing ignored characters (spaces and tabs)
# t_ANY_ignore  = ' \t'

# Error handling rule
def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


data = '''
# Comment line
KEY=1#=a

OTHER=
last
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
