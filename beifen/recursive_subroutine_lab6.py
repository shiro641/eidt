import sys
from get_token_form import nextsym


def judgeFunc(token):
    return token == 'getint' or token == 'getch' or token == 'putint' or token == 'putch'


def judge_wordType(word_type):
    return word_type == 'const' or word_type == 'int' or word_type == 'Indent' \
           or word_type == 'Return' or word_type == 'Lpar' or word_type == 'Plus' \
           or word_type == 'Minus' or word_type == 'Number' or word_type == 'If' \
           or word_type == 'LBrace' or word_type == 'While' or word_type == 'Break'\
           or word_type == 'Continue'


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
    global word_type, token, index, out, nowStep, g_variable, g_variable_type, needExp
    isGlobal = True
    while token == 'int' or token == 'const':
        temp_index = index
        temp_token = token
        word_type, token, index = nextsym(txt, index)
        word_type, token, index = nextsym(txt, index)
        if token == '(':
            index = temp_index
            token = temp_token
            break
        index = temp_index
        token = temp_token
        Decl(g_variable, g_variable_type)
    isGlobal = False
    ans = FuncDef()
    return ans


def FuncDef():
    global word_type, token, index, out, nowStep, g_variable, g_variable_type
    out.append('define dso_local')
    ans = FuncType()
    if ans:
        ans = Ident()
        if ans:
            if token == '(':
                out.append('(')
                word_type, token, index = nextsym(txt, index)
                if token == ')':
                    out.append(')')
                    word_type, token, index = nextsym(txt, index)
                    out.append('{\n')
                    varList = g_variable.copy()
                    varType = g_variable_type.copy()
                    varList_ = g_variable.copy()
                    varType_ = g_variable.copy()
                    ans = Block(varList, varType, varList_, varType_)
                    out.append('}')
                    if ans:
                        return True
    return False


def FuncType():
    global word_type, token, index, out, nowStep
    if token == 'int':
        out.append('i32')
        word_type, token, index = nextsym(txt, index)
        return True
    else:
        return False


def Ident():
    global word_type, token, index, out, nowStep
    if token == 'main':
        out.append('@main')
        word_type, token, index = nextsym(txt, index)
        return True
    elif word_type == 'Indent':
        word_type, token, index = nextsym(txt, index)
        return True
    else:
        return False


def Block(varList, varType, varList_, varType_, b_c_label=None):
    global word_type, token, index, out, nowStep
    if token == '{':
        #  out.append('{')
        word_type, token, index = nextsym(txt, index)
        ans = True
        # k = 0
        while judge_wordType(word_type) and ans:
            ''' ----just for debugging-------
            k = k + 1
            if k == 10:
                ok = 1
            ---------------------------------'''
            ans = BlockItem(varList, varType, varList_, varType_, b_c_label)
        if token == '}':
            #  out.append('}')
            word_type, token, index = nextsym(txt, index)
            return True
    return False


def BlockItem(varList, varType, varList_, varType_, b_c_label=None):
    global word_type, token, index, out, nowStep
    if word_type == 'const' or word_type == 'int':
        # word_type, token, index = nextsym(txt, index)
        ans = Decl(varList, varType, varList_, varType_)
    else:
        # word_type, token, index = nextsym(txt, index)
        ans = Stmt(varList, varType, b_c_label)
    return ans


def Decl(varList, varType, varList_=None, varType_=None):
    global word_type, token, index, out, nowStep, needExp
    if token == 'const':
        ans = ConstDecl(varList, varType, varList_, varType_)
        return ans
    elif token == 'int':
        ans = VarDecl(varList, varType, varList_, varType_)
        return ans
    elif isGlobal:
        if token == 'const':
            ans = ConstDecl(varList, varType, varList_, varType_)
            return ans
        elif token == 'int':
            ans = VarDecl(varList, varType, varList_, varType_)
            return ans

    return False


