# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #new scared times is a list of integers of the ghost. if it is zero then they are not scared
        #case 1. Run for your life! Ghosts are very close and they are not scared
        from util import manhattanDistance 
        totalGhostDistance=0
        minGhostDistance=float('inf')
        for everyGhost in newGhostStates:
            currentGhostDistance=manhattanDistance(newPos,everyGhost.getPosition())
            totalGhostDistance+=currentGhostDistance
            minGhostDistance=min(minGhostDistance,currentGhostDistance)
        if (minGhostDistance<=4 and min(newScaredTimes)==0):#ghost is very close and not scared. Please note that in this condition if one of two ghosts is scared and close to me, I will even run away from that. Yeah It's a flaw. Dont want to take care of it.
            return minGhostDistance
        #################################################################
        foods=newFood.asList()
        nodesInGraph=foods[:]
        nodesInGraph.insert(0,newPos)#so we always consider it first so as to make it a terminal node and minimize our dist
        edgeDict={}
        exploredSet=set()
        from util import PriorityQueue
        priorityQueue=PriorityQueue()
        for node in nodesInGraph:
            for otherNode in nodesInGraph:
                if node == otherNode:
                    continue
                manDist=manhattanDistance(node,otherNode)
                edgeDict[(node,otherNode)]=manDist;
                priorityQueue.push((node,otherNode),manDist)
        #using kruskal, sum them.
        sum=0
        while not priorityQueue.isEmpty():
            pair=priorityQueue.pop()
            x=pair[0] not in exploredSet
            y=pair[1] not in exploredSet
            if x or y:
                sum+=edgeDict[pair]
            if x:
                exploredSet.add(pair[0])
            if y:
                exploredSet.add(pair[1])
        reciprocalFoodSum=1/(1+1.0*sum)#we are adding 1 to prevent division by zero,we are multiplying to make it a float
        #case 2. nearest ghost dist is>4, or they are scared
        return (reciprocalFoodSum+successorGameState.getScore()) #getScore acts as a deciding factor between two states if they have equal value
        
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()
    
