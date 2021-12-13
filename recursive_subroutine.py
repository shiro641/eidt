import sys
from get_token_form import nextsym


def judgeFunc(token):
    return token == 'getint' or token == 'getch' or token == 'putint' or token == 'putch'


def judge_wordType(word_type):
    return word_type == 'const' or word_type == 'int' or word_type == 'Indent' \
           or word_type == 'Return' or word_type == 'Lpar' or word_type == 'Plus' \
           or word_type == 'Minus' or word_type == 'Number' or word_type == 'If'


def judge_exp(word_type):
    return word_type == 'Indent' or word_type == 'Lpar' or word_type == 'Plus' \
           or word_type == 'Minus' or word_type == 'Number'


def judgeparams(name, params):
    if name == 'getint' or name == 'getch':
        if len(params) == 0:
            return True
    if name == 'putint' or name == 'putch':
        if len(params) == 1:
            return True
    return False


def CompUnit():
    global word_type, token, index, out, nowStep, varList, varType
    ans = FuncDef()
    return ans


def FuncDef():
    global word_type, token, index, out, nowStep, varList, varType
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
                    out.append('{\n')
                    ans = Block()
                    out.append('}')
                    if ans == True:
                        return True
    return False


def FuncType():
    global word_type, token, index, out, nowStep, varList, varType
    if token == 'int':
        out.append('i32')
        word_type, token, index = nextsym(txt, index)
        return True
    else:
        return False


def Ident():
    global word_type, token, index, out, nowStep, varList, varType
    if token == 'main':
        out.append('@main')
        word_type, token, index = nextsym(txt, index)
        return True
    elif word_type == 'Indent':
        word_type, token, index = nextsym(txt, index)
        return True
    else:
        return False


def Block():
    global word_type, token, index, out, nowStep, varList, varType
    if token == '{':
        #  out.append('{')
        word_type, token, index = nextsym(txt, index)
        ans = True
        k = 0
        while judge_wordType(word_type) and ans:
            k = k + 1
            if k == 10:
                ok = 1
            ans = BlockItem()
        if token == '}':
            #  out.append('}')
            word_type, token, index = nextsym(txt, index)
            return True
    return False


def BlockItem():
    global word_type, token, index, out, nowStep, varList, varType
    if word_type == 'const' or word_type == 'int':
        # word_type, token, index = nextsym(txt, index)
        ans = Decl()
    else:
        # word_type, token, index = nextsym(txt, index)
        ans = Stmt()
    return ans


def Decl():
    global word_type, token, index, out, nowStep, varList, varType
    if token == 'const':
        ans = ConstDecl()
        return ans
    elif token == 'int':
        ans = VarDecl()
        return ans
    return False


def ConstDecl():
    global word_type, token, index, out, nowStep, varList, varType
    if token == 'const':
        word_type, token, index = nextsym(txt, index)
        ans = Btype()
        if ans:
            # word_type, token, index = nextsym(txt, index)
            ans = ConstDef()
            if ans:
                temp = index
                tempToken = token
                while token == ',' and ans:
                    temp = index
                    tempToken = token
                    word_type, token, index = nextsym(txt, index)
                    ans = ConstDef()

                if not ans:
                    index = temp
                    token = tempToken

                if token == ';':
                    word_type, token, index = nextsym(txt, index)
                    return True


def ConstDef():
    global word_type, token, index, out, nowStep, varList, varType
    if word_type == 'Indent':
        constName = token
        varType[token] = 'const'
        word_type, token, index = nextsym(txt, index)
        if token == '=':
            word_type, token, index = nextsym(txt, index)
            ans, value = ConstInitVal()
            varList[constName] = value
            return ans
    return False


def ConstInitVal():
    global word_type, token, index, out, nowStep, varList, varType
    ans, value = ConstExp()
    return ans, value


def ConstExp():
    global word_type, token, index, out, nowStep, varList, varType, judgeConst
    judgeConst = True
    ans, value = AddExp()
    judgeConst = False
    return ans, value


def Btype():
    global word_type, token, index, out, nowStep, varList, varType
    if token == 'int':
        word_type, token, index = nextsym(txt, index)
        return True
    return False


def VarDecl():
    global word_type, token, index, out, nowStep, varList, varType
    ans = Btype()
    if ans:
        # word_type, token, index = nextsym(txt, index)
        ans = VarDef()
        temp = index
        tempToken = token
        if ans:
            while token == ',' and ans:
                temp = index
                tempToken = token
                word_type, token, index = nextsym(txt, index)
                ans = VarDef()
            if not ans:
                token = tempToken
                index = temp

            if token == ';':
                word_type, token, index = nextsym(txt, index)
                return True
    return False


