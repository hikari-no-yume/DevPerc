import sys
from random import randint
from array import array

numbers = {} # FIXME: INCOMPLETE LIST
numbers["ZERO"] = 0
numbers["ONE"] = 1
numbers["TWO"] = 2
numbers["THREE"] = 3
numbers["FOUR"] = 4
numbers["FIVE"] = 5
numbers["SIX"] = 6
numbers["SEVEN"] = 7
numbers["EIGHT"] = 8
numbers["NINE"] = 9
numbers["TEN"] = 10
numbers["ELEVEN"] = 11
numbers["TWELVE"] = 12
numbers["THIRTEEN"] = 13
numbers["FOURTEEN"] = 14
numbers["FIFTEEN"] = 15
numbers["SIXTEEN"] = 16
numbers["SEVENTEEN"] = 17
numbers["EIGHTEEN"] = 18
numbers["NINETEEN"] = 19
numbers["TWENTY"] = 20
numbers["TWENTYSEVEN"] = 27
numbers["THIRTYTWO"] = 32
numbers["THIRTYTHREE"] = 33
numbers["FORTYSEVEN"] = 47
numbers["SIXTYFIVE"] = 65
numbers["SEVENTYSEVEN"] = 77

def wrap(num):
    while num > 255:
        num -= 256
    while num < 0:
        num += 256
    return num
        
def bool_to_int(b):
    return 1 if b == True else 0

def error(e, lineno=None, p=None):
    if lineno == None:
        lineno = linenum
    if p == None:
        p = pos
    print "ERROR in line %s (character %s from file start): %s" % (lineno, p, e)
    quit()

def parse_expr(expr):
    if len(expr) == 3:
        o1 = parse_expr([expr[0]])
        o2 = parse_expr([expr[2]])
        if expr[1] == "PLUS":
            return wrap(o1 + o2)
        elif expr[1] == "MINUS":
            return wrap(o1 - o2)
        elif expr[1] == "TIMES":
            return wrap(o1 * o2)
        elif expr[1] == "DIVIDE":
            if o2 != 0:
                return wrap(o1 // o2)
            else:
                error("Division by zero")
        elif expr[1] == "EQUALS":
            return bool_to_int(o1 == o2)
        elif expr[1] == "GREATERTHAN":
            return bool_to_int(o1 > o2)
        elif expr[1] == "LESSTHAN":
            return bool_to_int(o1 < o2)
        else:
            error("'%s' is not a valid expression" % (' '.join(expr),))
    elif len(expr) == 1:
        if len(expr[0]) > 1: # Not a character
            if expr[0] in numbers:
                return numbers[expr[0]]
            elif expr[0] == "RANDOM":
                return randint(0,255)
            else:
                error("'%s' is not a valid expression" % (' '.join(expr),))
        else: # Character
            return letters[ord(expr[0])]
    else:
        error("'%s' is not a valid expression" % (' '.join(expr),))
        
def find_line_pos(lineno):
    l = 0
    for i, item in enumerate(code):
        if l == lineno:
            return i
        if item == '\n':
            l += 1
    else:
        return -1
        
def parse_command(cmd):
    if cmd[0] == "PUT":
        if len(cmd)>1:
            sys.stdout.write(chr(parse_expr(cmd[1:])))
        else:
            error("Expression expected")
    elif cmd[0] == "GET":
        if len(cmd)>1:
            c = parse_expr(cmd[1:])
            if c in letters:
                letters[parse_expr(cmd[1:])] = ord(sys.stdin.read(1))
            else:
                error("'%s' is not a valid variable" % (chr(c),))
        else:
            error("Expression expected")
    elif cmd[0] == "DEFINE":
        if "TO" in cmd:
            for i, item in enumerate(cmd):
                if item == "TO":
                    topos = i
                    break
            letters[parse_expr(cmd[1:topos])] = parse_expr(cmd[topos+1:])
        else:
            error("'TO' expected")
    elif cmd[0] == "IF":
        if "PROCEEDTO" in cmd:
            for i, item in enumerate(cmd):
                if item == "PROCEEDTO":
                    proctopos = i
                    break
            if parse_expr(cmd[1:proctopos]) == 1:
                lineno = parse_expr(cmd[proctopos+1:])
                linepos = find_line_pos(lineno)
                if linepos == -1:
                    error("Could not find line %s" % (lineno,))
                else:
                    return (lineno, linepos) # Override automatic skip to next line
        else:
            error("'PROCEEDTO' expected")
    else:
        error("Unknown command '%s'" % (cmd[0],))
    return True
        
def replace(text):
    result = ""
    lineno = 0
    incomment = False
    for p, i in enumerate(text):
        if incomment:
            if i == '\n':
                incomment = False
            result += i
        else:
            if ord(i) in letters: # Valid letter
                result += chr(letters[ord(i)])
            elif i == ' ': # Space
                result += ' '
            elif i == '/': # Comment
                result += '/'
                incomment = True
            elif i == '\n': # New line
                result += '\n'
                lineno += 1
            else: # Invalid
                error("Invalid character '%s'" % (i,), lineno, p)
    return result

if len(sys.argv)>1:
    with open(sys.argv[1], "r") as f:
        rawcode = f.read()
    
    letters = {}
    for i in range(ord('A'),ord('Z')+1):
        letters[i] = i
    
    code = replace(rawcode)
    linenum = 0
    pos = 0
    charbuf = ""
        
    while pos < len(rawcode):
        lineend = code.find('\n', pos)
        if lineend == -1:
            lineend = len(code)
        lineend += 1
        
        line = ""
        for i in code[pos:lineend].rstrip('\n'):
            if ord(i) in letters: # Valid letter
                line += i
            elif i == ' ': # Space
                line += ' '
            elif i == '/': # Comment
                break
            else: # Invalid
                error("Invalid character '%s'" % (i,))
        
        line = line.split(' ')
        
        x = parse_command(line)
        if x == True:
            linenum += 1
            pos = lineend
        else:
            linenum = x[0]
            pos = x[1]
        code = replace(rawcode)
else:
    print "devperc.py - Usage:"
    print "    python devperc.py filename"
    print "Example:"
    print "    python devperc.py helloworld"