def ConstDecl(varList, varType, varList_, varType_):
    global word_type, token, index, out, nowStep
    if token == 'const':
        word_type, token, index = nextsym(txt, index)
        ans = Btype()
        if ans:
            # word_type, token, index = nextsym(txt, index)
            ans = ConstDef(varList, varType, varList_, varType_)
            if ans:
                temp = index
                tempToken = token
                while token == ',' and ans:
                    temp = index
                    tempToken = token
                    word_type, token, index = nextsym(txt, index)
                    ans = ConstDef(varList, varType, varList_, varType_)

                if not ans:
                    index = temp
                    token = tempToken

                if token == ';':
                    word_type, token, index = nextsym(txt, index)
                    return True


def ConstDef(varList, varType, varList_, varType_):
    global word_type, token, index, out, nowStep
    if word_type == 'Indent':
        constName = token
        if not needExp:
            if constName in varList and constName not in varList_:
                return False
        else:
            if constName in varList:
                return False
        varType[token] = 'const'
        word_type, token, index = nextsym(txt, index)
        if token == '=':
            exp = []
            exp.append('')
            word_type, token, index = nextsym(txt, index)
            ans, value = ConstInitVal(varList, varType, exp)
            if not needExp:
                varList[constName] = value
            else:
                varList[constName] = eval(exp[0])
            return ans
        else:
            if needExp:
                varList[constName] = 0
            return True
    return False


def ConstInitVal(varList, varType, exp=None):
    global word_type, token, index, out, nowStep
    ans, value = ConstExp(varList, varType, exp)
    return ans, value


def ConstExp(varList, varType, exp=None):
    global word_type, token, index, out, nowStep, judgeConst
    judgeConst = True
    ans, value = AddExp(varList, varType, exp)
    judgeConst = False
    return ans, value


def Btype():
    global word_type, token, index, out, nowStep
    if token == 'int':
        word_type, token, index = nextsym(txt, index)
        return True
    return False


def VarDecl(varList, varType, varList_, varType_):
    global word_type, token, index, out, nowStep
    ans = Btype()
    if ans:
        # word_type, token, index = nextsym(txt, index)
        ans = VarDef(varList, varType, varList_, varType_)
        temp = index
        tempToken = token
        if ans:
            while token == ',' and ans:
                temp = index
                tempToken = token
                word_type, token, index = nextsym(txt, index)
                ans = VarDef(varList, varType, varList_, varType_)
            if not ans:
                token = tempToken
                index = temp

            if token == ';':
                word_type, token, index = nextsym(txt, index)
                return True
    return False


def VarDef(varList, varType, varList_, varType_):
    global word_type, token, index, out, nowStep, needExp
    if word_type == 'Indent':
        if not isGlobal:
            if token in varList and token not in varList_:
                return False
            out.append('%n{0} = alloca i32\n'.format(nowStep))
            varList[token] = '%n' + nowStep
            varType[token] = 'var'
            oldStep = nowStep
            nowStep = str((int(nowStep) + 1))
        else:
            if token in varList:
                return False
            varList[token] = '@' + token
            varType[token] = 'var'
            globalName = token
        word_type, token, index = nextsym(txt, index)
        if token == '=':
            word_type, token, index = nextsym(txt, index)
            exp = []
            exp.append('')
            ans, value = InitVal(varList, varType, exp)
            if ans:
                if not isGlobal:
                    out.append('store i32 {0}, i32* %n{1}\n'.format(value, oldStep))
                else:
                    out.append('@{0} = dso_local global i32 {1}\n'.format(globalName, eval(exp[0])))
            return ans
        else:
            if isGlobal:
                out.append('@{0} = dso_local global i32 {1}\n'.format(globalName, 0))
            return True
    return False


def InitVal(varList, varType, exp=None):
    global word_type, token, index, out, nowStep
    ans, value = Exp(varList, varType, exp)
    return ans, value


