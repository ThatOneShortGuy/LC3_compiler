"""
Created on Sun Jun  5 11:41:42 2022

@author: braxbrowndog@gmail.com

Compiler for the LC-3 assembly language.
"""
from expressionEvaluator import in2post, eval_postfix, eval_expression


KEYWORDS = ['while', 'if', 'elif', 'else', 'for']
TYPES = ['int', 'bool', 'string', 'char']
OPERATIONS = ['+', '-', '*', '/', '%', '=', '!=', '>', '<', '>=', '<=']
SPECIALOPS = ('++', '--')


def makeAsm(tokens, variables, constants) -> str:
    '''
    Returns ASM code for the given tokens.

    Parameters
    ----------
    tokens : list
        List of tokens.
    variables : dict
        Dictionary where the keys are the variable names, and the values are the types and sizes of the variables.

    Returns
    -------
    str
        ASM code for the given tokens.

    '''
    s = []
    if tokens[0][0] == 't':
        dtype = tokens[0][1]
        var, size = variables[tokens[1][1]]
        expr = tokens[2][1]
        if size > 1:
            for i in range(size):
                variables(f'{var}{i if i else ""}\t.FILL {expr}')
        else:
            c, reg = eval_expression(expr, variables, constants)
            s.extend(c)

    return s


def generateAsmFile(tokens, variables, filename='a'):
    constants = dict()
    inner = []
    inner.extend(makeAsm(tokens[:3], variables, constants))
    with open(f'{filename}.asm', 'w') as f:
        f.write('.ORIG x3000\n')
        f.write(f'\tJSR #{len(constants)+len(variables)}\n')
        f.write('\n'.join(c for c in constants.values())+'\n')
        f.write('\n'.join(f'{v}\t.BLKW #{s}' for v, (_, s) in variables.items())+'\n\t')
        f.write('\n\t'.join(v for v in inner)+'\n')
        f.write(open('includes/Stack.asm').read())
        f.write('\n.END')


def tokenize(text):
    lines = text.split('\n')
    variables = dict()
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
            if variables and word in variables.keys():
                tokens.append(('v', word))
                continue
            if tokens[-1][0] == 't':
                if word.endswith(']'):
                    word, size = word[:-1].split('[')
                else:
                    size = 1
                variables[word] = tokens[-1][1], size
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
                if not expr[1].isnumeric():
                    variables[line[0].split(' ')[1]] = len(eval(expr))
                tokens.append(('a', [eval_postfix(in2post(i, line=i)) for i in part]))
            else:
                tokens.append(('e', in2post(line[1], variables, i+1)))
    return tokens, variables


if __name__ == '__main__':
    tokens, variables = tokenize(open("test.mat").read())
    generateAsmFile(tokens, variables)
