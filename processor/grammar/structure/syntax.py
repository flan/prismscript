"""
structure.syntax
================
Purpose
-------
Collects all of the syntactic relationship rules for the language, as well as the directives used
to marshall them into Python structures.

In linguistic terms, this expresses the grammatical relationship between elements, giving syntactic
saliance, but with no semblance of high-level semantics. (It can tell you which things are nouns,
but not what the nouns represent)

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
import ply.yacc

from .closed_lexicon import tokens

#Type definitions
STMT_GOTO = 10
STMT_RETURN = 11
STMT_EXIT = 12
STMT_BREAK = 13
STMT_CONTINUE = 14
COND_IF = 20
COND_ELIF = 21
COND_ELSE = 22
COND_WHILE = 23
TERM_IDENTIFIER_LOCAL = 30
TERM_IDENTIFIER_SCOPED = 31
TERM_NONE = 32
TERM_BOOL = 33
TERM_STRING = 34
TERM_INTEGER = 35
TERM_FLOAT = 36
TERM_IDENTIFIER_LOCAL_LOCAL = 39
TERM_IDENTIFIER_LOCAL_GLOBAL = 1030
SEQUENCE = 40
TEST_EQUALITY = 50
TEST_INEQUALITY = 51
TEST_GREATER_EQUAL = 52
TEST_GREATER = 53
TEST_LESSER_EQUAL = 54
TEST_LESSER = 55
TEST_BOOL_OR = 56
TEST_BOOL_AND = 57
MATH_MULTIPLY = 70
MATH_DIVIDE = 71
MATH_DIVIDE_INTEGER = 72
MATH_ADD = 73
MATH_SUBTRACT = 74
MATH_AND = 75
MATH_OR = 76
MATH_XOR = 79
MATH_MOD = 1070
FUNCTIONCALL_LOCAL = 80
FUNCTIONCALL_SCOPED = 81
FUNCTIONCALL_UNDEFINED = 82
ASSIGN = 90
ASSIGN_ADD = 91
ASSIGN_SUBTRACT = 92
ASSIGN_MULTIPLY = 93
ASSIGN_DIVIDE = 94
ASSIGN_DIVIDE_INTEGER = 95
ASSIGN_SEQUENCE = 96
ASSIGN_MOD = 97

precedence = (
 ('right',
   'EQUALITY', 'INEQUALITY', 'GREATER_EQUAL', 'GREATER', 'LESSER_EQUAL', 'LESSER',
   'AND', 'OR', 'XOR',
 ),
 ('left', 'ADD', 'SUBTRACT',),
 ('left', 'MULTIPLY', 'DIVIDE', 'DIVIDE_INTEGER', 'MOD',),
 ('left', 'BOOL_OR', 'BOOL_AND',),
)

start = 'nodelist'

def p_empty(p):
    r"""
    empty :
    """
    
def p_nodeset(p):
    r"""
    nodelist : nodelist node
             | nodelist function
             | empty
    """
    if p[1] is None:
        p[0] = ({}, {})
    else:
        p[0] = p[1]
        p[1][0].update(p[2][0])
        p[1][1].update(p[2][1])
        
def p_node(p):
    r"""
    node : IDENTIFIER_LOCAL LCURLY expressionlist RCURLY
    """
    p[0] = ({p[1]: p[3]}, {})

def p_function(p):
    r"""
    function : IDENTIFIER_LOCAL LPAREN parameterset RPAREN LCURLY expressionlist RCURLY
    """
    p[0] = ({}, {(p[1], frozenset(p[3])): p[6]})

def p_parameterset(p):
    r"""
    parameterset : IDENTIFIER_LOCAL COMMA parameterset
                 | IDENTIFIER_LOCAL
                 | empty
    """
    if p[1] is None:
        p[0] = set()
    else:
        p[0] = set((p[1],))
        if len(p) == 4:
            p[0].update(p[3])
            
def p_argumentset(p):
    r"""
    argumentset : IDENTIFIER_LOCAL ASSIGN expression COMMA argumentset
                | IDENTIFIER_LOCAL ASSIGN expression
                | empty
    """
    if p[1] is None:
        p[0] = {}
    else:
        p[0] = {p[1]: p[3]}
        if len(p) == 6:
            p[0].update(p[5])
            
def p_expressionlist(p):
    r"""
    expressionlist : expressionlist conditional
                   | expressionlist while
                   | expressionlist assignment SEMICOLON
                   | expressionlist statement SEMICOLON
                   | expressionlist expression SEMICOLON
                   | empty
    """
    if p[1] is None:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]
        
def p_conditional(p):
    r"""
    conditional : IF LPAREN expression RPAREN LCURLY expressionlist RCURLY conditionalalternate conditionalterminal
    """
    p[0] = [COND_IF, (p[3], p[6])] + p[8] + p[9]
    
def p_conditionalalternate(p):
    r"""
    conditionalalternate : conditionalalternate ELIF LPAREN expression RPAREN LCURLY expressionlist RCURLY
                         | empty
    """
    if p[1] is None:
        p[0] = []
    else:
        p[0] = p[1] + [(COND_ELIF, p[4], p[7])]
        
def p_conditionalterminal(p):
    r"""
    conditionalterminal : ELSE LCURLY expressionlist RCURLY
                        | empty
    """
    if p[1] is None:
        p[0] = []
    else:
        p[0] = [(COND_ELSE, p[3])]

def p_while(p):
    r"""
    while : WHILE LPAREN expression RPAREN LCURLY expressionlist RCURLY
    """
    p[0] = (COND_WHILE, p[3], p[6])
    
def p_assignment(p):
    r"""
    assignment : identifier_local ASSIGN expression
    """
    p[0] = (ASSIGN, p[1], p[3])
def p_assignment_augmented(p):
    r"""
    assignment : identifier_local ASSIGN_ADD expression
               | identifier_local ASSIGN_SUBTRACT expression
               | identifier_local ASSIGN_MULTIPLY expression
               | identifier_local ASSIGN_DIVIDE expression
               | identifier_local ASSIGN_DIVIDE_INTEGER expression
               | identifier_local ASSIGN_MOD expression
    """
    if p[2] == '+=':
        p[0] = (ASSIGN_ADD, p[1], p[3])
    elif p[2] == '-=':
        p[0] = (ASSIGN_SUBTRACT, p[1], p[3])
    elif p[2] == '*=':
        p[0] = (ASSIGN_MULTIPLY, p[1], p[3])
    elif p[2] == '/=':
        p[0] = (ASSIGN_DIVIDE, p[1], p[3])
    elif p[2] == '\=':
        p[0] = (ASSIGN_DIVIDE_INTEGER, p[1], p[3])
    elif p[2] == '%=':
        p[0] = (ASSIGN_MOD, p[1], p[3])
def p_assignment_sequence(p):
    r"""
    assignment : sequence ASSIGN expression
    """
    p[0] = (ASSIGN_SEQUENCE, p[1], p[3])
    
def p_statement_goto(p):
    r"""
    statement : STMT_GOTO IDENTIFIER_LOCAL
    """
    p[0] = (STMT_GOTO, p[2])
def p_statement_return(p):
    r"""
    statement : STMT_RETURN expression
              | STMT_RETURN
    """
    if p[1] is None:
        p[0] = (STMT_RETURN, (TERM_NONE, None))
    else:
        p[0] = (STMT_RETURN, p[2])
def p_statement_exit(p):
    r"""
    statement : STMT_EXIT expression
              | STMT_EXIT
    """
    if len(p) == 2:
        p[0] = (STMT_EXIT, (TERM_STRING, ''))
    elif len(p) == 3:
        p[0] = (STMT_EXIT, p[2])
def p_statement_break(p):
    r"""
    statement : STMT_BREAK
    """
    p[0] = (STMT_BREAK,)
def p_statement_continue(p):
    r"""
    statement : STMT_CONTINUE
    """
    p[0] = (STMT_CONTINUE,)

def p_expression(p):
    r"""
    expression : LPAREN expression RPAREN
               | sequence
               | functioncall
               | term
    """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]
def p_expression_math(p):
    r"""
    expression : expression MULTIPLY expression
               | expression DIVIDE_INTEGER expression
               | expression DIVIDE expression
               | expression SUBTRACT expression
               | expression ADD expression
               | expression MOD expression
               | expression AND expression
               | expression OR expression
               | expression XOR expression
    """
    if p[2] == '+':
        p[0] = (MATH_ADD, p[1], p[3])
    elif p[2] == '-':
        p[0] = (MATH_SUBTRACT, p[1], p[3])
    elif p[2] == '*':
        p[0] = (MATH_MULTIPLY, p[1], p[3])
    elif p[2] == '/':
        p[0] = (MATH_DIVIDE, p[1], p[3])
    elif p[2] == '\\':
        p[0] = (MATH_DIVIDE_INTEGER, p[1], p[3])
    elif p[2] == '%':
        p[0] = (MATH_MOD, p[1], p[3])
    elif p[2] == 'and':
        p[0] = (MATH_AND, p[1], p[3])
    elif p[2] == 'or':
        p[0] = (MATH_OR, p[1], p[3])
    elif p[2] == 'xor':
        p[0] = (MATH_XOR, p[1], p[3])
def p_expression_test(p):
    r"""
    expression : expression EQUALITY expression
               | expression INEQUALITY expression
               | expression GREATER_EQUAL expression
               | expression GREATER expression
               | expression LESSER_EQUAL expression
               | expression LESSER expression
               | expression BOOL_OR expression
               | expression BOOL_AND expression
    """
    if p[2] == '==':
        p[0] = (TEST_EQUALITY, p[1], p[3])
    elif p[2] == '!=':
        p[0] = (TEST_INEQUALITY, p[1], p[3])
    elif p[2] == '>=':
        p[0] = (TEST_GREATER_EQUAL, p[1], p[3])
    elif p[2] == '>':
        p[0] = (TEST_GREATER, p[1], p[3])
    elif p[2] == '<=':
        p[0] = (TEST_LESSER_EQUAL, p[1], p[3])
    elif p[2] == '<':
        p[0] = (TEST_LESSER, p[1], p[3])
    elif p[2] == '||':
        p[0] = (TEST_BOOL_OR, p[1], p[3])
    elif p[2] == '&&':
        p[0] = (TEST_BOOL_AND, p[1], p[3])
        
def p_sequence(p):
    r"""
    sequence : LSQUARE expressionsequence RSQUARE
    """
    p[0] = (SEQUENCE, p[2])

def p_expressionsequence(p):
    r"""
    expressionsequence : expression COMMA expressionsequence
                       | expression
                       | empty
    """
    if p[1] is None:
        p[0] = []
    else:
        p[0] = [p[1]]
        if len(p) == 4:
            p[0] += p[3]
            
def p_functioncall_scoped(p):
    r"""
    functioncall : IDENTIFIER_SCOPED LPAREN argumentset RPAREN
    """
    p[0] = (FUNCTIONCALL_SCOPED, p[1], p[3])
def p_functioncall_local(p):
    r"""
    functioncall : IDENTIFIER_LOCAL LPAREN argumentset RPAREN
    """
    p[0] = (FUNCTIONCALL_LOCAL, p[1], p[3])

def p_term(p):
    r"""
    term : STRING
         | INTEGER
         | FLOAT
    """
    if isinstance(p[1], str):
        p[0] = (TERM_STRING, p[1])
    elif type(p[1]) == int:
        p[0] = (TERM_INTEGER, p[1])
    elif type(p[1]) == float:
        p[0] = (TERM_FLOAT, p[1])
def p_term_special(p):
    r"""
    term : NONE
         | TRUE
         | FALSE
    """
    if p[1] == 'None':
        p[0] = (TERM_NONE, None)
    elif p[1] == 'True':
        p[0] = (TERM_BOOL, True)
    elif p[1] == 'False':
        p[0] = (TERM_BOOL, False)
def p_term_identifier_scoped(p):
    r"""
    term : IDENTIFIER_SCOPED
    """
    p[0] = (TERM_IDENTIFIER_SCOPED, p[1])
def p_term_identifier_local(p):
    r"""
    term : identifier_local
    """
    p[0] = p[1]
    
def p_identifier_local(p):
    r"""
    identifier_local : IDENTIFIER_LOCAL
                     | QUALIFIER_LOCAL IDENTIFIER_LOCAL
                     | QUALIFIER_GLOBAL IDENTIFIER_LOCAL
    """
    if len(p) == 2:
        p[0] = (TERM_IDENTIFIER_LOCAL, p[1])
    elif p[1] == 'local':
        p[0] = (TERM_IDENTIFIER_LOCAL_LOCAL, p[2])
    elif p[1] == 'global':
        p[0] = (TERM_IDENTIFIER_LOCAL_GLOBAL, p[2])
        
def p_error(t):
    if t:
        raise ValueError("Syntax error; offending token on line %(line)i: %(token)s" % {
         'line': t.lineno,
         'token': repr(t.value),
        })
    else:
        raise ValueError("Unexpectedly reached end of file")
        
parser = ply.yacc.yacc()

