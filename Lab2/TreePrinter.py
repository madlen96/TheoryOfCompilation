from __future__ import print_function
import AST

separator = '| '


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Const)
    def printTree(self, indent=0):
        return indent * separator + str(self.value) + "\n"

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        return indent * separator + str(self.value) + "\n"

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        return indent * separator + str(self.value) + "\n"

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        return indent * separator + str(self.name) + "\n"

    @addToClass(AST.String)
    def printTree(self, indent=0):
        return indent * separator + str(self.value) + "\n"

    @addToClass(AST.ValueArray)
    def printTree(self, indent=0):
        result = indent * separator + "REF\n"
        result += (indent + 1) * separator + self.name + "\n"
        result += self.index.printTree(indent + 1)
        return result

    @addToClass(AST.Values)
    def printTree(self, indent=0):
        result = ""
        for i in self.values:
            result += i.printTree(indent)
        return result

    @addToClass(AST.Rows)
    def printTree(self, indent=0):
        result = indent * separator + "MATRIX\n"
        for i in self.values:
            result += (indent + 1) * separator + "VECTOR\n"
            result += i.printTree(indent + 2)
        return result

    @addToClass(AST.Array)
    def printTree(self, indent=0):
        result = indent * separator + "MATRIX\n"
        result += self.values.printTree(indent + 1)
        return result

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        if self.instructions_opt is not None:
            return self.instructions_opt.printTree(indent)
        else:
            pass

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        result =  indent * separator + self.op + "\n"
        result += self.left.printTree(indent + 1)
        result += self.right.printTree(indent + 1)
        return result

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        result = indent * separator + self.op + "\n"
        result += (indent + 1) * separator + self.name + "\n"
        result += self.expr.printTree(indent + 1)
        return result

    @addToClass(AST.AssignmentWithArray)
    def printTree(self, indent=0):
        result = indent * separator + self.op + "\n"
        result += self.array.printTree(indent + 1)
        result += self.expr.printTree(indent + 1)
        return result

    @addToClass(AST.AssignmentWithRows)
    def printTree(self, indent=0):
        result = indent * separator + self.op + "\n"
        result += (indent + 1) * separator + self.id + "\n"
        result += self.expr.printTree(indent + 1)
        return result

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        result = ""
        for i in self.instructions:
            result += i.printTree(indent)
        return result

    @addToClass(AST.InstructionsOpt)
    def printTree(self, indent=0):
        return self.instructions.printTree(indent)

    @addToClass(AST.InstructionBlock)
    def printTree(self, indent=0):
        return self.instructions.printTree(indent)

    @addToClass(AST.IfElseInstruction)
    def printTree(self, indent=0):
        result = indent * separator + "IF\n"
        result += self.cond.printTree(indent + 1)
        result += indent * separator + "THEN\n"
        result += self.instruction.printTree(indent + 1)
        if self.else_ is not None:
            result += indent * separator + "ELSE\n"
            result += self.else_.printTree(indent + 1)
        return result

    @addToClass(AST.WhileInstruction)
    def printTree(self, indent=0):
        result = indent * separator + "WHILE\n"
        result += self.cond.printTree(indent + 1)
        result += self.instr.printTree(indent + 1)
        return result

    @addToClass(AST.ForInstruction)
    def printTree(self, indent=0):
        result = ""
        result += indent * separator + "FOR" + "\n"
        result += (indent + 1) * separator + self.variable + "\n"
        result += self.range.printTree(indent + 1)
        result += self.instruction_block.printTree(indent + 1)
        return result

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        result = indent * separator + "RANGE\n"
        result += self.from_.printTree(indent+1)
        result += self.to.printTree(indent+1)
        return result

    @addToClass(AST.BreakInstruction)
    def printTree(self, indent=0):
        return indent * separator + "BREAK\n"

    @addToClass(AST.ContinueInstruction)
    def printTree(self, indent=0):
        return indent * separator + "CONTINUE\n"

    @addToClass(AST.ReturnInstruction)
    def printTree(self, indent=0):
        result = indent * separator + "RETURN\n"
        result += self.ret.printTree(indent + 1)
        return result

    @addToClass(AST.PrintInstruction)
    def printTree(self, indent=0):
        result = indent * separator + "PRINT\n"
        result += self.to_print.printTree(indent + 1)
        return result

    @addToClass(AST.EyeInit)
    def printTree(self, indent=0):
        result = indent * separator + "EYE\n"
        result += (indent + 1) * separator + str(self.size) + "\n"
        return result

    @addToClass(AST.OnesInit)
    def printTree(self, indent=0):
        result = indent * separator + "ONES\n"
        result += (indent + 1) * separator + str(self.size) + "\n"
        return result

    @addToClass(AST.ZerosInit)
    def printTree(self, indent=0):
        result = indent * separator + "ZEROS\n"
        result += (indent + 1) * separator + str(self.size) + "\n"
        return result

    @addToClass(AST.UnExpr)
    def printTree(self, indent=0):
        if self.operator == "'":
            result = indent * separator + "TRANSPOSE" + '\n'
        else:
            result = indent * separator + self.operator + '\n'
        result += self.expression.printTree(indent + 1)
        return result

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        return ""