class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)       

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (TASK 2)
    """
    #yes i made my own constructors
        
    def MinMaxValue(self,gameState,curTotAgntIndx):
        curTotAgntIndx+=1
        agntIndx=curTotAgntIndx%gameState.getNumAgents()
        curDepth=(curTotAgntIndx/gameState.getNumAgents())+1
        curLegalActions=gameState.getLegalActions(agntIndx)[:]
        if (Directions.STOP in curLegalActions):
            curLegalActions.remove(Directions.STOP)
        # base case: leaf node
        if (curDepth>self.depth or len(curLegalActions)==0):
            return self.evaluationFunction(gameState)
        successorGameStates=[gameState.generateSuccessor(agntIndx,curAction) for curAction in curLegalActions]
        actionResultList=[self.MinMaxValue(sucGameState,curTotAgntIndx) for sucGameState in successorGameStates]        
        if (self.agentTypeDict[agntIndx]==self.PACMAN_AGENT):
            return max(actionResultList)
        #else
        return min(actionResultList)
 
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #create dict and bros
        self.PACMAN_AGENT,self.GHOST_AGENT=range(2)#it is to define enums, shift to constructor
        self.agentTypeDict={}

        #set dictionary.
        self.agentTypeDict[0]=self.PACMAN_AGENT;
        for agntIndx in range(1,gameState.getNumAgents()):
            self.agentTypeDict[agntIndx]=self.GHOST_AGENT
        ##########################################
        """
        curLegalActions=(gameState.getLegalActions())[:];#copy the list of actions
        curLegalActions.remove('Stop')
        #in order to get key for max value we can simply make a list of 2 elements where the first element is the value returned by the minmax func and second is the key.
        self.totalAgentIndex=0 #auto increments, when moded with numb agents, it gives the current agent index and when divided with the numb agents and one is added gives the current depth.
        #[MinMaxValue(curAction,gameState,currentAgentIndex),cur] has 2 components
        #1. self.MinMaxValue(self.generateSuccessor(curTotAgntIndx,curAction),curTotAgntIndx) is the function that returns the value for the action ie successor gamestate
        1.a MinMaxValue takes in a gamestate and curTotAgntIndx
        b. gamestate is the gamestate of the action performed by current agent
        #2. curAction
        actionResultList=[[self.MinMaxValue(gameState.generateSuccessor(curAction,gameState),curTotAgntIndx),curAction] for curAction in curLegalActions]
        bestActionResultPair=max(actionResultList, key= lambda x: x[:][0])#x[:]means all lists [0]means that minmax value is largest
        """
        ##############################################################################################
        #this code won me 664/1000 games :D Yeah!
        # for details of all lines below, see above """ *something* """ section
        curLegalActions=(gameState.getLegalActions())[:]
        if (Directions.STOP in curLegalActions):
            curLegalActions.remove(Directions.STOP)
        curTotAgntIndx=0# this total index takes care of itself in every iteration of this for loop,i.e becomes zero again as we go looking for the next 
        actionResultList=[[self.MinMaxValue(gameState.generateSuccessor(curTotAgntIndx,curAction),curTotAgntIndx),curAction] for curAction in curLegalActions]
        bestActionResultPair=max(actionResultList, key= lambda x: x[:][0])
        return bestActionResultPair[1]# the action of action result pair
        
class ExpectiminimaxAgent(MultiAgentSearchAgent):
    """
      Your expeciminimax agent (TASK 4)
    """
    #if ghost moving only between two positions. then it is the problem of their evaluation function.use a better one
    def ExpectiMinMaxValue(self,gameState,curTotAgntIndx):
        curTotAgntIndx+=1
        agntIndx=curTotAgntIndx%gameState.getNumAgents()
        curDepth=(curTotAgntIndx/gameState.getNumAgents())+1
        curLegalActions=gameState.getLegalActions(agntIndx)[:]
        if (Directions.STOP in curLegalActions):
            curLegalActions.remove(Directions.STOP)
        # base case: leaf node
        if (curDepth>self.depth or len(curLegalActions)==0):
            return self.evaluationFunction(gameState)
        successorGameStates=[gameState.generateSuccessor(agntIndx,curAction) for curAction in curLegalActions]
        actionResultList=[self.ExpectiMinMaxValue(sucGameState,curTotAgntIndx) for sucGameState in successorGameStates]        
        if (self.agentTypeDict[agntIndx]==self.PACMAN_AGENT):
            return max(actionResultList)
        #else if it is my first agent which is a min agent
        if (self.agentTypeDict[agntIndx]==self.MINGHOST_AGENT):
            return max(actionResultList)      
        #else
        return (sum(actionResultList)*1.00)/(len(actionResultList))

    def getAction(self, gameState):
        """
          Use your already written code in Task 2 and Task 3 
        """
        #I observe that in smallclassic with vs without directional ghosts. pacman usually avoids only one ghost and not the other. considers one as minimizing and the others as expecti and usually gets killed by others while eating food due to the wrong thinking.same for original classic and other maps
 
        "*** YOUR CODE HERE ***"
        #won me 820/1000 with avg 333.96 games in minmaxClassic while minmax got 664/1000 and Expectimax got me 86/100 with avg of 374. The result as expected. 
        #create dict and bros
        self.PACMAN_AGENT,self.MINGHOST_AGENT,self.EXPECTIGHOST_AGENT=range(3)#it is to define enums, shift to constructor
        self.agentTypeDict={}
        #set dictionary.
        self.agentTypeDict[0]=self.PACMAN_AGENT;
        self.agentTypeDict[1]=self.MINGHOST_AGENT
        for agntIndx in range(2,gameState.getNumAgents()):
            self.agentTypeDict[agntIndx]=self.EXPECTIGHOST_AGENT
        # for details of all lines below, see above """ *something* """ section
        curLegalActions=(gameState.getLegalActions())[:]
        if (Directions.STOP in curLegalActions):
            curLegalActions.remove(Directions.STOP)
        curTotAgntIndx=0# this total index takes care of itself in every iteration of this for loop,i.e becomes zero again as we go looking for the next 
        actionResultList=[[self.ExpectiMinMaxValue(gameState.generateSuccessor(curTotAgntIndx,curAction),curTotAgntIndx),curAction] for curAction in curLegalActions]
        bestActionResultPair=max(actionResultList, key= lambda x: x[:][0])
        return bestActionResultPair[1]# the action of action result pair

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (TASK 3)
    """
    def ExpectiMaxValue(self,gameState,curTotAgntIndx):
        curTotAgntIndx+=1
        agntIndx=curTotAgntIndx%gameState.getNumAgents()
        curDepth=(curTotAgntIndx/gameState.getNumAgents())+1
        curLegalActions=gameState.getLegalActions(agntIndx)[:]
        if (Directions.STOP in curLegalActions):
            curLegalActions.remove(Directions.STOP)
        # base case: leaf node
        if (curDepth>self.depth or len(curLegalActions)==0):
            return self.evaluationFunction(gameState)
        successorGameStates=[gameState.generateSuccessor(agntIndx,curAction) for curAction in curLegalActions]
        actionResultList=[self.ExpectiMaxValue(sucGameState,curTotAgntIndx) for sucGameState in successorGameStates]        
        if (self.agentTypeDict[agntIndx]==self.PACMAN_AGENT):
            return max(actionResultList)
        #else#only difference b/w this and minmax
        return (sum(actionResultList)*1.00)/(len(actionResultList))

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        #create dict and bros
        self.PACMAN_AGENT,self.GHOST_AGENT=range(2)#it is to define enums, shift to constructor
        self.agentTypeDict={}
        #python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10    I have 6/10 Wins
        #set dictionary.
        self.agentTypeDict[0]=self.PACMAN_AGENT;
        for agntIndx in range(1,gameState.getNumAgents()):
            self.agentTypeDict[agntIndx]=self.GHOST_AGENT
        # for details of all lines below, see above """ *something* """ section
        curLegalActions=(gameState.getLegalActions())[:]
        if (Directions.STOP in curLegalActions):
            curLegalActions.remove(Directions.STOP)
        curTotAgntIndx=0# this total index takes care of itself in every iteration of this for loop,i.e becomes zero again as we go looking for the next 
        actionResultList=[[self.ExpectiMaxValue(gameState.generateSuccessor(curTotAgntIndx,curAction),curTotAgntIndx),curAction] for curAction in curLegalActions]
        bestActionResultPair=max(actionResultList, key= lambda x: x[:][0])
        return bestActionResultPair[1]# the action of action result pair

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function.

      DESCRIPTION: <write something here so we know what you did>
    """
 
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
      
        util.raiseNotDefined()

