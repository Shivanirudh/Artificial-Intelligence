"""
Name: Shivanirudh S G
Reg. No: 185001146
"""

import random

"""
- A state is represented as a tuple, where each element represents a paragraph number.
- A state can have a maximum of 9 elements.
- Goal state is the elements of a state in ascending order.
"""

max_goal_state = [i for i in range(1, 10)]
goal_size = random.randint(1, 10)

goal_state = max_goal_state[:goal_size]
print(f'Goal state is: {goal_state}')

initial_state = [i for i in goal_state]
random.shuffle(initial_state)
print(f'Initial state is: {initial_state}')
print("_"*50)

def gen_cutlist(state):
    """
    Generate all possible cutlists of a state, i.e, all possible sublists
    """
    cutlists = []
    n = len(state)
    for l in range(1, n):
        for i in range(n):
            if i + l <= n:
                cutlists.append(state[i:i+l])
    return cutlists

print(f'Possible sublists of [1, 2, 3, 4] are {gen_cutlist([1,2,3,4])}')
print("_"*50)

def cut_paste(state):
    """
    Generate all possible successors of a state for each of the possible cutlists,
    by cutting and pasting them.
    """
    cut_lists = gen_cutlist(state)
    next_states = []
    for cl in cut_lists:
        rem_state = [i for i in state if i not in cl]
        rs_len = len(rem_state)
        cl_len = len(cl)
        for pos in range(rs_len + 1):
            s1, s2 = rem_state[:pos], rem_state[pos:]
            new_state = s1 + list(cl) + s2
            next_states.append(new_state)
    return next_states

print(f'Next states of [1, 2, 3, 4] are: {cut_paste([1,2,3,4])}')

print("_"*50)
"""
BEST FIRST SEARCH

Heuristic: Number of positions out of order
"""

def compute_heuristic_hn(state, goal):
    h_n = 0
    for i in range(len(state)):
        if state[i] != goal[i]:
            h_n += 1
    return h_n

print(f'Heuristic value of [4, 2, 3, 1] is: {compute_heuristic_hn([4,2,3,1], [1, 2, 3, 4])}')
print("_"*50)

