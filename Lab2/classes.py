class Node(object):
    pass


class Const(Node):
    def __init__(self, value):
        self.value = value


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class Program(Node):
    def __init__(self, instructions_opt):
        self.instructions_opt = instructions_opt

class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Assignment(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class Instructions(Node):
    def __init__(self):
        self.instructions = []

class InstructionsOpt(Node):
    def __init__(self, instructions):
        self.instructions = instructions

class InstructionBlock(Node):
    def __init__(self, instructions):
        self.instructions = instructions

class IfElseInstruction(Node):
    def __init__(self, cond, instruction, else_):
        self.cond = cond
        self.instruction = instruction
        self.else_ = else_


class WhileInstruction(Node):
    def __init__(self, cond, instr):
        self.cond = cond
        self.instr = instr


class ForInstruction(Node):
    def __init__(self, range, instruction_block):
        self.range = range
        self.instruction_block = instruction_block


class Range(Node):
    def __init__(self, variable, from_, to_):
        self.variable = variable
        self.from_ = from_
        self.to_ = to_


class BreakInstruction(Node):
    pass


class ContinueInstruction(Node):
    pass


class ReturnInstruction(Node):
    def __init__(self, ret):
        self.ret = ret


class PrintInstruction(Node):
    def __init__(self, to_print):
        self.to_print = to_print



class EyeInit(Node):
    def __init__(self, expression):
        self.size = expression


class OnesInit(Node):
    def __init__(self, expression):
        self.expression = expression


class ZerosInit(Node):
    def __init__(self, expression):
        self.expression = expression


class UnExpr(Node):
    def __init__(self, expression, operator):
        self.expression = expression
        self.operator = operator
