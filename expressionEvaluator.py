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

def in2post(expr):
    '''
    Takes an infix expression as a string and returns an equivalent postfix expression as a string.
    If the expression is not valid, raise a SyntaxError. If the parameter expr is not a string, raise a 
    ValueError. 
    '''
    if not isinstance(expr, str):
        raise ValueError
    if expr == '':
        return ''
    postfix = ''
    stack = Stack()
    for char in expr:
        if char == ' ':
            continue
        if char == '(':
            stack.push(char)
        elif char == ')':
            try:
                while stack.top() != '(':
                    postfix += stack.pop()
                stack.pop()
            except IndexError:
                raise SyntaxError
        elif char in '+-*/':
            while char in '+-' and len(stack) and stack.top() in '+-*/':
                postfix += stack.pop()
            while char in '*/' and len(stack) and stack.top() in '*/':
                postfix += stack.pop()
            stack.push(char)
        else:
            postfix += char
    while stack.size():
        postfix += stack.pop()
    return postfix

def eval_postfix(expr):
    '''
    Takes a postfix string as input and returns a number. If the expression is not valid, raise a SyntaxError.
    '''
    if not isinstance(expr, str):
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
            stack.push(float(char))
    return stack.pop()