def Stmt(varList, varType, b_c_label=None):
    global word_type, token, index, out, nowStep, labelStep
    if word_type == 'Return':
        word_type, token, index = nextsym(txt, index)
        ans, value = Exp(varList, varType)
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
                ans, value = Exp(varList, varType)
                out.append('store i32 {0}, i32* {1}\n'.format(value, varList[varName]))
                if ans:
                    if token == ';':
                        word_type, token, index = nextsym(txt, index)
                        return True
            else:
                index = temp
                word_type = tempType
                token = tempToken

                ans = Exp(varList, varType)
                if ans:
                    if token == ';':
                        word_type, token, index = nextsym(txt, index)
                        return True
    elif token == ';':
        word_type, token, index = nextsym(txt, index)
        return True
    elif word_type == 'Lpar' or word_type == 'Plus' or word_type == 'Minus' or word_type == 'Number':
        ans = Exp(varList, varType)
        if ans:
            while ans and judge_exp(word_type):
                ans = Exp(varList, varType)
            if token == ';':
                return True
    elif token == '{':
        # ______save_________
        varList_ = varList.copy()
        varType_ = varType.copy()
        # ___________________

        ans = Block(varList, varType, varList_, varType_, b_c_label)

        # ______copy_________
        varList.clear()
        varType.clear()
        for _ in varList_:
            varList[_] = varList_[_]
        for _ in varType_:
            varType[_] = varType_[_]
        # ____________________

        return ans
    elif token == 'if':
        word_type, token, index = nextsym(txt, index)
        if token == '(':
            word_type, token, index = nextsym(txt, index)
            label = []
            ans = Cond(label, varList, varType)
            if ans:
                if token == ')':
                    word_type, token, index = nextsym(txt, index)
                    # ------------yes ⬇----------
                    out.append('a' + label[0] + ':' + '\n')
                    ans = Stmt(varList, varType, b_c_label)
                    if ans:
                        end = labelStep
                        out.append('br label %a{0}\n'.format(end))
                        labelStep = str(int(labelStep) + 1)
                    # ------------yes ⬆----------
                        out.append('a' + label[1] + ':' + '\n')
                        if token == 'else':
                            word_type, token, index = nextsym(txt, index)
                            ans = Stmt(varList, varType, b_c_label)

                        out.append('br label %a{0}\n'.format(end))
                        out.append('a' + end + ':' + '\n')
                        return ans
    elif token == 'while':
        word_type, token, index = nextsym(txt, index)
        if token == '(':
            word_type, token, index = nextsym(txt, index)
            label = []
            condStart = labelStep
            out.append('br label %a{0}\n'.format(condStart))
            out.append('a' + condStart + ':' + '\n')
            labelStep = str(int(labelStep) + 1)
            ans = Cond(label, varList, varType)
            if ans:
                if token == ')':
                    word_type, token, index = nextsym(txt, index)
                    # ------------yes ⬇----------
                    out.append('a' + label[0] + ':' + '\n')
                    b_c_label = [condStart, label[1]]
                    ans = Stmt(varList, varType, b_c_label)
                    if ans:
                        out.append('br label %a{0}\n'.format(condStart))
                    # ------------yes ⬆----------
                        out.append('a' + label[1] + ':' + '\n')
                        return ans
    elif token == 'break':
        out.append('br label %a{0}\n'.format(b_c_label[1]))
        word_type, token, index = nextsym(txt, index)
        if token == ';':
            word_type, token, index = nextsym(txt, index)
            return True

    elif token == 'continue':
        out.append('br label %a{0}\n'.format(b_c_label[0]))
        word_type, token, index = nextsym(txt, index)
        if token == ';':
            word_type, token, index = nextsym(txt, index)
            return True

    return False


def Cond(label, varList, varType):
    global word_type, token, index, out, nowStep
    ans = LOrExp(label, varList, varType)
    # out.append('%{0} = icmp eq i32 {1}, {2}'.format(nowStep, value1, value2))
    return ans


