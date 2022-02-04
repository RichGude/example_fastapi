# A file for displaying and utilizing simple calcs in order to test testing
def add(num1: int, num2: 2):
    return num1 + num2
def mult(num1: int, num2: 2):
    return num1 * num2
def divid(num1: int, num2: 2):
    return num1 / num2

# Dummy Exception class
class  InsuffientFunds(Exception):
    pass

# Dummy class for testing
class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsuffientFunds("Insufficient funds")
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1