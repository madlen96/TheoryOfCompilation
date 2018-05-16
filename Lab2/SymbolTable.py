#!/usr/bin/python


class VariableSymbol(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class SymbolTable(object):
    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parentScope = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        if name not in self.symbols:
            self.symbols[name] = symbol
        else:
            raise ValueError

    def get(self, name):  # get variable symbol or fundef from <name> entry
        if name in self.symbols.keys():
            return self.symbols[name]
        elif self.parentScope.name is None:
            return None
        else:
            return self.getParentScope().get(name)

    def getParentScope(self):
        return self.parentScope

    def pushScope(self, name):
        new_scope = SymbolTable(self, name)
        self.symbols[name] = new_scope
        return new_scope

    def popScope(self):
        parent_scope = self.getParentScope()
        if parent_scope is None:
            print('Cannot pop scope')
        parent_scope.pop(self.name)
        return parent_scope
