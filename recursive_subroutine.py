import sys
from get_token_form import nextsym


def CompUnit():
    global word_type, token, index, out
    ans = FuncDef()
    return ans

def FuncDef():
    global word_type, token, index, out
    out.append('define dso_local')
    ans = FuncType()
    if ans == True:
        ans = Ident()
        if ans:
            if token == '(':
                out.append('(')
                word_type, token, index = nextsym(txt, index)
                if token == ')':
                    out.append(')')
                    word_type, token, index = nextsym(txt, index)
                    ans = Block()
                    if ans == True:
                        return True
    return False


def FuncType():
    global word_type, token, index, out
    if token == 'int':
        out.append('i32')
        word_type, token, index = nextsym(txt, index)
        return True
    else:
        return False


def Ident():
    global word_type, token, index, out
    if token == 'main':
        out.append('@main')
        word_type, token, index = nextsym(txt, index)
        return True
    else:
        return False


def Block():
    global word_type, token, index, out
    if token == '{':
        out.append('{')
        word_type, token, index = nextsym(txt, index)
        ans = Stmt()
        if ans:
            if token == '}':
                out.append('}')
                word_type, token, index = nextsym(txt, index)
                return True
    return False


def Stmt():
    global word_type, token, index, out
    if token == 'return':
        word_type, token, index = nextsym(txt, index)
        ans = Exp()
        out.append('ret')
        if ans:
            if token == ';':
                word_type, token, index = nextsym(txt, index)
                return True
    return False


def Exp():
    global word_type, token, index, out
    ans = AddExp()
    return ans


def AddExp():
    global word_type, token, index, out
    ans = MulExp()
    return ans


def MulExp():
    global word_type, token, index, out
    ans = UnaryExp()
    return ans


def UnaryExp():
    global word_type, token, index, out
    if token == '(' or word_type == 'Number':
        ans = PrimaryExp()
        return ans
    elif token == '+' or token == '-':
        ans = UnaryOp()
        if ans:
            ans = UnaryExp()
            return ans
    return False


def PrimaryExp():
    global word_type, token, index, out
    if token == '(':
        word_type, token, index = nextsym(txt, index)
        ans = Exp()
        if ans:
            if token == ')':
                word_type, token, index = nextsym(txt, index)
                return True
    elif word_type == 'Number':
        word_type, token, index = nextsym(txt, index)
        return True
    return False


def UnaryOp():
    global word_type, token, index, out
    if token == '+' or token == '-':
        word_type, token, index = nextsym(txt, index)
        return True
    return False


if __name__ == '__main__':
    file = open(sys.argv[1])
    # print(sys.argv[1])
    txt = file.read()
    word_type, token, index = nextsym(txt, 0)
    out = []
    f = open(sys.argv[2], 'w')
    if CompUnit():
        for item in out:
            f.write(item + ' ')
        f.close()
        exit(0)
    else:
        #f.write('1')
        exit(1)
