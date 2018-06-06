import sys
import scanner
import Mparser
import TypeChecker
import Interpreter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "ex.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer)
    # result = ast.printTree()
    # print(result)

    typeChecker = TypeChecker.TypeChecker()
    typeChecker.visit(ast)
    ast.accept(Interpreter.Interpreter())
