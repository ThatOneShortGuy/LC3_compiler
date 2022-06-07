# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 11:41:42 2022

@author: braxt
"""
from expressionEvaluator import in2post, eval_postfix


KEYWORDS = ['while', 'if', 'elif', 'else', 'for']
TYPES = ['int', 'bool', 'string', 'char']
OPERATIONS = ['+', '-', '*', '/', '%', '=', '==', '!=', '>', '<', '>=', '<=']


def tokenize(text):
    lines = text.split('\n')
    variables = []
    tokens = []
    for i, line in enumerate(lines):
        line = line.split('=')
        for word in line[0].split(' '):
            if word in tuple(zip(*variables))[1]:
                continue
            if word in TYPES:
                tokens.append(('t', word))
                continue
            if tokens[-1][0] == 't':
                variables.append((tokens[-1][1], word))
                tokens.append(('v', word))
                continue
            raise NameError(f'{word} is not a defined variable on line {i}')
        if len(line) > 1:
            tokens.append(('e', in2post(line[1])))


if __name__ == '__main__':
    tokenize(open("test.mat").read())
