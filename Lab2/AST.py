class Node(object):
    pass


class Const(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class String(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class IntNum(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class FloatNum(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class Variable(Node):
    def __init__(self, name, line):
        self.name = name
        self.line = line


class ValueArray(Node):
    def __init__(self, name, index, line):
        self.name = name
        self.index = index
        self.line = line


class Rows(Node):
    def __init__(self, line):
        self.values = []
        self.line = line


class Values(Node):
    def __init__(self, line):
        self.values = []
        self.line = line


class Array(Node):
    def __init__(self, row, line):
        self.values = row
        self.line = line


class Program(Node):
    def __init__(self, instructions_opt):
        self.instructions_opt = instructions_opt


class BinExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class Assignment(Node):
    def __init__(self, op, name, expr, line):
        self.op = op
        self.name = name
        self.expr = expr
        self.line = line


class AssignmentWithArray(Node):
    def __init__(self, op, array, expr, line):
        self.op = op
        self.array = array
        self.expr = expr
        self.line = line


class AssignmentWithRows(Node):
    def __init__(self, op, id, expr, line):
        self.op = op
        self.id = id
        self.expr = expr
        self.line = line


class Instructions(Node):
    def __init__(self, line):
        self.instructions = []
        self.line = line

# z zerowa liczba elementow
# albo np 10 albo zaden element
class InstructionsOpt(Node):
    def __init__(self, instructions):
        self.instructions = instructions


# lista instrukcji,mozna to zredukowac/zmienic
class InstructionBlock(Node):
    def __init__(self, instructions, line):
        self.instructions = instructions
        self.line = line

class IfElseInstruction(Node):
    def __init__(self, cond, instruction, line, else_=None,):
        self.cond = cond
        self.instruction = instruction
        self.else_ = else_
        self.line = line


class WhileInstruction(Node):
    def __init__(self, cond, instr, line):
        self.cond = cond
        self.instr = instr
        self.line = line


class ForInstruction(Node):
    def __init__(self, variable, range, instruction_block, line):
        self.variable = variable
        self.range = range
        self.instruction_block = instruction_block
        self.line = line

class Range(Node):
    def __init__(self, from_, to, line):
        self.from_ = from_
        self.to = to
        self.line = line


class BreakInstruction(Node):
    def __init__(self, line):
        self.line = line


class ContinueInstruction(Node):
    def __init__(self, line):
        self.line = line


class ReturnInstruction(Node):
    def __init__(self, ret, line):
        self.ret = ret
        self.line = line


class PrintInstruction(Node):
    def __init__(self, to_print, line):
        self.to_print = to_print
        self.line = line


class EyeInit(Node):
    def __init__(self, expression, line):
        self.size = expression
        self.line = line

class OnesInit(Node):
    def __init__(self, expression, line):
        self.size = expression
        self.line = line

class ZerosInit(Node):
    def __init__(self, expression, line):
        self.size = expression
        self.line = line


class UnExpr(Node):
    def __init__(self, expression, operator, line):
        self.expression = expression
        self.operator = operator
        self.line = line


class Error(Node):
    def __init__(self):
        pass

