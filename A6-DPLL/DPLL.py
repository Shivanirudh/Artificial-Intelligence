import random

class Clause():
    def __init__(self, no_literals, literals):
        self.no_literals = no_literals
        self.literals = [i for i in literals]
    
    def __str__(self):
        print("{", end = "")
        for i in range(0, self.no_literals):
            print(i, end = " ")
            if i != self.no_literals - 1:
                print("v", end = " ")
        print("}", end = "")
