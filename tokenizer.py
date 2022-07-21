"""
Created on Sun Jun  5 11:41:42 2022

@author: braxbrowndog@gmail.com

Compiler for the LC-3 assembly language.
"""
from lib2to3.pgen2 import token
from expressionEvaluator import in2post, eval_postfix


KEYWORDS = ['while', 'if', 'elif', 'else', 'for']
TYPES = ['int', 'bool', 'string', 'char']
OPERATIONS = ['+', '-', '*', '/', '%', '=', '!=', '>', '<', '>=', '<=']
SPECIALOPS = ('++', '--')


def tokenize(text):
    lines = text.split('\n')
    variables = dict()
    # functions = dict()
    tokens = []
    inComment = False
    # inFunc = False
    # funcDef = False
    for i, line in enumerate(lines):
        # if line.startswith('\t'):
        #     line = line[1:]
        #     if funcDef:
        #         funcDef = False
        #         inFunc = True
        # elif inFunc and not line.startswith('\t'):
        #     inFunc = False
        if line.startswith('//'):
            continue
        if line.startswith('/*'):
            inComment = True
            continue
        if line.endswith('*/'):
            inComment = False
            continue
        if inComment:
            continue
        line = line.split('=')
        for word in line[0].split(' '):
            if not word:
                continue
            if word in TYPES:
                tokens.append(('t', word))
                continue
            if variables and word in variables.keys():
                tokens.append(('v', word))
                continue
            # if tokens[-1][0] == 't' and word.startswith('('):
            
            #     '''This is a function definition'''
            #     if word[1:-1] in functions.keys():
            #         raise SyntaxError(f'Function {word[1:-1]} already defined on line {i+1}')
            #     funcDef = True
            #     tokens.append(('f', word[1:-1]))
            #     functions[word[1:-1]] = [tokens[-1][1]]
            #     continue
            # if funcDef and word in TYPES:
            #     functions[tokens[-1][1]].append(word)
            #     continue
            # if funcDef and functions[tokens[-1][1]][-1] in TYPES:
            #     functions[tokens[-1][1]].append(word)
            #     continue
            # if funcDef:
            #     raise SyntaxError(f'Invalid function ({tokens[-1][1]}) definition on line {i+1}')
            # if inFunc:

            if tokens[-1][0] == 't':
                if word.endswith(']'):
                    word, size = word[:-1].split('[')
                else:
                    size = 1
                variables[word] = tokens[-1][1], int(size)
                tokens.append(('v', word))
                continue
            if word.startswith(SPECIALOPS):
                op = '++' if word[0] == '+' else '--'
                tokens.extend((('o', op), word[word.find(op):]))
                continue
            elif word.endswith(SPECIALOPS):
                op = '++' if word[-1] == '+' else '--'
                tokens.extend((('v', word[:word.find(op)]), ('o', op)))
                continue
            if word in OPERATIONS:
                tokens.append(('o', word+'='))
                continue
            raise NameError(f'{word} is not a defined variable on line {i}')
        if len(line) > 1:
            line[1] = line[1].strip()
            if line[1].startswith('"'):
                line[1] = line[1].replace('"', '')
                variables[tokens[-1][1]] = variables[tokens[-1][1]][0], len(line[1])+1
                tokens.append(('a', list(line[1]+'\0')))
            elif line[1][0] == '[':
                expr = line[1]
                part = expr[expr.find('[')+1:].split(']')[0].split(',')
                if not expr[1].isnumeric():
                    variables[line[0].split(' ')[1]] = len(eval(expr))
                tokens.append(('a', [eval_postfix(in2post(i, line=i)) for i in part]))
            else:
                tokens.append(('e', in2post(line[1], variables, i+1)))
    return tokens, variables


if __name__ == '__main__':
    tokens, variables = tokenize(open("test.mat").read())