def VarDef():
    global word_type, token, index, out, nowStep, varList, varType
    if word_type == 'Indent':
        out.append('%n{0} = alloca i32\n'.format(nowStep))
        varList[token] = '%n' + nowStep
        varType[token] = 'var'
        oldStep = nowStep
        nowStep = str((int(nowStep) + 1))
        word_type, token, index = nextsym(txt, index)
        temp = index
        if token == '=':
            word_type, token, index = nextsym(txt, index)
            ans, value = InitVal()
            if ans:
                out.append('store i32 {0}, i32* %n{1}\n'.format(value, oldStep))
            if not ans:
                index = temp
        return True
    return False


def InitVal():
    global word_type, token, index, out, nowStep, varList, varType
    ans, value = Exp()
    return ans, value


def Stmt():
    global word_type, token, index, out, nowStep, varList, varType, labelStep
    if word_type == 'Return':
        word_type, token, index = nextsym(txt, index)
        ans, value = Exp()
        out.append('ret i32 {0}\n'.format(value))
        if ans:
            if token == ';':
                word_type, token, index = nextsym(txt, index)
                return True
    elif word_type == 'Indent':

        temp = index
        tempToken = token
        tempType = word_type

        ans, varName = LVal()
        if ans:
            if token == '=':
                if (varName not in varType) or (varType[varName] == 'const'):
                    return False
                word_type, token, index = nextsym(txt, index)
                ans, value = Exp()
                out.append('store i32 {0}, i32* {1}\n'.format(value, varList[varName]))
                if ans:
                    if token == ';':
                        word_type, token, index = nextsym(txt, index)
                        return True
            else:
                index = temp
                word_type = tempType
                token = tempToken

                ans = Exp()
                if ans:
                    if token == ';':
                        word_type, token, index = nextsym(txt, index)
                        return True
    elif token == ';':
        word_type, token, index = nextsym(txt, index)
        return True
    elif word_type == 'Lpar' or word_type == 'Plus' or word_type == 'Minus' or word_type == 'Number':
        ans = Exp()
        if ans:
            while ans and judge_exp(word_type):
                ans = Exp()
            if token == ';':
                return True
    elif token == '{':
        ans = Block()
        return ans
    elif token == 'if':
        word_type, token, index = nextsym(txt, index)
        if token == '(':
            word_type, token, index = nextsym(txt, index)
            label = []
            ans = Cond(label)
            if ans:
                if token == ')':
                    word_type, token, index = nextsym(txt, index)
                    out.append('a'+label[0]+':'+'\n')
                    ans = Stmt()
                    end = labelStep
                    out.append('br label %a{0}\n'.format(end))
                    labelStep = str(int(labelStep) + 1)
                    if ans:
                        out.append('a' + label[1] + ':' + '\n')
                        if token == 'else':
                            word_type, token, index = nextsym(txt, index)
                            ans = Stmt()

                        out.append('br label %a{0}\n'.format(end))
                        out.append('a' + end + ':' + '\n')
                        return ans

    return False


def Cond(label):
    global word_type, token, index, out, nowStep, varList, varType
    ans = LOrExp(label)
    # out.append('%{0} = icmp eq i32 {1}, {2}'.format(nowStep, value1, value2))
    return ans


def LOrExp(label):
    global word_type, token, index, out, nowStep, varList, varType, labelStep
    Orlabel = []
    label.append(labelStep)
    labelStep = str(int(labelStep) + 1)
    ans = LAndExp(Orlabel, label)
    if ans:
        while ans and token == '||':
            word_type, token, index = nextsym(txt, index)
            ans = LAndExp(Orlabel, label)


    return ans


def LAndExp(Orlabel, label):
    global word_type, token, index, out, nowStep, varList, varType, labelStep
    if len(Orlabel) != 0:
        out.append('a'+Orlabel[0]+':'+'\n')  #no
    # Orlabel.append(nowStep)  #no
    # nowStep = str(int(nowStep)+1)
    ans, value1 = EqExp()

    '''yes = nowStep  #yes
    nowStep = str(int(nowStep)+1)'''
    no = labelStep  #no
    labelStep = str(int(labelStep) + 1)

    if ans:
        while ans and token == '&&':
            yes = labelStep  # yes
            labelStep = str(int(labelStep) + 1)
            out.append('br i1 {0},label %a{1}, label %a{2}\n'.format(value1, yes, no))
            out.append('a' + yes+':'+'\n')  #if yes, compare next exp
            word_type, token, index = nextsym(txt, index)
            ans, value1 = EqExp()

        if len(label) == 1:
            label.append(no)  #no
        else:
            label[1] = no  # no

        #  Orlabel.append(yes)  #yes
        if len(Orlabel) == 0:
            Orlabel.append(no)
        else:
            Orlabel[0] = no  #attention: Orlabel = [no] without yes

        out.append('br i1 {0},label %a{1}, label %a{2}\n'.format(value1, label[0], Orlabel[0]))

    return ans


