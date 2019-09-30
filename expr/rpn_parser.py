import sys
import argparse

DEBUG = False

char_list = [
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "0",
    "."
]

pri_dct = {
    "+": 1, "-": 1,
    "*": 2, "/": 2
}

class IllegalExpressionException(Exception):
    pass

def myeval(line):
    rev = line.replace(" ", "")
    rev = make_rev_polish(rev)
    if DEBUG:
        print("REV_POLISH: ")
        print(rev)
    return calc_rev_polish(rev)
    

def make_rev_polish(line):
    stack = []
    result = []
    pos = 0
    number_flag = False
    float_flag = False
    tmp = ""
    
    while pos < len(line):
        c = line[pos]
        pos += 1
        if c in char_list:
            if c == ".":
                float_flag = True
            number_flag = True
            tmp += c
        if (c not in char_list) and number_flag:
            number_flag = False
            if float_flag:
                result.append(float(tmp))
            else:
                result.append(int(tmp))
            float_flag = False
            tmp = ""

        if c in pri_dct:
            while True:
                if len(stack) == 0:
                    stack.append(c)
                    break
                top = stack.pop()
                if top in pri_dct and pri_dct[top] >= pri_dct[c]:
                    result.append(top)
                else:
                    stack.append(top)
                    stack.append(c)
                    break
                    
        if c == "(":
            stack.append(c)
        if c == ")":
            while True:
                top = stack.pop()
                if top == "(":
                    break
                else:
                    result.append(top)

        if DEBUG:
            print(stack)
            print(result)

    if number_flag:
        if float_flag:
            result.append(float(tmp))
        else:
            result.append(int(tmp))
    for c in stack:
        result.append(c)
    return result

def calc_rev_polish(rev_list):
    stack = []
    for c in rev_list:
        if c in pri_dct:
            res = 0
            v1 = stack.pop()
            v2 = stack.pop()
            if c == "+":
                res = v2 + v1
            if c == "-":
                res = v2 - v1
            if c == "*":
                res = v2 * v1
            if c == "/":
                res = v2 / v1
            stack.append(res)
        else:
            stack.append(c)
        if DEBUG:
            print(stack)
    return stack.pop()

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
            v = myeval(line)
            print(v)
        except:
            import traceback
            traceback.print_exc()

