#!/usr/bin/python

import scanner
import AST
import ply.yacc as yacc


tokens = scanner.tokens + scanner.literals

precedence = (
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE'),
    ("right", '=', 'PLUSASSIGNMENT', 'MINUSASSIGNMENT', 'TIMESASSIGNMENT', 'DIVIDEASSIGNMENT'),
    ('nonassoc', '<', '>', 'EQUAL', 'UNEQUAL', 'LESSEQUAL', 'GREATEREQUAL'),  # Nonassociative operators
    ('left', 'DOTPLUS', 'DOTMINUS'),
    ('left', 'DOTTIMES', 'DOTDIVIDE'),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("right", 'TRANSPOSE')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""
    p[0] = AST.Program(p[1])


def p_instructions_opt_1(p):
    """instructions_opt : instructions """
    p[0] = AST.InstructionsOpt(p[1])


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions(p):
    """instructions : instructions instruction
                    | instruction"""
    if len(p) == 3:
        p[1].instructions.append(p[2])
        p[0] = p[1]
    else:
        p[0] = AST.Instructions(p.lineno(1))
        p[0].instructions.append(p[1])


def p_instruction(p):
    """instruction : if_else_instruction
                    | while_instruction
                    | for_instruction
                    | break_instruction
                    | continue_instruction
                    | return_instruction
                    | print_instruction
                    | assignment
                    | expression ';'"""
    p[0] = p[1]


def p_if_else_instruction(p):
    """if_else_instruction : IF '(' expression_to_bool ')' instructions %prec IFX
                            | IF '(' expression_to_bool ')' instructions ELSE instructions"""
    if len(p) == 6:
        p[0] = AST.IfElseInstruction(p[3], p[5], p.lineno(1))
    elif len(p) == 8:
        p[0] = AST.IfElseInstruction(p[3], p[5], p.lineno(1), p[7])


def p_while_instruction(p):
    """while_instruction : WHILE '(' expression_to_bool ')' instruction_block"""
    p[0] = AST.WhileInstruction(p[3], p[5], p.lineno(1))


def p_for_instruction(p):
    """for_instruction : FOR ID '=' range instruction_block"""
    p[0] = AST.ForInstruction(p[2], p[4], p[5], p.lineno(1))


def p_range(p):
    """range : expression ':' expression"""
    p[0] = AST.Range(p[1], p[3], p.lineno(1))


def p_break_instruction(p):
    """break_instruction : BREAK ';' """
    p[0] = AST.BreakInstruction(p.lineno(1))


def p_continue_instruction(p):
    """continue_instruction : CONTINUE ';' """
    p[0] = AST.ContinueInstruction(p.lineno(1))


def p_return_instruction(p):
    """return_instruction : RETURN expression ';' """
    p[0] = AST.ReturnInstruction(p[2], p.lineno(1))


def p_print_instruction(p):
    """print_instruction : PRINT print_expressions ';' """
    p[0] = AST.PrintInstruction(p[2], p.lineno(1))


def p_instruction_block(p):
    """instruction_block : '{' instructions '}' """
    p[0] = AST.InstructionBlock(p[2], p.lineno(1))


def p_assignment_op(p):
    """assignment_op : '='
                        | PLUSASSIGNMENT
                        | MINUSASSIGNMENT
                        | TIMESASSIGNMENT
                        | DIVIDEASSIGNMENT """
    p[0] = p[1]


# do poprawy
def p_assignment(p):
    """assignment : ID assignment_op expression ';'
                    | ID '[' values ']' assignment_op expression ';'
                    | ID '=' '[' rows ']' ';' """
    if len(p) == 5:
        p[0] = AST.Assignment(p[2], p[1], p[3], p.lineno(1))
    elif len(p) == 7:
        p[0] = AST.AssignmentWithRows(p[2], p[1], p[4], p.lineno(1))
    elif len(p) == 8:
        p[0] = AST.AssignmentWithArray(p[5], AST.ValueArray(p[1], p[3], p.lineno(1)), p[6], p.lineno(1))


def p_id_expression(p):
    """expression : ID"""
    p[0] = AST.Variable(p[1], p.lineno(1))


def p_string_expression(p):
    """expression : STRING"""
    p[0] = AST.String(p[1], p.lineno(1))


def p_int_expression(p):
    """expression : INT"""
    p[0] = AST.IntNum(p[1], p.lineno(1))


def p_float_expression(p):
    """expression : FLOAT"""
    p[0] = AST.FloatNum(p[1], p.lineno(1))


def p_rows(p):
    """rows : rows ';' values
            | values"""
    if len(p) == 2:
        p[0] = AST.Rows(p.lineno(1))
        p[0].values.append(p[1])
    else:
        p[1].values.append(p[3])
        p[0] = p[1]


def p_values(p):
    """values : values ',' expression
            | expression """
    if len(p) == 2:
        p[0] = AST.Values(p.lineno(1))
        p[0].values.append(p[1])
    else:
        p[1].values.append(p[3])
        p[0] = p[1]


def p_expression_to_bool(p):
    """expression_to_bool : expression '<' expression
                        | expression '>' expression
                        | expression EQUAL expression
                        | expression UNEQUAL expression
                        | expression LESSEQUAL expression
                        | expression GREATEREQUAL expression"""
    p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(2))


def p_expression(p):
    """expression : array
                | expression TRANSPOSE
                | '-' expression
                | expression '+' expression
                | expression '-' expression
                | expression '*' expression
                | expression '/' expression"""
    if len(p) == 3:
        if p[1] == '-':
            p[0] = AST.UnExpr(p[2], p[1], p.lineno(1))
        elif p[2] == '\'':
            p[0] = AST.UnExpr(p[1], p[2], p.lineno(1))
    elif len(p) == 4:
        p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(2))
    elif len(p) == 2:
        p[0] = p[1]


def p_array_expression(p):
    """expression : expression DOTPLUS expression
                    | expression DOTMINUS expression
                    | expression DOTTIMES expression
                    | expression DOTDIVIDE expression """
    p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(1))


def p_array(p):
    """array : ID '[' values ']'"""
    p[0] = AST.ValueArray(p[1], p[3], p.lineno(1))


def p_print_expressions(p):
    """print_expressions : values
                        | STRING """
    p[0] = p[1]


def p_eye(p):
    """expression : EYE '(' INT ')' """
    p[0] = AST.EyeInit(AST.IntNum(p[3], p.lineno(1)), p.lineno(1))


def p_ones(p):
    """expression : ONES '(' INT ')' """
    p[0] = AST.OnesInit(AST.IntNum(p[3], p.lineno(1)), p.lineno(1))


def p_zeros(p):
    """expression : ZEROS '(' INT ')' """
    p[0] = AST.ZerosInit(AST.IntNum(p[3], p.lineno(1)), p.lineno(1))


parser = yacc.yacc()