def EqExp():
    global word_type, token, index, out, nowStep, varList, varType, OnlyExp
    # needTrans = False
    ans, value1 = RelExp()
    if ans:
        if token == '==' or token == '!=':
            while ans and (token == '==' or token == '!='):
                nowStackToken = token
                word_type, token, index = nextsym(txt, index)
                ans, value2 = RelExp()
                if nowStackToken == '==':
                    out.append('%n{0} = icmp eq i32 {1}, {2}\n'.format(nowStep, value1, value2))
                elif nowStackToken == '!=':
                    out.append('%n{0} = icmp ne i32 {1}, {2}\n'.format(nowStep, value1, value2))
                value1 = '%n' + nowStep
                nowStep = str((int(nowStep) + 1))
        else:
            if OnlyExp:
                out.append('%n{0} = icmp ne i32 {1}, 0\n'.format(nowStep, value1))
                value1 = '%n' + nowStep
                nowStep = str((int(nowStep) + 1))

    return ans, value1


def RelExp():
    global word_type, token, index, out, nowStep, varList, varType, OnlyExp
    ans, value1 = AddExp()
    OnlyExp = True
    if ans:
        while ans and (token == '>=' or token == '<=' or token == '>' or token == '<'):
            if OnlyExp:
                OnlyExp = False
            nowStackToken = token
            word_type, token, index = nextsym(txt, index)
            ans, value2 = AddExp()
            if nowStackToken == '>=':
                out.append('%n{0} = icmp sge i32 {1}, {2}\n'.format(nowStep, value1, value2))
            elif nowStackToken == '<=':
                out.append('%n{0} = icmp sle i32 {1}, {2}\n'.format(nowStep, value1, value2))
            elif nowStackToken == '>':
                out.append('%n{0} = icmp sgt i32 {1}, {2}\n'.format(nowStep, value1, value2))
            elif nowStackToken == '<':
                out.append('%n{0} = icmp slt i32 {1}, {2}\n'.format(nowStep, value1, value2))

            value1 = '%n' + nowStep
            nowStep = str((int(nowStep) + 1))

    return ans, value1


def LVal():
    global word_type, token, index, out, nowStep, varList, varType
    value = token
    if word_type == 'Indent':
        word_type, token, index = nextsym(txt, index)
        return True, value
    return False


def Exp():
    global word_type, token, index, out, nowStep, varList, varType
    ans, value = AddExp()
    return ans, value


def AddExp():
    global word_type, token, index, out, nowStep, varList, varType
    ans, value1 = MulExp()
    if ans:
        while (token == '+' or token == '-') and ans:
            now_stack_token = token
            word_type, token, index = nextsym(txt, index)
            ans, value2 = MulExp()
            if now_stack_token == '+':
                out.append('%n{0} = add i32 {1}, {2}\n'.format(nowStep, value1, value2))
            elif now_stack_token == '-':
                out.append('%n{0} = sub i32 {1}, {2}\n'.format(nowStep, value1, value2))
            value1 = '%n' + nowStep
            nowStep = str((int(nowStep) + 1))

    return ans, value1


def MulExp():
    global word_type, token, index, out, nowStep, varList, varType
    ans, value1 = UnaryExp()
    if ans:
        while (token == '*' or token == '/' or token == '%') and ans:
            now_stack_token = token
            word_type, token, index = nextsym(txt, index)
            ans, value2 = UnaryExp()
            if now_stack_token == '*':
                out.append('%n{0} = mul i32 {1}, {2}\n'.format(nowStep, value1, value2))
            elif now_stack_token == '/':
                out.append('%n{0} = sdiv i32 {1}, {2}\n'.format(nowStep, value1, value2))
            elif now_stack_token == '%':
                out.append('%n{0} = srem i32 {1}, {2}\n'.format(nowStep, value1, value2))
            value1 = '%n' + nowStep
            nowStep = str((int(nowStep) + 1))

    return ans, value1


