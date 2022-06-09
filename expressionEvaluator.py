'''
Stack ADT and functions for creating postfix expressions and evaluating them.
'''


class Stack:
    '''
    Is a stack ADT that has methods for a stack
    '''

    def __init__(self):
        self.items = []
        self._size = 0

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

    def top(self):
        '''return the top item from the stack without removing it.
        Raise an IndexError if the stack is empty.'''
        if self._size == 0:
            raise IndexError
        return self.items[-1]

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
            expr = expr.replace(var, f"'{var}'")
    isVar = False
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
                    postfix[-1] += stack.pop()
                stack.pop()
            except IndexError:
                raise SyntaxError
        elif char in '+-*/':
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
        elif char == "'":
            isVar = not isVar
            if postfix[-1]:
                postfix.append('')
        elif char.isnumeric() or isVar:
            if postfix[-1] and postfix[-1] in '+-*/':
                postfix.append('')
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


if __name__ == '__main__':
    post = in2post('2*(abd*df)- 34/(abd *df-6)', {'abd': ('int', 1), 'df': ('int', 1)})
    d = eval_postfix(post, {'abd': 2, 'df': -3})
