'''
Stack ADT and functions for creating postfix expressions and evaluating them.
'''


class Stack:
    '''
    Is a stack ADT that has methods for a stack
    '''

    def __init__(self, items=[]):
        self.items = list(items)
        self._size = len(items)

    def __len__(self):
        return self._size

    def push(self, item):
        '''Pushes item onto stack'''
        self.items.append(item)
        self._size += 1

    def pop(self):
        '''remove the top item from the stack and return it.
        Raise an IndexError if the stack is empty.'''
        if self._size == 0:
            raise IndexError
        self._size -= 1
        return self.items.pop()

    def top(self, num=1):
        '''return the top item from the stack without removing it.
        Raise an IndexError if the stack is empty.'''
        if self._size == 0:
            raise IndexError
        return self.items[-num]

    def size(self):
        '''return the number of items on the stack.'''
        return self._size

    def clear(self):
        '''Empty the stack.'''
        self.items = []
        self._size = 0


def in2post(expr, variables=None, line=1):
    '''
    Takes an infix expression as a string and returns an equivalent postfix expression as a list.
    If the expression is not valid, raise a SyntaxError. If the parameter expr is not a list, raise a 
    ValueError. 
    '''
    if not isinstance(expr, str):
        raise ValueError
    if expr == '':
        return ''
    postfix = ['']
    stack = Stack()
    if variables:
        for var, (varType, size) in variables.items():
            expr = expr.replace(var, f"${var}$")
    isChar = False
    isVar = False
    num = True
    for char in expr:
        if char == ' ':
            continue
        if char == '(':
            stack.push(char)
        elif char == '[':
            raise TypeError(f'Arrays are not suppported as constants on line {line}')
        elif char == ')':
            try:
                if postfix[-1]:
                    postfix.append('')
                while stack.top() != '(':
                    if postfix[-1]:
                        postfix.append('')
                    postfix[-1] += stack.pop()
                stack.pop()
            except IndexError:
                raise SyntaxError
        elif char in '+-*/':
            if not postfix[0] and char == '-':
                postfix[0] += '-'
                continue
            while char in '+-' and len(stack) and stack.top() in '+-*/':
                if not postfix[-1]:
                    postfix[-1] += stack.pop()
                else:
                    postfix.append(stack.pop())
            while char in '*/' and len(stack) and stack.top() in '*/':
                if not postfix[-1]:
                    postfix[-1] += stack.pop()
                else:
                    postfix.append(stack.pop())
            stack.push(char)
            num = False
        elif char == "'":
            isChar = not isChar
            if postfix[-1]:
                postfix.append('')
        elif char.isnumeric() or isChar:
            if not num or postfix[-1] and postfix[-1] in '+-*/' and len(postfix) > 1:
                postfix.append('')
            if char.isalpha():
                char = str(ord(char))
            postfix[-1] += char
            num = True
        elif char == '$':
            isVar = not isVar
            if not num or (postfix[-1] and postfix[-1] in '+-*/'):
                postfix.append('')
        elif isVar:
            postfix[-1] += char
        else:
            raise NameError(f'Encountered undefined variable "{expr[expr.find(char):expr[expr.find(char):].find(" ")+1]}" evaluating expression on line {line}')
    while stack.size():
        if not postfix[-1]:
            postfix[-1] += stack.pop()
        else:
            postfix.append(stack.pop())
    return postfix


def eval_postfix(expr, variables=None, line=1):
    '''
    Takes a postfix list as input and returns a number. If the expression is not valid, raise a SyntaxError.
    variables is a dict{string: value} where string is the name and value is the value of the variable
    '''
    if not isinstance(expr, list):
        raise ValueError
    if expr == '':
        return 0
    stack = Stack()
    for char in expr:
        if char == ' ':
            continue
        if char in '+-*/':
            try:
                num2 = stack.pop()
                num1 = stack.pop()
            except IndexError:
                raise SyntaxError
            if char == '+':
                stack.push(num1 + num2)
            elif char == '-':
                stack.push(num1 - num2)
            elif char == '*':
                stack.push(num1 * num2)
            elif char == '/':
                stack.push(num1 / num2)
        else:
            if char.isnumeric():
                stack.push(float(char))
            else:
                for var, d in variables.items():
                    if var == char:
                        stack.push(float(d))
                        break
    return stack.pop()


def eval_expression(expression, variables, constants, reg=None):
    '''
    Evaluate postfix expression in assembly

    Parameters
    ----------
    expression : list
        Postfix expression to be evaluated.
    variables : dict
        Dictionary where the keys are the variable names, and the values are the types and sizes of the variables.

    Returns
    -------
    str
        The assembly code for the given expression.

    '''
    s = []
    stack = Stack()
    if not reg:
        reg = Stack(range(7, -1, -1))
    elif hasattr(reg, '__iter__'):
        reg = Stack(reg)
    for part in expression:
        if part == '':
            continue
        reg0 = f'r{reg.pop()}'
        if part in variables.keys():
            s.append(f'LD {reg0}, {part}')
            stack.push(reg0)
        if (part.isnumeric() or (part[0] == '-' and part[1:].isnumeric)) and part not in constants.keys():
            constants[part] = f'const{"n" if int(part) < 0 else ""}{part if int(part) > 0 else part[1:]}'
        if part.isnumeric() or (part[0] == '-' and part[1:].isnumeric):
            s.append(f'LD {reg0}, const{"n" if int(part) < 0 else ""}{part if int(part) > 0 else part[1:]}')
            stack.push(reg0)
            continue
        if part in '+-*/':
            try:
                num2 = stack.pop()
                num1 = stack.pop()
            except IndexError:
                raise SyntaxError
            if num1.isnumeric():
                reg1 = f'r{reg.pop()}'
                s.append(f'''LD {reg1}, f"const{'n' if num1 < 0 else str()}{abs(num1)}"''')
            else:
                reg1 = num1
                # s.append(f'AND {reg1}, {num1}, #-1')
            if num2.isnumeric():
                reg2 = f'r{reg.pop()}'
                s.append(f'''LD {reg2}, f"const{'n' if num2 < 0 else str()}{abs(num2)}"''')
            else:
                reg2 = num2
                # s.append(f'AND {reg2}, {num2}, #-1')
            if part == '+':
                s.append(f'ADD {reg0}, {reg1}, {reg2}')
            elif part == '-':
                s.extend((f'NOT {reg2}, {reg2}', f'ADD {reg2}, {reg2}, x1', f'ADD {reg0}, {reg1}, {reg2}'))
            elif part == '*':
                s.extend((f'AND {reg0}, {reg1}, x0',
                          # f'ADD {reg1}, {reg2}, x0',
                          f'ADD {reg0}, {reg0}, {reg1}',
                          f'ADD {reg2}, {reg2}, #-1',
                          'BRP #-3'))
            else:
                raise NotImplementedError(f'Function "{part}" is not yet implemented')
            stack.push(reg0)
            reg.push(reg1[1:])
            reg.push(reg2[1:])

    return s, stack.pop()


if __name__ == '__main__':
    post = in2post('2*(abd*df)- 34/(abd *df-6)', {'abd': ('int', 1), 'df': ('int', 1)})
    d = eval_postfix(post, {'abd': 2, 'df': -3})
