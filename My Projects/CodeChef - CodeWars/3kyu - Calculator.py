"""
Created on Thu 15 Jul 18:07 2021
Finished on Thu 15 Jul 21:00 2021
@author: Cpt.Ender

https://www.codewars.com/kata/5235c913397cbf2508000048

Create a simple calculator that given a string of operators
(), +, -, *, / and numbers separated by spaces returns the value of that expression

Example:
Calculator().evaluate("(2 / 2) + 3 * 4 - 6") # => 7

Remember about the order of operations!
Multiplications and divisions have a higher priority and should be performed left-to-right.
Additions and subtractions have a lower priority and should also be performed left-to-right.
                                                                                             """


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def subtract(a, b):
    return a - b


def add(a, b):
    return a + b


class Calculator:

    def evaluate(self, expression: str):
        order = {'/': divide, '*': multiply, '-': subtract, '+': add}
        while len(expression.split(' ')) != 1:
            # Find parenthesis pairs
            op = -1
            for i, s in enumerate(expression):
                if s == '(':
                    op = i
                elif s == ')':
                    expression = expression[:op] + str(self.evaluate(expression[op + 2:i - 1])) + expression[i + 1:]
                    break

            # if there are no parenthesis
            if op == -1:
                ls = expression.split(' ')
                for i, n in enumerate(ls):
                    if n in order or n == '':
                        pass
                    else:
                        ls[i] = float(ls[i])

                for operation in order:
                    j = 0
                    while j < len(ls):
                        if ls[j] == operation:
                            ls[j - 1] = order[operation](ls[j - 1], ls[j + 1])
                            ls.pop(j)
                            ls.pop(j)
                            j -= 1

                        j += 1
                expression = str(ls[0])
        return int(float(expression)) if int(float(expression)) == float(expression) else float(expression)


calc = Calculator()

print(calc.evaluate("(2 / 2) + 3 * 4 - 6"))
print(calc.evaluate('2 + 3 * 4 / 3 - 6 / 3 * 3 + 8'))
