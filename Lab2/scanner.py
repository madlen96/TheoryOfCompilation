import sys
import ply.lex as lex

tokens = ['DOTPLUS', 'DOTMINUS', 'DOTTIMES', 'DOTDIVIDE', 'PLUSASSIGNMENT',
          'MINUSASSIGNMENT', 'TIMESASSIGNMENT', 'DIVIDEASSIGNMENT', 'LESSEQUAL',
          'GREATEREQUAL', 'UNEQUAL', 'EQUAL', 'FLOAT', 'INT', 'ID']

literals = ['+', '-', '*', '/', '(', ')', '=', ';', '[', ']', '{', '}', ':', '<', '>', ',', '\'', '"']

t_DOTPLUS = r'\.\+'
t_DOTMINUS = r'\.-'
t_DOTTIMES = r'\.\*'
t_DOTDIVIDE = r'\.\/'
t_PLUSASSIGNMENT = r'\+='
t_MINUSASSIGNMENT = r'-='
t_TIMESASSIGNMENT = r'\*='
t_DIVIDEASSIGNMENT = r'\/='
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_UNEQUAL = r'!='
t_EQUAL = r'=='

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'print': 'PRINT',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN'
}

tokens.extend(reserved.values())


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # check for reserved words
    return t


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = '  \t'


# ignore comments
def t_COMMENT(t):
    r'\#.*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


# if __name__ == '__main__':
#     try:
#         filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
#         file = open(filename, "r")
#     except IOError:
#         print("Cannot open {0} file".format(filename))
#         sys.exit(0)
#
#     text = file.read()
#     lexer = lex.lex()
#
#     lexer.input(text)
#     for token in lexer:
#         print("line %d: %s(%s)" % (token.lineno, token.type, token.value))
lexer = lex.lex()
