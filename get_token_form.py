import sys
import re

keyword = {'if':'If', 'else':'Else', 'while':'While', 'break':'Break', 'continue':'Continue', 'return':'Return'}


def isSpace(char):
    return (char == ' ') or char == '\t' or char == '\n'


def getNbc(s, start):
    while start < len(s):
        if not isSpace(s[start]):
            break
        start += 1
    return start


def isHexDigit(chr):
    return chr.isdigit() or chr == 'a' or chr == 'b' or chr == 'c' or chr == 'd' or chr == 'e' or chr == 'f'

def checkAlpha(chr):
    return chr == '_' or chr.isalpha()


def nextsym(sentense, i):
    while i < len(sentense):
        token = ''
        i = getNbc(sentense, i)
        if i >= len(sentense):
            break
        char = sentense[i]
        if checkAlpha(char):
            while checkAlpha(char) or char.isdigit():
                token += char
                i += 1
                char = sentense[i]
            # i -= 1
            if token in keyword:
                return keyword[token], token, i  # type, token, index
                # ans.append(keyword[token])
            else:
                return 'Indent', token, i
                # ans.append('Ident({})'.format(token))
        elif char.isdigit():
            if char == '0':
                token += char
                i += 1
                char = sentense[i]
                if char == 'x' or char == 'X':
                    token += char
                    i += 1
                    char = sentense[i]
                    if isHexDigit(char):
                        while isHexDigit(char):
                            token += char
                            i += 1
                            char = sentense[i]
                        tmp = int(token, 16)
                        token = str(tmp)
                        return 'Number', token, i
                    else:
                        return 'Number', '0', i-1
                elif char.isdigit() and char < '8':
                    while char.isdigit() and char < '8':
                        token += char
                        i += 1
                        char = sentense[i]
                    tmp = int(token, 8)
                    token = str(tmp)
                    return 'Number', token, i
                else:
                    return 'Number', token, i
            else:
                while char.isdigit():
                    token += char
                    i += 1
                    char = sentense[i]
                return 'Number', token, i
        elif char == '=':
            i += 1
            char = sentense[i]
            if char == '=':
                # ans.append('Eq')
                i += 1
                return 'Eq', '==', i
            else:
                # ans.append('Assign')
                return 'Assign', '=', i
        elif char == ';':
            # ans.append('Semicolon')
            i += 1
            return 'Semicolon', ';', i
        elif char == '(':
            # ans.append('LPar')
            i += 1
            return 'Lpar', '(', i
        elif char == ')':
            # ans.append('RPar')
            i += 1
            return 'RPar', ')', i
        elif char == '{':
            # ans.append('LBrace')
            i += 1
            return 'LBrace', '{', i
        elif char == '}':
            # ans.append('RBrace')
            i += 1
            return 'RBrace', '}', i
        elif char == '+':
            # ans.append('Plus')
            i += 1
            return 'Plus', '+', i
        elif char == '*':
            # ans.append('Mult')
            i += 1
            return 'Mult', '*', i
        elif char == '<':
            # ans.append('Lt')
            i += 1
            return 'Lt', '<', i
        elif char == '>':
            # ans.append('Gt')
            i += 1
            return 'Gt', '>', i
        elif char == '/':
            i += 1
            char = sentense[i]
            if char == '/':
                while i < len(sentense) and sentense[i] != '\n':
                    i += 1
            elif char == '*':
                i += 1
                while (i+1 < len(sentense)) and not (sentense[i] == '*' and sentense[i+1] == '/'):
                    i += 1
                i += 2
            else:
                return 'Div', '/', i
        else:
            # ans.append('Err')
            return 'Err', '', i
    return '', '', ''

if __name__ == '__main__':
    ans = []
    # nextsym(words, i)
    for item in ans:
        print(item)
