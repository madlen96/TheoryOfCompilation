#!/usr/bin/python


class VariableSymbol(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type
        #


class SymbolTable(object):
    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parentScope = parent
        self.name = name
        self.symbols = {}

    #

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        if name not in self.symbols:
            self.symbols[name] = symbol
        else:
            raise ValueError

    def get(self, name):  # get variable symbol or fundef from <name> entry
        pass

    #

    def getParentScope(self):
        return self.parentScope

    #

    def pushScope(self, name):
        pass

    #

    def popScope(self):
        pass
        #
