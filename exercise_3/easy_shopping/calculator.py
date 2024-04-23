class Calculator:
    def __init__(self):
        pass

    def add(self, a, b):
        if type(a) == int and type(b) == int: # Check type of input
            return a + b
        else:
            return 'Not a number given'
    
    def subtract(self, a, b):
        if type(a) == int and type(b) == int: # Check type of input
            return a - b
        else:
            return 'Not a number given'
    
    def multiply(self, a, b):
        if type(a) == int and type(b) == int: # Check type of input
            return a * b
        else:
            return 'Not a number given'
    
    def divide(self, a, b):
        try: # Try to catch division by zero
            return a / b 
        except:
            return 'Not a valid number'