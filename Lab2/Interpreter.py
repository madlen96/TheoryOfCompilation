import AST
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)


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
        pass
        # TODO

    @when(AST.Values)
    def visit(self, node):
        pass
        # TODO

    @when(AST.ValueArray)
    def visit(self, node):
        pass
        # TODO


    # @when(AST.InstructionsOpt)
    # def visit(self, node):
    #     for instruction in node.instructions:
    #         self.visit(instruction)

    #
    # @when(AST.InstructionsBlock)
    # def visit(self, node):
    #     pass
    #

    @when(AST.Program)
    def visit(self, node):
        for instr in node.instructions_opt:
            instr.accept(self)

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
        return node.to_print.accept(self)

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
        pass
        # TODO

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval
        # TODO

    @when(AST.UnExpr)
    def visit(self, node):
        pass
        # TODO

    @when(AST.Assignment)
    def visit(self, node):
        pass
        # TODO

    @when(AST.AssignmentWithArray)
    def visit(self, node):
        pass
        # TODO

    @when(AST.AssignmentWithRows)
    def visit(self, node):
        pass
        # TODO

    @when(AST.EyeInit)
    def visit(self, node):
        pass
        # TODO

    @when(AST.OnesInit)
    def visit(self, node):
        pass
        # TODO

    @when(AST.ZerosInit)
    def visit(self, node):
        pass
        # TODO
