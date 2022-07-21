# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 16:53:47 2022

@author: braxton.brown
"""

BUILTINS = ['print', 'input']


def printFunc(tokens, variables, constants, speedEfficient=True):
    s = []
    if tokens[0] == 'a':    # Handle for constants
        arr = tokens[1]
        if not speedEfficient:  # Should only be used in programs where there are multiple contants being used in the print
            for char in arr:
                char = ord(char)
                constants[char] = f'const{"n" if char < 0 else ""}{char}'
                '''OUT is the trap call to print char in r0 to console'''
                s.extend((f'LD r0, {constants[char]}',
                          'OUT'))
        else:
            varName = ''.join(arr)
            s.extend(('LEA r0, x1',
                      f'JSR #{len(varName)}'))
            s.extend(f'.FILL #{ord(char)}' for char in arr)
            s.append('PUTS')
    elif tokens[0] == 'v':  # Handle for variables
        if (varName := tokens[1]) not in variables:
            raise NameError(f'"{varName}" is not a defined variable')
        dtype, size = variables[varName]
        if dtype == 'string':
            s.extend((f'LEA r0, {varName}', 'PUTS'))
        elif dtype == 'char':
            s.extend((f'LD r0, {varName}', 'OUT'))
        elif dtype == 'int':
            '''Convert the value in varName as an int into the string representation of the int via assembly'''
            constants['45'] = 'const45'
            s.extend([f'LD r2, {varName}']+open('includes/Int2Str.asm').read().split('\n')[1:])
    return s


def funcHandler(tokens, variables, constants):
    if tokens[0][1] == 'print':
        return printFunc(tokens[1], variables, constants)