def UnaryExp():
    global word_type, token, index, out, nowStep, varList, varType, defFunc
    now_stack_token = token
    if token == '(' or word_type == 'Number' or word_type == 'Indent':
        if judgeFunc(token):
            funcName = token
            temp = index
            tempToken = token
            tempType = word_type
            word_type, token, index = nextsym(txt, index)
            if token == '(':
                params = []
                word_type, token, index = nextsym(txt, index)
                if token == ')':
                    if judgeparams(funcName, params):
                        if funcName not in defFunc:
                            defFunc.append(funcName)
                            defStr = 'declare i32 @{0}('.format(funcName)
                            # this is not a good way-----
                            if len(params) == 1:
                                defStr = defStr + 'i32'
                            defStr = defStr + ')\n'
                            # ---------------------------
                            out.insert(0, defStr)
                        value = '%n' + nowStep
                        # ----------------
                        if len(params) == 1:
                            out.append('%n{0} = call i32 @{1}(i32 {2})\n'.format(nowStep, funcName, params[0]))
                            nowStep = str(int(nowStep) + 1)
                        else:
                            out.append('%n{0} = call i32 @{1}()\n'.format(nowStep, funcName))
                            nowStep = str(int(nowStep) + 1)
                        # ----------------
                        word_type, token, index = nextsym(txt, index)
                        return True, value
                    else:
                        return False, ''
                elif judge_exp(word_type):
                    ans = FuncRParams(params)
                    if ans:
                        if token == ')':
                            if judgeparams(funcName, params):
                                if funcName not in defFunc:
                                    defFunc.append(funcName)
                                    defStr = 'declare i32 @{0}('.format(funcName)
                                    # this is not a good way-----
                                    if len(params) == 1:
                                        defStr = defStr + 'i32'
                                    defStr = defStr + ')\n'
                                    # ---------------------------
                                    out.insert(0, defStr)
                                value = '%n' + nowStep
                                # ----------------
                                if len(params) == 1:
                                    out.append('%n{0} = call i32 @{1}(i32 {2})\n'.format(nowStep, funcName, params[0]))
                                    nowStep = str(int(nowStep) + 1)
                                else:
                                    out.append('%n{0} = call i32 @{1}()\n'.format(nowStep, funcName))
                                    nowStep = str(int(nowStep) + 1)
                                # ----------------
                                word_type, token, index = nextsym(txt, index)
                                return True, value
                else:
                    return False, ''  # because PrimaryExp do not has Indent(, you can also write index = temp ... here
            else:
                index = temp
                token = tempToken
                word_type = tempType

        ans, value = PrimaryExp()
        if ans:
            return ans, value
    elif token == '+' or token == '-' or token == '!':
        ans = UnaryOp()
        if ans:
            ans, value = UnaryExp()
            if ans:
                if now_stack_token == '-':
                    out.append("%n{0} = sub i32 0, {1}\n".format(nowStep, value))
                    value = "%n" + nowStep
                    nowStep = str((int(nowStep) + 1))
                elif now_stack_token == '!':
                    out.append('%n{0} = icmp eq i32 {1}, 0\n'.format(nowStep, value))
                    out.append('%n{0} = zext i1 %n{1} to i32\n'.format(str(int(nowStep)+1), nowStep))
                    value = "%n" + str(int(nowStep)+1)
                    nowStep = str(int(nowStep) + 2)
                return ans, value
    return False, ''


def FuncRParams(params):
    global word_type, token, index, out, nowStep, varList, varType, judgeConst
    ans, value = Exp()
    if ans:
        params.append(value)
        temp = index
        tempToken = token
        while ans and token == ',':
            temp = index
            tempToken = token
            word_type, token, index = nextsym(txt, index)
            ans, value = Exp()
            if ans:
                params.append(value)
        if not ans:
            index = temp
            token = tempToken
        return True
    return False


def PrimaryExp():
    global word_type, token, index, out, nowStep, varList, varType, judgeConst
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
    elif word_type == 'Indent':
        ans, varName = LVal()
        if varName not in varList:
            return False, ''
        else:
            if judgeConst:
                if varType[varName] != 'const':
                    return False, ''
            if varType[varName] != 'const':
                out.append('%n{0} = load i32, i32* {1}\n'.format(nowStep, varList[varName]))
                nowStep = str((int(nowStep) + 1))
                return ans, '%n' + str(int(nowStep) - 1)
            return ans, varList[varName]
    return False, ''


def UnaryOp():
    global word_type, token, index, out, nowStep, varList, varType
    if token == '+' or token == '-' or token == '!':
        word_type, token, index = nextsym(txt, index)
        return True
    return False


if __name__ == '__main__':
    file = open(sys.argv[1])
    # print(sys.argv[1])
    txt = file.read()
    word_type, token, index = nextsym(txt, 0)
    out = []
    varList = {}
    varType = {}
    nowStep = '1'
    labelStep = '1'
    defFunc = []
    judgeConst = False
    OnlyExp = True
    f = open(sys.argv[2], 'w')
    if CompUnit():
        for item in out:
            f.write(item + ' ')
        f.close()
        exit(0)
    else:
        # f.write('1')
        exit(1)
