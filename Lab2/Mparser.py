#!/usr/bin/python

import scanner
import classes
import ply.yacc as yacc

tokens = scanner.tokens + scanner.literals

precedence = (
   ("nonassoc", 'IF'),
   ("nonassoc", 'ELSE'),
   ("right", '=','PLUSASSIGNMENT','MINUSASSIGNMENT','TIMESASSIGNMENT','DIVIDEASSIGNMENT'),
   ('nonassoc', '<', '>', 'EQUAL', 'UNEQUAL','LESSEQUAL','GREATEREQUAL'),  # Nonassociative operators
   ("left", '+', '-'),
   ("left", '*', '/'),
   ('left', 'DOTPLUS', 'DOTMINUS'),
   ('left', 'DOTMUL', 'DOTDIV'),
 )


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""
    p[0] = classes.Program(p[1])

def p_instructions_opt_1(p):
    """instructions_opt : instructions """
    p[0] = classes.InstructionsOpt(p[1])


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction
                      | instruction"""
    # TODO


def p_instructions_2(p):
    """instructions : instruction """


def p_instruction(self, p):
    """instruction : if_else_instruction
                    | while_instruction
                    | for_instruction
                    | break_instruction
                    | continue_instruction
                    | return_instruction
                    | print_instruction
                    | instruction_block
                    | assignment ';'"""
    p[0] = p[1]

def p_if_else_instruction(p):
    """if_else_instruction : """
    # TODO

def p_while_instruction(p):
    """while_instruction : WHILE '(' expression ')' instruction_block"""
    p[0] = classes.WhileInstruction(p[3], p[5])

def p_for_instruction(p):
    """for_instruction : FOR range instruction_block"""
    p[0] = classes.ForInstruction(p[2], p[3])

def p_range(p):
    """range : ID '=' expression ':' expression"""
    p[0] = classes.Range(p[1], p[3], p[5])

def p_break_instruction(p):
    """break_instruction : BREAK"""
    p[0] = classes.BreakInstruction()

def p_continue_instruction(p):
    """continue_instruction : CONTINUE"""
    p[0] = classes.ContinueInstruction()

def p_return_instruction(p):
    """return_instruction : RETURN expression"""
    p[0] = classes.ReturnInstruction(p[2])

def p_print_instruction(p):
    """print_instruction : PRINT print_expressions ';' """
    p[0] = classes.PrintInstruction(p[2])

def p_instruction_block(p):
    """instruction_block: """
    # TODO

def p_assignment(p):
    """assignment: """
    # TODO

def p_expression(p):
    """expression : """
    # TODO

def p_print_expressions(p):
    """print_expressions : """
    # TODO

def p_eye(self, p):
    """eye : EYE '(' INT ')' """
    p[0] = classes.EyeInit(p[3])

def p_ones(self, p):
    """ones : ONES '(' INT ')' """
    p[0] = classes.OnesInit(p[3])

def p_zeros(self, p):
    """zeros : ZEROS '(' INT ')' """
    p[0] = classes.ZerosInit(p[3])


parser = yacc.yacc()