class PQueue():
    """
    Priority Queue to order the states
    """

    #initialise the heap
    def __init__(self, initval):
        """
        Initialise the values of the Queue
        """
        self.A = [initval]
        self.n = 0
    
    def printQueue(self):
        """
        Print Queue
        """
        ix = 1
        while ix <= self.n:
            print(str(self.A[ix]), end = '')
            ix += 1
        print()
            
    def insert(self, newOb):
        """
        Insert element into the Priority Queue
        """
        self.n += 1
        self.A.append(Element([0, 1, 2, 3, 4, 5, 6, 7, 8], 100))
        ix = self.n
        while(self.A[ix//2] > newOb):
            self.A[ix] = self.A[ix//2]
            ix//=2
        self.A[ix] = newOb
    
    def isEmpty(self):
        """
        Check if Queue is empty
        """
        if len(self.A) == 0:
            return True
        return False

    def DeleteMin(self):
        """
        Retrieve minimum valued element
        """
        if self.n == 0:
            return None
        minval = self.A[1]
        lastval = self.A[self.n]
        self.n = self.n - 1
        i = 1
        while 2*i < self.n :
            child=2*i
            if child != self.n and self.A[child + 1] < self.A[child]:
                child += 1

            if lastval > self.A[child]:
                self.A[i] = self.A[child]
            else:
                break
            i = child
        self.A[i] = lastval
        return minval

    def rewriteElement(self, newOb):
        """
        Replace node with new cost
        """
        ix = self.A.index(newOb)
        while self.A[ix//2] > newOb:
            self.A[ix] = self.A[ix//2]
            ix //= 2
        self.A[ix] = newOb

class Element():
    """
    Element of the Priority Queue
    """
    def __init__(self, state = None, cost = None):
        self.state = state
        self.cost = cost
    
    def __str__(self):
        ele = ""
        ele += str(self.state) + " "
        ele += str(self.cost)
        return ele 
    
    def __lt__(self, other):
        if self.cost < other.cost:
            return True
        return False
    
    def __gt__(self, other):
        if self.cost > other.cost:
            return True
        return False
    
    def __eq__(self, other):
        if self.state == other.state:
            return True
        return False

def BFS(initial, goal):
    """
    Best First Search algorithm
    """
    Frontier = PQueue(Element([0, 1, 2, 3, 4, 5, 6, 7, 8], -1))
    element_state = tuple(initial)
    level = 1
    Frontier.insert(Element(element_state, compute_heuristic_hn(element_state, goal)))
    Explored = dict()
    while not Frontier.isEmpty():
        level  += 1
        element = Frontier.DeleteMin()
        if not element:
            return list(Explored.keys())

        if element.cost == 0: 
            return list(Explored.keys())

        if tuple(element.state) not in Explored.keys():
            Explored[tuple(element.state)] = 1
            successors = [tuple(i) for i in cut_paste(element.state)]
            for child_state in successors:
                child = Element(child_state, compute_heuristic_hn(child_state, goal))
                if child in Frontier.A:
                    Frontier.rewriteElement(child)
                elif child.state in Explored.keys():
                    Explored[child.state] = 1
                else:
                    Frontier.insert(child)
    return False
print("_"*50)
print("Best First Search")
soln = BFS([2, 4, 1, 5, 3, 6], [1, 2, 3, 4, 5, 6])
if soln:
    print("Number of steps is: " + str(len(soln)))
else:
    print("None")
print("_"*50)
"""
_____________________________________________________________________________________________________________________________
"""
def Astar(initial, goal):
    """
    A* Search algorithm
    """
    Frontier = PQueue(Element([0, 1, 2, 3, 4, 5, 6, 7, 8], -1))
    element_state = tuple(initial)
    level = 1
    Frontier.insert(Element(element_state, level + compute_heuristic_hn(element_state, goal)))
    Explored = dict()
    while not Frontier.isEmpty():
        level  += 1
        element = Frontier.DeleteMin()
        if not element:
            return list(Explored.keys())

        if element.cost == 0: 
            return list(Explored.keys())

        if tuple(element.state) not in Explored.keys():
            Explored[tuple(element.state)] = 1
            successors = [tuple(i) for i in cut_paste(element.state)]
            for child_state in successors:
                child = Element(child_state, level+ compute_heuristic_hn(element_state, goal))
                if child in Frontier.A:
                    Frontier.rewriteElement(child)
                elif child.state in Explored.keys():
                    Explored[child.state] = 1
                else:
                    Frontier.insert(child)
    return False

print("A* search")
soln = Astar([2, 4, 1, 5, 3, 6], [1, 2, 3, 4, 5, 6])
if soln:
    print("Number of steps is: " + str(len(soln)))
else:
    print("None")

"""
Output:
Goal state is: [1, 2]
Initial state is: [2, 1]
__________________________________________________
Possible sublists of [1, 2, 3, 4] are [[1], [2], [3], [4], [1, 2], [2, 3], [3, 4], [1, 2, 3], [2, 3, 4]]
__________________________________________________
Next states of [1, 2, 3, 4] are: [[1, 2, 3, 4], [2, 1, 3, 4], [2, 3, 1, 4], [2, 3, 4, 1], [2, 1, 3, 4], [1, 2, 3, 4], [1, 3, 2, 4], [1, 3, 4, 2], [3, 1, 2, 4], [1, 3, 2, 4], [1, 2, 3, 4], [1, 2, 4, 3], [4, 1, 2, 3], [1, 4, 2, 3], [1, 2, 4, 3], [1, 2, 3, 4], [1, 2, 3, 4], [3, 1, 2, 4], [3, 4, 1, 2], [2, 3, 1, 4], [1, 2, 3, 4], [1, 4, 2, 3], [3, 4, 1, 2], [1, 3, 4, 2], [1, 2, 3, 4], [1, 2, 3, 4], [4, 1, 2, 3], [2, 3, 4, 1], [1, 2, 3, 4]]
__________________________________________________
Heuristic value of [4, 2, 3, 1] is: 2
__________________________________________________
__________________________________________________
Best First Search
Number of steps is: 2
__________________________________________________
A* search
Number of steps is: 2
"""
