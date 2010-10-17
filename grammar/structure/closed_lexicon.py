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

:Version: 1.0.0 : Oct. 17, 2010

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
 #states
 'None': 'NONE', #This language's has-no-value keyword
 #literals
 'True': 'TRUE',
 'False': 'FALSE',
 #operands
 'and': 'AND',
 'or': 'OR',
 'nand': 'NAND',
 'nor': 'NOR',
 'xor': 'XOR',
 #functions
 '__undefined': 'UNDEFINED', #__undefined(x) : true if x is not a resolvable identifier
 #statements
 'goto': 'STMT_GOTO', #goto IDENTIFIER_LOCAL;
 'return': 'STMT_RETURN', #return 5 == 4;
 'exit': 'STMT_EXIT', #exit [1, 2, 5]; | exit "hello"; #Packs a string representation of the exit value (sequences are null-delimited) into a returned string; exit with no value or an implied kill will return the empty string
 #Things like int(), round(), and other common functions will be part of the 'language' namespace
}

tokens = [
 'IDENTIFIER_SCOPED', #hello.lawlwhut
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
 #assignments
 'ASSIGN',
 'ASSIGN_ADD',
 'ASSIGN_SUBTRACT',
 'ASSIGN_MULTIPLY',
 'ASSIGN_DIVIDE',
 'ASSIGN_DIVIDE_INTEGER',
 #operands
 'MULTIPLY',
 'DIVIDE',
 'DIVIDE_INTEGER',
 'ADD',
 'SUBTRACT',
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

#Token mapping
def t_IDENTIFIER_SCOPED(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)+'
    t.type = reserved.get(t.value, 'IDENTIFIER_SCOPED')
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

t_ASSIGN = r'='
t_ASSIGN_ADD = r'\+='
t_ASSIGN_SUBTRACT = r'\-='
t_ASSIGN_MULTIPLY = r'\*='
t_ASSIGN_DIVIDE = r'/='
t_ASSIGN_DIVIDE_INTEGER = r'\\='

t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_DIVIDE_INTEGER = r'\\'
t_ADD = r'\+'
t_SUBTRACT = r'\-'

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
t_ignore_semicolon = ';'
t_ignore_comment = r'(?:\#|//).*'

def t_error(t):
    raise ValueError("Illegal character on line %(line)i: '%(character)s'" % {
     'line': t.lexer.lineno,
     'character': t.value[0],
    })
    
#Digest functional categories
lexer = ply.lex.lex()

