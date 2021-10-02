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


def checkAlpha(chr):
    return chr == '_' or chr.isalpha()


def edit():
    file = open(sys.argv[1])
    lines = file.readlines()
    for line in lines:
        i = 0
        while i < len(line):
            token = ''
            i = getNbc(line, i)
            if i >= len(line):
                break
            char = line[i]
            if checkAlpha(char):
                while checkAlpha(char) or char.isdigit():
                    token += char
                    i += 1
                    char = line[i]
                # i -= 1
                if token in keyword:
                    ans.append(keyword[token])
                else:
                    ans.append('Ident({})'.format(token))
            elif char.isdigit():
                while char.isdigit():
                    token += char
                    i += 1
                    char = line[i]
                ans.append('Number({})'.format(token))
            elif char == '=':
                i += 1
                char = line[i]
                if char == '=':
                    ans.append('Eq')
                    i += 1
                else:
                    ans.append('Assign')
            elif char == ';':
                ans.append('Semicolon')
                i += 1
            elif char == '(':
                ans.append('LPar')
                i += 1
            elif char == ')':
                ans.append('RPar')
                i += 1
            elif char == '{':
                ans.append('LBrace')
                i += 1
            elif char == '}':
                ans.append('RBrace')
                i += 1
            elif char == '+':
                ans.append('Plus')
                i += 1
            elif char == '*':
                ans.append('Mult')
                i += 1
            elif char == '/':
                ans.append('Div')
                i += 1
            elif char == '<':
                ans.append('Lt')
                i += 1
            elif char == '>':
                ans.append('Gt')
                i += 1
            else:
                ans.append('Err')
                return


if __name__ == '__main__':
    ans = []
    edit()
    for item in ans:
        print(item)
