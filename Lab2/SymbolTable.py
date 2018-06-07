#!/usr/bin/python


class VariableSymbol(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class SymbolTable(object):
    def __init__(self, parent, name, calledFunction):  # parent scope and symbol table name
        self.parentScope = parent
        self.name = name
        self.symbols = {}
        self.calledFunction = calledFunction

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        if name not in self.symbols:
            self.symbols[name] = symbol
        else:
            return None

    def get(self, name):  # get variable symbol or fundef from <name> entry
        if name in self.symbols.keys():
            return self.symbols[name]
        elif self.parentScope is None:
            return None
        else:
            return self.getParentScope().get(name)

    def getParentScope(self):
        return self.parentScope

    def getGlobal(self, name):
        s = self.get(name)
        if s is None:
            if self.parentScope is not None:
                return self.parentScope.getGlobal(name)
            else:
                return None
        else:
            return s

    def pushScope(self, name):
        new_scope = SymbolTable(self, name, False)
        self.symbols[name] = new_scope
        return new_scope

    def popScope(self):
        parent_scope = self.getParentScope()
        if parent_scope is None:
            print('Cannot pop scope')
        parent_scope.get(self.name)
        return parent_scope
