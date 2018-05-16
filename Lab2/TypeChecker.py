#!/usr/bin/python
import AST
import SymbolTable

types_dict = dict()

for op in ['+', '-', '/', '*']:
    types_dict[(op, 'float', 'float')] = 'float'
    types_dict[(op, 'float', 'int')] = 'float'
    types_dict[(op, 'int', 'int')] = 'int'
    types_dict[(op, 'int', 'float')] = 'float'


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

                    # simpler version of generic_visit, not so general
                    # def generic_visit(self, node):
                    #    for child in node.children:
                    #        self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable.SymbolTable(None, "root")

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)
        op = node.op
        op_type = types_dict[(op, type1, type2)]
        if op_type is None:
            print('Invalid types in binary expression in line: ')
        return op_type

    def visit_Const(self, node):
        # TODO
        pass

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        # TODO
        pass

    def visit_Program(self, node):
        if node.instructions_opt is not None:
            self.visit(node.instructions_opt)

    def visit_ValueArray(self, node):
        # TODO
        pass

    def visit_Rows(self, node):
        # TODO
        pass

    def visit_Values(self, node):
        # TODO
        pass

    def visit_Array(self, node):
        # TODO
        pass

    def visit_Assignment(self, node):
        # TODO
        pass

    def visit_AssignmentWithArray(self, node):
        # TODO
        pass

    def visit_AssignmentWithRows(self, node):
        # TODO
        pass

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_InstructionsOpt(self, node):
        self.visit(node.instructions)

    def visit_InstructionBlock(self, node):
        self.visit(node.instructions)

    def visit_IfElseInstruction(self, node):
        # TODO czy trzeba sprawdzac tez warunek?
        self.visit(node.instruction)
        if node.else_ is not None:
            self.visit(node.else_)

    def visit_WhileInstruction(self, node):
        # TODO czy trzeba sprawdzac tez warunek?
        self.visit(node.instr)

    def visit_ForInstruction(self, node):
        self.visit(node.range)
        self.visit(node.instruction_block)

    def visit_Range(self, node):
        # TODO czy trzeba sprawdzac czy to jest tylko int?
        from_ = self.visit(node.from_)
        to = self.visit(node.to)
        if from_ != 'int' or to != 'int':
            print('Not int in range instruction in line ')

    def visit_BreakInstruction(self, node):
        tab = self.table
        while tab is not None and tab.name != 'while' and tab.name != 'for':
            tab = tab.parentScope
        if tab is None:
            print('Break instruction not in a loop in line ')

    def visit_ContinueInstruction(self, node):
        tab = self.table
        while tab is not None and tab.name != 'while' and tab.name != 'for':
            tab = tab.parentScope
        if tab is None:
            print('Continue instruction not in a loop in line ')

    def visit_ReturnInstruction(self, node):
        pass

    def visit_PrintInstruction(self, node):
        pass

    def visit_EyeInit(self, node):
        arg = self.visit(node.size)
        if arg != 'int':
            print('Incorrect argument type in eye function in line: ')

    def visit_OnesInit(self, node):
        arg = self.visit(node.size)
        if arg != 'int':
            print('Incorrect argument type in ones function in line: ')

    def visit_ZerosInit(self, node):
        arg = self.visit(node.size)
        if arg != 'int':
            print('Incorrect argument type in zeros function in line: ')

    def visit_UnExpr(self, node):
        # TODO
        pass
