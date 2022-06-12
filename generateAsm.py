from expressionEvaluator import eval_expression
from tokenizer import tokenize


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
        var = tokens[1][1]
        size = variables[var][1]
        expr = tokens[2][1]
    elif tokens[0][0] == 'v':
        var = tokens[0][1]
        size = variables[var][1]
        expr = tokens[1][1]
    if size > 1:
        # Handle for arrays (potenially could allow expressions in the array)
        s.append(f'LEA r0, {var}')
        for i in range(size):
            c, reg = eval_expression(str(int(expr[i])), variables, constants, range(8, 0, -1))
            s.extend(c)
            s.append(f'STR {reg}, r0, #{i}')
    else:
        c, reg = eval_expression(expr, variables, constants)
        s.extend(c)
        # Assign the register in reg in variable
        s.append(f'ST {reg}, {var}')

    return s


def generateAsmFile(tokens, variables, filename='a'):
    constants = dict()
    inner = []
    send = []
    for token in tokens:
        if token[0] == 't':
            continue
        elif not send or token[0] == 'v' and send[-1][0] != 'v':
            send.append(token)
        elif send and send[-1][0] == 'v' and token[0] == 'v':
            send[0] = token
        elif token[0] in 'ea':
            send.append(token)
            inner.extend(makeAsm(send, variables, constants))
            send = []
    with open(f'{filename}.asm', 'w') as f:
        f.write('.ORIG x3000\n')
        f.write(f'\tJSR #{len(constants)+sum(tuple(zip(*variables.values()))[1])}\n')
        f.write('\n'.join(c for c in constants.values())+'\n')
        f.write('\n'.join(f'{v}\t.BLKW #{s}' for v, (_, s) in variables.items())+'\n\t')
        f.write('\n\t'.join(v for v in inner)+'\n')
        # f.write(open('includes/Stack.asm').read())
        f.write('\n.END')


if __name__ == '__main__':
    tokens, variables = tokenize(open('test.mat').read())
    generateAsmFile(tokens, variables)
