import sys
from get_token_form import nextsym


def CompUnit():
    global word_type, token, index, out, nowStep, args
    ans = FuncDef()
    return ans

def FuncDef():
    global word_type, token, index, out, nowStep, args
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
    global word_type, token, index, out, nowStep, args
    if token == 'int':
        out.append('i32')
        word_type, token, index = nextsym(txt, index)
        return True
    else:
        return False


def Ident():
    global word_type, token, index, out, nowStep, args
    if token == 'main':
        out.append('@main')
        word_type, token, index = nextsym(txt, index)
        return True
    else:
        return False


def Block():
    global word_type, token, index, out, nowStep, args
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
    global word_type, token, index, out, nowStep, args
    if token == 'return':
        word_type, token, index = nextsym(txt, index)
        ans, value = Exp()
        out.append('ret')
        out.append('i32')
        out.append('%'+ str(int(nowStep)-1))
        if ans:
            if token == ';':
                word_type, token, index = nextsym(txt, index)
                return True
    return False


def Exp():
    global word_type, token, index, out, nowStep, args
    ans, value = AddExp()
    return ans, value


def AddExp():
    global word_type, token, index, out, nowStep, args
    ans, value1 = MulExp()
    if ans:
        while (token == '+' or token == '-') and ans:
            now_stack_token = token
            word_type, token, index = nextsym(txt, index)
            ans, value2 = MulExp()
            if now_stack_token == '+':
                out.append('%{0} = add i32 {1}, {2}\n'.format(nowStep, value1, value2))
            elif now_stack_token == '-':
                out.append('%{0} = sub i32 {1}, {2}\n'.format(nowStep, value1, value2))
            value1 = '%' + nowStep
            nowStep = str((int(nowStep) + 1))

    return ans, value1


def MulExp():
    global word_type, token, index, out, nowStep, args
    ans, value1 = UnaryExp()
    if ans:
        while (token == '*' or token == '/' or token == '%') and ans:
            now_stack_token = token
            word_type, token, index = nextsym(txt, index)
            ans, value2 = UnaryExp()
            if now_stack_token == '*':
                out.append('%{0} = mul i32 {1}, {2}\n'.format(nowStep, value1, value2))
            elif now_stack_token == '/':
                out.append('%{0} = sdiv i32 {1}, {2}\n'.format(nowStep, value1, value2))
            elif now_stack_token == '%':
                out.append('%{0} = srem i32 {1}, {2}\n'.format(nowStep, value1, value2))
            value1 = '%' + nowStep
            nowStep = str((int(nowStep) + 1))

    return ans, value1


def UnaryExp():
    global word_type, token, index, out, nowStep
    now_stack_token = token
    if token == '(' or word_type == 'Number':
        ans, value = PrimaryExp()
        if ans:
            return ans, value
    elif token == '+' or token == '-':
        ans = UnaryOp()
        if ans:
            ans, value = UnaryExp()
            if ans:
                if now_stack_token == '-':
                    out.append("%{0} = sub i32 0, {1}\n".format(nowStep, value))
                    value = "%" + nowStep
                    nowStep = str((int(nowStep)+1))
                return ans, value
    return False, ''


def PrimaryExp():
    global word_type, token, index, out, nowStep
    if token == '(':
        word_type, token, index = nextsym(txt, index)
        ans, value = Exp()
        if ans:
            if token == ')':
                word_type, token, index = nextsym(txt, index)
                return True, value
    elif word_type == 'Number':
        value = token
        word_type, token, index = nextsym(txt, index)
        return True, value
    return False, ''


def UnaryOp():
    global word_type, token, index, out, nowStep, args
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
    args = ''
    nowStep = '1'
    f = open(sys.argv[2], 'w')
    if CompUnit():
        for item in out:
            f.write(item + ' ')
        f.close()
        exit(0)
    else:
        #f.write('1')
        exit(1)
