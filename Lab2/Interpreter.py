import AST
from Memory import *
from Exceptions import *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

BIN_OP = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '.+': lambda a, b: np.add(a, b),
    '.-': lambda a, b: np.subtract(a, b),
    '.*': lambda a, b: np.multiply(a, b),
    './': lambda a, b: np.divide(a, b),
    '=': lambda a, b: b,
    '+=': lambda a, b: a + b,
    '-=': lambda a, b: a - b,
    '*=': lambda a, b: a * b,
    '/=': lambda a, b: a / b,
    '<': lambda a, b: a < b,
    '>': lambda a, b: a > b,
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '<=': lambda a, b: a <= b,
    '>=': lambda a, b: a >= b,
}


class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack(Memory('global'))

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Const)
    def visit(self, node):
        return node.value

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        return self.memory_stack.get(node.name)

    @when(AST.Rows)
    def visit(self, node):
        return node.values

    @when(AST.Array)
    def visit(self, node):
        return node.values

    @when(AST.Values)
    def visit(self, node):
        return node.values

    @when(AST.ValueArray)
    def visit(self, node):
        array = self.memory_stack.get(node.name)
        list_of_index = node.index.accept(self)

        pass
        # TODO


    @when(AST.InstructionsOpt)
    def visit(self, node):
        node.instructions.accept(self)


    @when(AST.InstructionBlock)
    def visit(self, node):
        node.instructions.accept(self)


    @when(AST.Program)
    def visit(self, node):
        node.instructions_opt.accept(self)

    @when(AST.ReturnInstruction)
    def visit(self, node):
        val = node.ret.accept(self)
        raise ReturnValueException(val)

    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException()

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()

    @when(AST.PrintInstruction)
    def visit(self, node):
        print(node.to_print.accept(self))

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    @when(AST.Range)
    def visit(self, node):
        return range(node.from_.accept(self), node.to.accept(self))

    @when(AST.ForInstruction)
    def visit(self, node):
        self.memory_stack.push(Memory(node.id))
        r = None
        for i in node.range.accept(self):
            self.memory_stack.insert(node.variable.name, i)
            try:
                r = node.instruction_block.accept(self)
            except ContinueException:
                pass
            except BreakException:
                break
        self.memory_stack.pop()
        return r

    @when(AST.WhileInstruction)
    def visit(self, node):
        r = None
        self.memory_stack.push(Memory(node.id))
        while node.cond.accept(self):
            try:
                r = node.instr.accept(self)
            except ContinueException:
                pass
            except BreakException:
                break
        self.memory_stack.pop()
        return r

    @when(AST.IfElseInstruction)
    def visit(self, node):
        r = None
        if node.cond.accept(self):
            r = node.instruction.accept(self)
        elif node.else_ is not None:
            r = node.else_.accept(self)
        return r

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return BIN_OP[node.op](r1, r2)

    @when(AST.UnExpr)
    def visit(self, node):
        if node.operator == "-":
            return - node.expression.accept(self)
        else:
            return np.transpose(node.expression.accept(self))

    @when(AST.Assignment)
    def visit(self, node):
        name = node.name.accept(self)
        expr = node.expr.accept(self)
        value = BIN_OP[node.op](self.memory_stack.get(name), expr)
        if node.op == '=':
            self.memory_stack.insert(name, value)
        else:
            self.memory_stack.set(name, value)
        return value

    @when(AST.AssignmentWithArray)
    def visit(self, node):
        name = node.array.accept(self)
        expr = node.expr.accept(self)
        value = BIN_OP[node.op](self.memory_stack.get(name), expr)
        if node.op == '=':
            self.memory_stack.insert(name, value)
        else:
            self.memory_stack.set(name, value)
        return value

    @when(AST.AssignmentWithRows)
    def visit(self, node):
        name = node.id.accept(self)
        expr = node.expr.accept(self)
        value = BIN_OP[node.op](self.memory_stack.get(name), expr)
        if node.op == '=':
            self.memory_stack.insert(name, value)
        else:
            self.memory_stack.set(name, value)
        return value

    @when(AST.EyeInit)
    def visit(self, node):
        return np.eye(node.size.accept(self))

    @when(AST.OnesInit)
    def visit(self, node):
        return np.ones(node.size.accept(self))

    @when(AST.ZerosInit)
    def visit(self, node):
        return np.zeros(node.size.accept(self))
