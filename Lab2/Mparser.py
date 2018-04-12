#!/usr/bin/python

import scanner
import classes
import ply.yacc as yacc

tokens = scanner.tokens + scanner.literals

precedence = (
    ("nonassoc", 'IF'),
    ("nonassoc", 'ELSE'),
    ("right", '=', 'PLUSASSIGNMENT', 'MINUSASSIGNMENT', 'TIMESASSIGNMENT', 'DIVIDEASSIGNMENT'),
    ('nonassoc', '<', '>', 'EQUAL', 'UNEQUAL', 'LESSEQUAL', 'GREATEREQUAL'),  # Nonassociative operators
    ("left", '+', '-'),
    ("left", '*', '/'),
    ('left', 'DOTPLUS', 'DOTMINUS'),
    ('left', 'DOTTIMES', 'DOTDIVIDE'),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""
    p[0] = classes.Program(p[1])


def p_instructions_opt(p):
    """instructions_opt : instructions """
    p[0] = classes.InstructionsOpt(p[1])


def p_instructions(p):
    """instructions : instructions instruction
                     | instruction"""
    p[0] = classes.Instructions()


def p_instruction(p):
    """instruction : if_else_instruction
                    | while_instruction
                    | for_instruction
                    | break_instruction
                    | continue_instruction
                    | return_instruction
                    | print_instruction
                    | assignment """
    p[0] = p[1]


def p_if_else_instruction(p):
    """if_else_instruction : IF '(' expression_to_bool ')' instructions
                            | IF '(' expression_to_bool ')' instructions ELSE instructions"""
    if len(p) == 6:
        p[0] = classes.IfElseInstruction(p[3], p[5])
    elif len(p) == 8:
        p[0] = classes.IfElseInstruction(p[3], p[5], p[7])


def p_while_instruction(p):
    """while_instruction : WHILE '(' expression_to_bool ')' instruction_block"""
    p[0] = classes.WhileInstruction(p[3], p[5])


def p_for_instruction(p):
    """for_instruction : FOR range instruction_block"""
    p[0] = classes.ForInstruction(p[2], p[3])


def p_range(p):
    """range : ID '=' INT ':' INT
            | ID '=' INT ':' ID
            | ID '=' ID ':' INT
            | ID '=' ID ':' ID"""
    p[0] = classes.Range(p[1], p[3], p[5])


def p_break_instruction(p):
    """break_instruction : BREAK ';' """
    p[0] = classes.BreakInstruction()


def p_continue_instruction(p):
    """continue_instruction : CONTINUE ';' """
    p[0] = classes.ContinueInstruction()


def p_return_instruction(p):
    """return_instruction : RETURN expression ';'
                        | RETURN array_expression ';' """
    p[0] = classes.ReturnInstruction(p[2])


def p_print_instruction(p):
    """print_instruction : PRINT print_expressions ';' """
    p[0] = classes.PrintInstruction(p[2])


def p_instruction_block(p):
    """instruction_block : '{' instructions '}' """
    p[0] = classes.InstructionBlock(p[1])


def p_assignment_char(p):
    """assignment_char : '='
                        | PLUSASSIGNMENT
                        | MINUSASSIGNMENT
                        | TIMESASSIGNMENT
                        | DIVIDEASSIGNMENT """
    p[0] = p[1]


def p_assignment(p):
    """assignment : ID '=' zeros
                    | ID '=' ones
                    | ID '=' eye
                    | ID assignment_char expression ';'
                    | ID assignment_char array_expression ';'
                    | array assignment_char expression ';'
                    | ID '=' '[' rows ']' ';' """
    if len(p) == 4:
        p[0] = classes.Assignment(p[1], p[2], p[3])
    elif len(p) == 7:
        p[0] = classes.Assignment(p[1], p[2], classes.Array(p[4]))
    elif len(p) == 8:
        p[0] = classes.Assignment(p[1], p[2], p[3])


def p_rows(p):
    """rows : values ';' rows
            | values"""
    if len(p) == 2:
        p[0] = classes.Values([p[1]])
    else:
        p[0] = classes.Values([p[1]].append(p[3]))


def p_values(p):
    """values : values ',' expression
            | expression """
    if len(p) == 2:
        p[0] = classes.Values([p[1]])
    else:
        p[0] = classes.Values([p[1]] + [p[3]])


def p_values_int(p):
    """values_int : values_int ',' INT
            | INT """
    if len(p) == 2:
        p[0] = classes.Values([p[1]])
    else:
        p[0] = classes.Values([p[1]] + [p[3]])


def p_expression_to_bool(p):
    """expression_to_bool : expression '<' expression
                        | expression '>' expression
                        | expression EQUAL expression
                        | expression UNEQUAL expression
                        | expression LESSEQUAL expression
                        | expression GREATEREQUAL expression"""
    p[0] = classes.BinExpr(p[2], p[1], [3])


def p_expression(p):
    """expression : array
                | ID "'"
                | '-' expression
                | expression '+' expression
                | expression '-' expression
                | expression '*' expression
                | expression '/' expression"""
    if len(p) == 3:
        if p[1] == '-':
            p[0] = classes.UnExpr(p[2], p[1])
        else:
            p[0] = classes.UnExpr(p[1], p[2])
    elif len(p) == 4:
        p[0] = classes.BinExpr(p[2], p[1], [3])
    elif len(p) == 2:
        p[0] = p[1]


def p_array_expression(p):
    """array_expression : ID DOTPLUS ID
                    | ID DOTMINUS ID
                    | ID DOTTIMES ID
                    | ID DOTDIVIDE ID """
    p[0] = classes.BinExpr(p[2], p[1], [3])


def p_array(p):
    """array : ID '[' values_int ']'"""
    p[0] = classes.ValueArray(p[1], p[3])


def p_id_expression(p):
    """expression : ID"""
    p[0] = classes.Variable(p[1])


def p_int_expression(p):
    """expression : INT"""
    p[0] = classes.IntNum(p[1])


def p_float_expression(p):
    """expression : FLOAT"""
    p[0] = classes.FloatNum(p[1])
	
def p_string_expression(p):
    """expression : STRING"""
    p[0] = classes.String(p[1])


def p_print_expressions(p):
    """print_expressions : values 
		| expression 
		| '"' expression_to_bool '"' """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_eye(p):
    """eye : EYE '(' INT ')' ';' """
    p[0] = classes.EyeInit(p[3])


def p_ones(p):
    """ones : ONES '(' INT ')' ';' """
    p[0] = classes.OnesInit(p[3])


def p_zeros(p):
    """zeros : ZEROS '(' INT ')' ';' """
    p[0] = classes.ZerosInit(p[3])


parser = yacc.yacc()
