import sys
import argparse

"""
BNF

expr := term | expr + term | expr - term
term := factor | term * factor | term / factor
factor := (expr) | number
number := [0 - 9]*

---------

expr := <term>[+,-<term>]*
term := <factor>[*,/<factor>]*
factor := (expr) | number
number := int or float
"""

DEBUG = False

char_dct = {
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "0",
    "."
}

pos = 0

class IllegalExpressionException(Exception):
    pass

def myeval(line):
    global pos
    pos = 0
    return expr(line.replace(" ", ""))

def expr(line):
    global pos
    if DEBUG:
        print("Expr: " + line[pos:])
    v = term(line)
    while pos < len(line) and (line[pos] == "+" or line[pos] == "-"):
        op = line[pos]
        pos += 1
        if op == "+":
            v = v + term(line)
        elif op == "-":
            v = v - term(line)
    return v

def term(line):
    global pos
    if DEBUG:
        print("Term: " + line[pos:])
    v = factor(line)
    while pos < len(line) and (line[pos] == "*" or line[pos] == "/"):
        op = line[pos]
        pos += 1
        if op == "*":
            v = v * factor(line)
        elif op == "/":
            v = v / factor(line)
    return v

def factor(line):
    global pos
    if DEBUG:
        print("Factor: " + line[pos:])
    v = None
    if line[pos] == "(":
        pos += 1
        v = expr(line)
        if pos == len(line) or line[pos] != ")":
            raise IllegalExpressionException()
        pos += 1
    else:
        v = number(line)
    return v

def number(line):
    global pos
    if DEBUG:
        print("Number: " + line[pos:])
    tmp = ""
    is_float = False
    while pos < len(line) and line[pos] in char_dct:
        if line[pos] == ".":
            is_float = True
        tmp += line[pos]
        pos += 1
    if is_float:
        return float(tmp)
    else:
        return int(tmp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="debug", action="store_true")
    args = parser.parse_args()
    DEBUG = args.d
    while True:
        line = sys.stdin.readline().strip()
        if line == "q":
            break
        try:
            pos = 0
            v = myeval(line)
            if pos != len(line):
                raise IllegalExpressionException()
            print(v)
        except:
            import traceback
            traceback.print_exc()
        
