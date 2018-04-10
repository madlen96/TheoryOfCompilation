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
                            | IF '(' expression_to_bool ')' instructions ELSE instructions
                            | IF '(' expression_to_bool ')' instructions else_if_instructions ELSE instructions
                            | IF '(' expression_to_bool ')' instructions else_if_instructions"""
    # TODO


def p_else_if_instructions(p):
    """else_if_instructions : else_if_instructions ELSE IF '(' expression_to_bool ')' instructions
                            | ELSE IF '(' expression_to_bool ')' instructions"""


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
    """return_instruction : RETURN expression ';' """
    p[0] = classes.ReturnInstruction(p[2])


def p_print_instruction(p):
    """print_instruction : PRINT print_expressions ';' """
    p[0] = classes.PrintInstruction(p[2])


def p_instruction_block(p):
    """instruction_block : '{' instructions '}' """
    # TODO


def p_assignment_char(p):
    """assignment_char : '='
                        | PLUSASSIGNMENT
                        | MINUSASSIGNMENT
                        | TIMESASSIGNMENT
                        | DIVIDEASSIGNMENT """


def p_assignment(p):
    """assignment : ID '=' zeros
                    | ID '=' ones
                    | ID '=' eye
                    | ID assignment_char expression ';'
                    | ID assignment_char '-' expression ';'
                    | ID '[' values_int ']' assignment_char expression ';'
                    | ID '=' '[' rows ']' ';' """
    # TODO


def p_rows(p):
    """rows : values ';' rows
            | values"""


def p_values(p):
    """values : values ',' INT
            | values ',' FLOAT
            | values ',' ID
            | INT
            | FLOAT
            | ID """


def p_values_int(p):
    """values_int : values_int ',' INT
            | INT """


def p_expression_to_bool(p):
    """expression_to_bool : expression '<' expression
                        | expression '>' expression
                        | expression EQUAL expression
                        | expression UNEQUAL expression
                        | expression LESSEQUAL expression
                        | expression GREATEREQUAL expression"""


def p_expression(p):
    """expression : ID
                | FLOAT
                | INT
                | ID '[' values_int ']'
                | ID "'"
                | expression '+' expression
                | expression '-' expression
                | expression '*' expression
                | expression '/' expression
                | ID DOTPLUS ID
                | ID DOTMINUS ID
                | ID DOTTIMES ID
                | ID DOTDIVIDE ID """
    # TODO


def p_print_expressions(p):
    """print_expressions : values
                        | '"' expression_to_bool '"' """
    # TODO


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
