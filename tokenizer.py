# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 11:41:42 2022

@author: braxt
"""
from expressionEvaluator import in2post, eval_postfix


KEYWORDS = ['while', 'if', 'elif', 'else', 'for']
TYPES = ['int', 'bool', 'string', 'char']
OPERATIONS = ['+', '-', '*', '/', '%', '=', '!=', '>', '<', '>=', '<=']
SPECIALOPS = ('++', '--')


def tokenize(text):
    lines = text.split('\n')
    variables = []
    tokens = []
    inComment = False
    for i, line in enumerate(lines):
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
            if variables and word in tuple(zip(*variables))[1]:
                tokens.append(('v', word))
                continue
            if tokens[-1][0] == 't':
                if word.endswith(']'):
                    word, size = word[:-1].split('[')
                else:
                    size = 1
                variables.append((tokens[-1][1], word, size))
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
                tokens.append(('a', list(line[1]+'\0')))
            elif line[1][0] == '[':
                expr = line[1]
                part = expr[expr.find('[')+1:].split(']')[0].split(',')
                tokens.append(('a', [eval_postfix(in2post(i, line=i)) for i in part]))
            else:
                tokens.append(('e', in2post(line[1], variables, i+1)))
    return tokens, variables


if __name__ == '__main__':
    tokens, variables = tokenize(open("test.mat").read())
