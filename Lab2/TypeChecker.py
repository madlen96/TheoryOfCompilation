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
        self.table = SymbolTable.SymbolTable(None, "root", calledFunction=None)

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)
        op = node.op
        if type1 is None or type2 is None:
            print "Undeclare variable in line: {0}".format(node.line)
        else:
            op_type = types_dict[(op, type1, type2)]
            if op_type is None:
                print "Invalid types in binary expression in line: {0}".format(node.line)
            return op_type
        return None

    def visit_Const(self, node):
        pass

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        # TODO nie wiem czy to ma byc tak? -->zmienilam, ale tez nie wiem czy to ok
        # self.table.put(node.name, None)
        # return None
        var = self.table.getGlobal(node.name)
        if var is None:
            print "Undefined symbol {0} in line {1}.".format(node.name, node.line)
        else:
            return None# TODO chociaz chyba powinno sie zwrocic typ tej zmiennej

    def visit_Program(self, node):
        if node.instructions_opt is not None:
            self.visit(node.instructions_opt)

    def visit_ValueArray(self, node):
        # TODO w mapie z macierzami?
        if self.table.get(node.name) is None:
            print "Variable is undeclare in line {0}".format(node.line)
        elif len(self.visit(node.index)) == len(self.table.get(node.name)):
            print "Incorrect index in line {0}".format(node.line)
        else:
            values = self.visit(node.index)
            size_matrix = self.table.get(node.name)
            for value, size in zip(values, size_matrix):
                if value < 0 or value > size:
                    print "Index out of range in line {0}".format(node.line)

    def visit_Rows(self, node):
        count_rows = 0
        count_elem_in_row = 0
        for row in node.values:
            count_rows += 1
            if count_elem_in_row == 0:
                count_elem_in_row = self.visit(row)
            elif len(self.visit(row)) != count_elem_in_row:
                print("Different size in line {0}".format(node.line))
                # TODO fix name
        return count_rows, count_elem_in_row

    def visit_Values(self, node):
        return node.values

    def visit_Array(self, node):
        self.visit(node.values)
    #     TODO czy tu powinnam zwracac typ ktory przechowuje w tablicy czy w tablicy moga byc wogle rozne typy? -->
    #     TODO chyba nie mamy nigdzie uwzglenionego, ze nie moga

    def visit_Assignment(self, node):
        if node.op != '=':
            if self.table.get(node.name) is None:
                print "Undeclare variable in line {0}".format(node.line)
        else:
            if self.table.get(node.name) is None:
                self.table.put(node.name, self.visit(node.expr))
            # else:
            #     print('This variable is already initialize in line ')


#### cos pozmienialam, ale nie wiem
    # def visit_Assignment(self, node):
    #     name = self.table.getGlobal(node.name)
    #     if node.op != '=':
    #         if name is None:
    #             print "Undefined symbol: {0} at line {1}".format(node.name, node.lineno)
    #     else:
    #         if self.table.getGlobal(node.name) is None:
    #             self.table.put(node.name, self.visit(node.expr))

    def visit_AssignmentWithArray(self, node):
        self.visit(node.array)
        self.visit(node.expr)

    def visit_AssignmentWithRows(self, node):
        if self.table.get(node.id) is None:
            #     TODO dodawac do innej mapy?
            size = self.visit(node.expr)
            self.table.put(node.id, size)
        else:
            print "This variable is already initialized in line {0}".format(node.line)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_InstructionsOpt(self, node):
        self.visit(node.instructions)

    def visit_InstructionBlock(self, node):
        self.visit(node.instructions)

    def visit_IfElseInstruction(self, node):
        # TODO czy trzeba sprawdzac tez warunek? --> chyba tak
        type = self.visit(node.cond)
        if type != 'int':
            print "Incorrect condition type in IF ELSE instr in line {0}".format(node.line)
        self.visit(node.instruction)
        if node.else_ is not None:
            self.visit(node.else_)

    def visit_WhileInstruction(self, node):
        # TODO czy trzeba sprawdzac tez warunek? --> chyba tak,powinien sprowadzac sie do inta
        self.visit(node.instr)
        type = self.visit(node.cond)
        if type != 'int':
            print "Incorrect condition type in while instr in line {0}".format(node.line)
        self.table = self.table.pushScope('while')
        self.visit(node.instr)
        self.table = self.table.popScope()

    def visit_ForInstruction(self, node):
        self.visit(node.range)
        self.table = self.table.pushScope('for')
        self.visit(node.instruction_block)
        self.table = self.table.popScope()

    def visit_Range(self, node):
        # TODO czy moze byc cos innego niz int? --> raczej nie
        from_ = self.visit(node.from_)
        to = self.visit(node.to)
        if from_ != 'int' or to != 'int':
            print "Not int in range instruction in line in line {0}".format(node.line)

    def visit_BreakInstruction(self, node):
        tab = self.table
        while tab is not None and tab.name != 'while' and tab.name != 'for':
            tab = tab.parentScope
        if tab is None:
            print "Break instruction not in a loop in line {0}".format(node.line)

    def visit_ContinueInstruction(self, node):
        tab = self.table
        while tab is not None and tab.name != 'while' and tab.name != 'for':
            tab = tab.parentScope
        if tab is None:
            print "Continue instruction not in a loop in line {0}".format(node.line)

    def visit_ReturnInstruction(self, node):
        if self.table.calledFunction is None:
            print "Return statement outside of function in line {0}".format(node.line)

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
        val = self.visit(node.expression)
        return val
