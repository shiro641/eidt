import sys
from get_token_form import nextsym


def CompUnit():
    global word_type, token, index
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
    global word_type, token, index
    if token == 'main':
        out.append('@main')
        word_type, token, index = nextsym(txt, index)
        return True
    else:
        return False


def Block():
    global word_type, token, index
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
    global word_type, token, index
    if token == 'return':
        out.append('ret')
        word_type, token, index = nextsym(txt, index)
        if word_type == 'Number':
            out.append('i32')
            out.append(token)
            word_type, token, index = nextsym(txt, index)
            if token == ';':
                word_type, token, index = nextsym(txt, index)
                return True
    return False


if __name__ == '__main__':
    file = open(sys.argv[1])
    # print(sys.argv[1])
    txt = file.read()
    word_type, token, index = nextsym(txt, 0)
    out = []
    if CompUnit():
        for item in out:
            print(item, end=' ')
    else:
        print(-1)
