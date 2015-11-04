# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:#it's an abstract class
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]
    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from game import Directions #import directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    start = problem.getStartState()# gets the initial state of the pacman from problem.py
    if problem.isGoalState(start):#if start state and goal state are same then the goal has been reached before dfs
        return []                   #so  so return as there is no point in any search
    from util import Stack      #import stack data structure.
    statesStack = Stack()       #make a stack,stack is used in dfs since you can keep pushing elements to the stack from top, so newer elements are on top i.e the children of recently explored state. so stack is use in dfs
    exploredSet = set([start])   #create a python (AND Mathemaical) set to store the currently explored states. In this cas this is only the start state
    tup = (start,[])            #create a tuple with start state and empty list and .this comes in handy in returning the actual path. store it in the stack
    statesStack.push(tup)   
    while not statesStack.isEmpty():#keep iterating while stack is not empty
        tup1 = statesStack.pop()    #remove top item from stack
        state = tup1[0] #the current state
        path = tup1[1]  #the list`
        if problem.isGoalState(state):# return the list of states between the start and the goal state if goal is found
            return path
        successors = problem.getSuccessors(state)#For a given state, this should return a list of triples,(successor, action, stepCost), where 'successor' is asuccessor to the current state, 'action' is the action required to get there, and 'stepCost' is the incremental cost of expanding to that successor
        for succ in successors:#for all children of the current state.
            coor = succ[0]#the child name/coordinates
            move = succ[1]#action required to get to the child
            tempPath = list(path)#create a new seperate list from another list, ie deep copy
            if not coor in exploredSet:#checks if we are going in an infinite loop. ie if child/coordinate not in explored set
                exploredSet.add(coor)#add them
                if move == 'North':#the if conditions check the next move required to get to the next state.north, south, east, west directions and add the direction to the new path list
                    tempPath.append(n)
                elif move == 'East':
                    tempPath.append(e)
                elif move == 'South':
                    tempPath.append(s)
                elif move == 'West':
                    tempPath.append(w)
                statesStack.push((coor,tempPath))#add the state with it's explored path to stack for further dfs            
    return []#if nothing found return null#nodes expanded, tiny=14, medium=144, big=390
    
    
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []
    from util import Queue
    statesQueue = Queue()
    exploredSet = set([start])
    tup = (start,[])
    statesQueue.push(tup)
    while not statesQueue.isEmpty():
        tup1 = statesQueue.pop()
        state = tup1[0]
        path = tup1[1]
        if problem.isGoalState(state):
            return path
        successors = problem.getSuccessors(state)
        for succ in successors:
            coor = succ[0]
            move = succ[1]
            tempPath = list(path)
            if not coor in exploredSet:
                exploredSet.add(coor)
                if move == 'North':
                    tempPath.append(n)
                elif move == 'East':
                    tempPath.append(e)
                elif move == 'South':
                    tempPath.append(s)
                elif move == 'West':
                    tempPath.append(w)
                statesQueue.push((coor,tempPath))
    return []#nodes expanded, tiny=15, medium=269, big=620

def depthLimitedSearch(problem,depth_limit,start,s,w,n,e,statesStack):
    exploredSet = set([start])
    tup = (start,[])
    statesStack.push(tup)
    full_graph_explored=True;
    while not statesStack.isEmpty():
        tup1 = statesStack.pop()
        state = tup1[0]
        path = tup1[1]
        if problem.isGoalState(state):
            return path,full_graph_explored
        if(len(path)>=depth_limit):
            full_graph_explored=False#if it never comes in this part. this means that depth_limit is bigger than out tree depth and we have explored all the nodes
            continue            
        successors = problem.getSuccessors(state)
        for succ in successors:
            coor = succ[0]
            move = succ[1]
            tempPath = list(path)
            if not coor in exploredSet:
                exploredSet.add(coor)
                if move == 'North':
                    tempPath.append(n)
                elif move == 'East':
                    tempPath.append(e)
                elif move == 'South':
                    tempPath.append(s)
                elif move == 'West':
                    tempPath.append(w)
                statesStack.push((coor,tempPath))
    return [],full_graph_explored
    
def iterativeDeepeingSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []
    full_graph_explored=False;
    depth=1;
    from util import Stack
    statesStack = Stack()
    while not full_graph_explored:# this means that still depth<graph_depth
        path,full_graph_explored=depthLimitedSearch(problem,depth,start,s,w,n,e,statesStack)
        if len(path)>0:
            print "The optimal depth is: "+str(depth)
            return path
        depth+=1;
    """
    #code for optimal depth.
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []
    full_graph_explored=False;
    from util import Stack
    statesStack = Stack()
    depth=210
    path,full_graph_explored=depthLimitedSearch(problem,depth,start,s,w,n,e,statesStack)
    return path
    #THE NODES EXPANDED FOR 210 alone are 364.
    """
    #THE NODES EXPANDED FOR 210 alone are 364.
    return[]#optimal depth=210,total nodes expanded for bigmaze=60211(for 210 alone, 364 nodes expanded). 
    
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []
    from util import PriorityQueue,PriorityQueueWithFunction
    statesPriorityQueue = PriorityQueue()
    exploredSet = set([start])
    tup = (start,[])
    statesPriorityQueue.push(tup,heuristic(start,problem))
    while not statesPriorityQueue.isEmpty():
        tup1 = statesPriorityQueue.pop()
        state = tup1[0]
        path = tup1[1]
        if problem.isGoalState(state):
            return path
        successors = problem.getSuccessors(state)
        for succ in successors:
            coor = succ[0]
            move = succ[1]
            stepCost=succ[2]
            tempPath = list(path)
            if not coor in exploredSet:
                exploredSet.add(coor)
                if move == 'North':
                    tempPath.append(n)
                elif move == 'East':
                    tempPath.append(e)
                elif move == 'South':
                    tempPath.append(s)
                elif move == 'West':
                    tempPath.append(w)
                costSoFar=len(path)#assuming step cost=constant AND THIS IS BECAUSE WE ARE NOT ALLOW TO CHANGE POP FUNCTION of the priority queue, else we could have just added the priority of parent as cost so far
                totalCost=stepCost+heuristic(coor,problem)+costSoFar 
                statesPriorityQueue.push((coor,tempPath),totalCost)
    return []#nodes expanded, tiny=15, medium=269, big=620
    

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ids = iterativeDeepeingSearch