def LOrExp(label, varList, varType):
    global word_type, token, index, out, nowStep, labelStep
    Orlabel = []
    label.append(labelStep)
    labelStep = str(int(labelStep) + 1)
    ans = LAndExp(Orlabel, label, varList, varType)
    if ans:
        while ans and token == '||':
            word_type, token, index = nextsym(txt, index)
            ans = LAndExp(Orlabel, label, varList, varType)

    return ans


def LAndExp(Orlabel, label, varList, varType):
    global word_type, token, index, out, nowStep, labelStep
    if len(Orlabel) != 0:
        out.append('a' + Orlabel[0] + ':' + '\n')  # no
    # Orlabel.append(nowStep)  #no
    # nowStep = str(int(nowStep)+1)
    ans, value1 = EqExp(varList, varType)

    '''yes = nowStep  #yes
    nowStep = str(int(nowStep)+1)'''
    no = labelStep  # no
    labelStep = str(int(labelStep) + 1)

    if ans:
        while ans and token == '&&':
            yes = labelStep  # yes
            labelStep = str(int(labelStep) + 1)
            out.append('br i1 {0},label %a{1}, label %a{2}\n'.format(value1, yes, no))
            out.append('a' + yes + ':' + '\n')  # if yes, compare next exp
            word_type, token, index = nextsym(txt, index)
            ans, value1 = EqExp(varList, varType)

        if len(label) == 1:
            label.append(no)  # no
        else:
            label[1] = no  # no

        #  Orlabel.append(yes)  #yes
        if len(Orlabel) == 0:
            Orlabel.append(no)
        else:
            Orlabel[0] = no  # attention: Orlabel = [no] without yes

        out.append('br i1 {0},label %a{1}, label %a{2}\n'.format(value1, label[0], Orlabel[0]))

    return ans


def EqExp(varList, varType):
    global word_type, token, index, out, nowStep, OnlyExp
    # needTrans = False
    ans, value1 = RelExp(varList, varType)
    if ans:
        if token == '==' or token == '!=':
            while ans and (token == '==' or token == '!='):
                nowStackToken = token
                word_type, token, index = nextsym(txt, index)
                ans, value2 = RelExp(varList, varType)
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


def RelExp(varList, varType):
    global word_type, token, index, out, nowStep, OnlyExp
    ans, value1 = AddExp(varList, varType)
    OnlyExp = True
    if ans:
        while ans and (token == '>=' or token == '<=' or token == '>' or token == '<'):
            if OnlyExp:
                OnlyExp = False
            nowStackToken = token
            word_type, token, index = nextsym(txt, index)
            ans, value2 = AddExp(varList, varType)
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
    global word_type, token, index, out, nowStep
    value = token
    if word_type == 'Indent':
        word_type, token, index = nextsym(txt, index)
        return True, value
    return False


def Exp(varList, varType, exp=None):
    global word_type, token, index, out, nowStep
    ans, value = AddExp(varList, varType, exp)
    return ans, value


def AddExp(varList, varType, exp=None):
    global word_type, token, index, out, nowStep, needExp
    ans, value1 = MulExp(varList, varType, exp)
    if ans:
        while (token == '+' or token == '-') and ans:
            if isGlobal:
                exp[0] += token
            now_stack_token = token
            word_type, token, index = nextsym(txt, index)
            ans, value2 = MulExp(varList, varType, exp)
            if not isGlobal:
                if now_stack_token == '+':
                    out.append('%n{0} = add i32 {1}, {2}\n'.format(nowStep, value1, value2))
                elif now_stack_token == '-':
                    out.append('%n{0} = sub i32 {1}, {2}\n'.format(nowStep, value1, value2))
                value1 = '%n' + nowStep
                nowStep = str((int(nowStep) + 1))

    return ans, value1


