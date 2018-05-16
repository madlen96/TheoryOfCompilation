#!/usr/bin/python


class VariableSymbol(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type
    #


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        pass
    #

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        pass
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        pass
    #

    def getParentScope(self):
        pass
    #

    def pushScope(self, name):
        pass
    #

    def popScope(self):
        pass
    #

