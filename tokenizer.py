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
    isType = True
    isOp = True
    isKeyword = True
    word = ''
    prev = ''
    ziptypes = tuple(zip(*TYPES))
    zipops = tuple(zip(*OPERATIONS))
    zipkeywords = tuple(zip(*KEYWORDS))
    for line in lines:
        for i, char in enumerate(line):
            if char.startswith('//') or char == '':
                break
            if char == ' ' and not (isType or isOp or isKeyword):
                if not (isType or isOp or isKeyword):
                    variables.append(word)
                tokens.append(((prev := 't' * isType + 'o' * isOp + 'k' * isKeyword), word))
                word = ''
                continue
            isType = isType and char.startswith(ziptypes[i]) and prev != 't' and prev != 'o'
            isOp = isOp and char.startswith(zipops[i])
            isKeyword = isKeyword and char.startswith(zipkeywords[i])
            word += char


if __name__ == '__main__':
    tokenize(open("test.mat").read())