def MulExp(varList, varType, exp=None):
    global word_type, token, index, out, nowStep, needExp
    ans, value1 = UnaryExp(varList, varType, exp)
    if ans:
        while (token == '*' or token == '/' or token == '%') and ans:
            if isGlobal:
                exp[0] += token
            now_stack_token = token
            word_type, token, index = nextsym(txt, index)
            ans, value2 = UnaryExp(varList, varType, exp)
            if not isGlobal:
                if now_stack_token == '*':
                    out.append('%n{0} = mul i32 {1}, {2}\n'.format(nowStep, value1, value2))
                elif now_stack_token == '/':
                    out.append('%n{0} = sdiv i32 {1}, {2}\n'.format(nowStep, value1, value2))
                elif now_stack_token == '%':
                    out.append('%n{0} = srem i32 {1}, {2}\n'.format(nowStep, value1, value2))
                value1 = '%n' + nowStep
                nowStep = str((int(nowStep) + 1))

    return ans, value1


def UnaryExp(varList, varType, exp=None):
    global word_type, token, index, out, nowStep, defFunc, needExp
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
                    ans = FuncRParams(params, varList, varType)
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

        ans, value = PrimaryExp(varList, varType, exp)
        if ans:
            return ans, value
    elif token == '+' or token == '-' or token == '!':
        ans = UnaryOp()
        if ans:
            ans, value = UnaryExp(varList, varType, exp)
            if ans:
                if isGlobal:
                    exp[0] += str(now_stack_token)
                if not isGlobal:
                    if now_stack_token == '-':
                        out.append("%n{0} = sub i32 0, {1}\n".format(nowStep, value))
                        value = "%n" + nowStep
                        nowStep = str((int(nowStep) + 1))
                    elif now_stack_token == '!':
                        out.append('%n{0} = icmp eq i32 {1}, 0\n'.format(nowStep, value))
                        out.append('%n{0} = zext i1 %n{1} to i32\n'.format(str(int(nowStep) + 1), nowStep))
                        value = "%n" + str(int(nowStep) + 1)
                        nowStep = str(int(nowStep) + 2)
                return ans, value
    return False, ''


def FuncRParams(params, varList, varType):
    global word_type, token, index, out, nowStep
    ans, value = Exp(varList, varType)
    if ans:
        params.append(value)
        temp = index
        tempToken = token
        while ans and token == ',':
            temp = index
            tempToken = token
            word_type, token, index = nextsym(txt, index)
            ans, value = Exp(varList, varType)
            if ans:
                params.append(value)
        if not ans:
            index = temp
            token = tempToken
        return True
    return False


def PrimaryExp(varList, varType, exp=None):
    global word_type, token, index, out, nowStep, judgeConst, needExp
    if token == '(':
        if isGlobal:
            exp[0] += '('
        word_type, token, index = nextsym(txt, index)
        ans, value = Exp(varList, varType, exp)
        if ans:
            if token == ')':
                if isGlobal:
                    exp[0] += ')'
                word_type, token, index = nextsym(txt, index)
                return True, value
    elif word_type == 'Number':
        value = token
        if isGlobal:
            exp[0] += str(value)
        word_type, token, index = nextsym(txt, index)
        return True, value
    elif word_type == 'Indent':
        ans, varName = LVal()
        if varName not in varList:
            return False, ''
        else:
            if judgeConst or isGlobal:
                if varType[varName] != 'const':
                    return False, ''
            if not isGlobal:
                if varType[varName] != 'const':
                    out.append('%n{0} = load i32, i32* {1}\n'.format(nowStep, varList[varName]))
                    nowStep = str((int(nowStep) + 1))
                    return ans, '%n' + str(int(nowStep) - 1)
            if isGlobal:
                exp[0] += str(varList[varName])
            return ans, varList[varName]
    return False, ''


def UnaryOp():
    global word_type, token, index, out, nowStep
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
    nowStep = '1'
    labelStep = '1'
    defFunc = []
    judgeConst = False
    OnlyExp = True
    needExp = False
    g_variable = {}
    g_variable_type = {}
    f = open(sys.argv[2], 'w')
    if CompUnit():
        for item in out:
            f.write(item + ' ')
        f.close()
        exit(0)
    else:
        # f.write('1')
        exit(1)
