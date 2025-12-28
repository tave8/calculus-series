"""
Reverse Polish Notation algorithm.

Evaluates a string of valid RPN (Reverse Polish Notation)
expressions, where the operands are integers and the operators
are the symbols + - * /


    "Reverse Polish Notation (RPN), or postfix notation, 
    is a way to write math expressions where the operator 
    comes after its numbers (operands), like 2 3 + instead of 2 + 3, 
    eliminating the need for parentheses and simplifying evaluation 
    by computers using a stack."

    - Wikipedia


Examples: 

IN: 4 1 +
OUT: 5

IN: 6 3 + 5 -
OUT: 4

IN: 10 5 + 4 - 3 * 11 /
OUT: 3


author: Giuseppe Tavella
"""


import math

def RPN(string):
    return reversePolishNotation(
        reversePolishNotationParser(string)
    )


def reversePolishNotationParser(string):
    return string.split(" ")


def reversePolishNotation(tokens):

    # [
    #   {
    #     tokenType: str [operator | operand]
    #     value: int | str
    #   }
    # ]
    stack = []

    for token in tokens:
        # do the math operation between the stack[-2] element
        # and the stack[-1] element, with this operator
        # push this output onto the stack
        # token is an operator
        if isTokenOperator(token):
            stack.append({
                "tokenType": "operator",
                "value": token
            })
            # print(stack)
            calcExpressionFromStack(stack)
        # if this token is an operand
        else:
            stack.append({
                "tokenType": "operand",
                "value": int(token)
            })
            
    # when we are done, there will be only element in the stack
    return stack[0]["value"]


def calcExpressionFromStack(stack):
    ret = None
    operator = stack[-1]["value"]
    operandRight = stack[-2]["value"]
    operandLeft = stack[-3]["value"]

    if operator == "+":
        ret = operandLeft + operandRight
    elif operator == "-":
        ret = operandLeft - operandRight
    elif operator == "*":
        ret = operandLeft * operandRight
    elif operator == "/":
        ret = math.trunc(operandLeft / operandRight)
    
    stack.pop()
    stack.pop()
    stack.pop()
    
    stack.append({
        "tokenType": "operand",
        "value": ret
    })



def isTokenOperator(token):
    return token in ["+", "-", "*", "/"]



text1 = "4 1 +"
text2 = "6 3 + 5 -"
text3 = "10 5 + 4 - 3 * 11 /"

print(RPN(text1)) # 5
print(RPN(text2)) # 4
print(RPN(text3)) # 3




