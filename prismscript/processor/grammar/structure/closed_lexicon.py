"""
structure.closed_lexicon
========================
Purpose
-------
Collects all of the lexing rules required for the language.

In linguistic terms, this forms the basis of the language's phonology and provides its closed
lexical categories, like determiners and propositions.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.1 : Mar. 06, 2011

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import ply.lex

reserved = {
 #conditionals
 'if': 'IF',
 'elif': 'ELIF',
 'else': 'ELSE',
 'while': 'WHILE',
 'for': 'FOR',
 #states
 'None': 'NONE',
 #literals
 'True': 'TRUE',
 'False': 'FALSE',
 #statements
 'goto': 'STMT_GOTO',
 'return': 'STMT_RETURN',
 'exit': 'STMT_EXIT',
 'break': 'STMT_BREAK',
 'continue': 'STMT_CONTINUE',
 #qualifiers
 'global': 'QUALIFIER_GLOBAL',
 'local': 'QUALIFIER_LOCAL',
 #meta
 'in': 'IN',
}

tokens = [
 'IDENTIFIER_SCOPED', #hello.lawlwhut
 'IDENTIFIER_SUFFIX', #.whee : any suffix off of a term or function-call
 'IDENTIFIER_LOCAL', #lawlwhut : note the lack of a dot
 #literals
 'STRING',
 'FLOAT',
 'INTEGER',
 #tests
 'EQUALITY',
 'INEQUALITY',
 'GREATER_EQUAL',
 'GREATER',
 'LESSER_EQUAL',
 'LESSER',
 'BOOL_AND',
 'BOOL_OR',
 'NEGATE',
 #assignments
 'ASSIGN',
 'ASSIGN_ADD',
 'ASSIGN_SUBTRACT',
 'ASSIGN_EXPONENTIATE',
 'ASSIGN_MULTIPLY',
 'ASSIGN_DIVIDE',
 'ASSIGN_DIVIDE_INTEGER',
 'ASSIGN_MOD',
 #operands
 'EXPONENTIATE',
 'MULTIPLY',
 'DIVIDE',
 'DIVIDE_INTEGER',
 'ADD',
 'SUBTRACT',
 'MOD',
 #delimiters
 'LPAREN',
 'RPAREN',
 'LCURLY',
 'RCURLY',
 'LSQUARE',
 'RSQUARE',
 'COMMA',
 'SEMICOLON',
] + list(reserved.values())


#Token-mapping
##############
def t_IDENTIFIER_SCOPED(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)+'
    t.type = reserved.get(t.value, 'IDENTIFIER_SCOPED')
    return t
def t_IDENTIFIER_SUFFIX(t):
    r'(?:\.[a-zA-Z_][a-zA-Z0-9_]*)+'
    t.type = reserved.get(t.value, 'IDENTIFIER_SUFFIX')
    return t
def t_IDENTIFIER_LOCAL(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER_LOCAL')
    return t
    
def t_STRING(t):
    r'(?:"(?:[^"]|(?<=\\)")*"|\'(?:[^\']|(?<=\\)\')*\')'
    t.value = t.value[1:-1]
    for (escape, replacement) in (
     ('\\\\', '\\'),
     ('\\b', '\b'),
     ('\\t', '\t'),
     ('\\n', '\n'),
     ('\\a', '\a'),
     ('\\r', '\r'),
     ('\\"', '"'),
     ("\\'", "'"),
    ):
        t.value = t.value.replace(escape, replacement)
    return t
def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t
def t_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t
    
t_EQUALITY = r'=='
t_INEQUALITY = r'!='
t_GREATER_EQUAL = r'>='
t_GREATER = r'>'
t_LESSER_EQUAL = r'<='
t_LESSER = r'<'
t_BOOL_AND = r'\&\&'
t_BOOL_OR = r'\|\|'
t_NEGATE = r'!'

t_ASSIGN = r'='
t_ASSIGN_ADD = r'\+='
t_ASSIGN_SUBTRACT = r'\-='
t_ASSIGN_EXPONENTIATE = r'\^='
t_ASSIGN_MULTIPLY = r'\*='
t_ASSIGN_DIVIDE = r'/='
t_ASSIGN_DIVIDE_INTEGER = r'\\='
t_ASSIGN_MOD = r'%='

t_EXPONENTIATE = r'\^'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_DIVIDE_INTEGER = r'\\'
t_ADD = r'\+'
t_SUBTRACT = r'\-'
t_MOD = r'%'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_COMMA = r','
t_SEMICOLON = r'\;'

def t_newline(t):
    r'(?:\r\n|\n|\r)+'
    t.lexer.lineno += len(t.value) - t.value.count('\r\n')
    
t_ignore_whitespace = r'[ \t]'
t_ignore_comment = r'(?:\#|//).*'


#Error-handing
##############
def t_error(t):
    raise ValueError("Illegal character on line %(line)i: '%(character)s'" % {
     'line': t.lexer.lineno,
     'character': t.value[0],
    })

    
#Digest functional categories
#############################
lexer = ply.lex.lex()

