# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        # print("succesor",successorGameState)
        # print("newPos",newPos)
        # print("newFood",newFood)
        # print("newGhostStates",newGhostStates)
        # print("newScaredTimes",newScaredTimes)
        #add food location factor
        scared = False
        foodleft = currentGameState.getFood().count()
        FoodDistance = 99999
        if foodleft == 0:
            FoodDistance = 1
        else:
            for food in currentGameState.getFood().asList():
                # print("n",newPos)
                # print("f",food)
                curr  = manhattanDistance(newPos,food)
                if curr < FoodDistance:
                    FoodDistance = curr
        # add ghost factor
        # Ghostpositions = newGhostStates.getGhostPositions()
        GhostDistance = 999
        for ghost in newGhostStates:
            # print(ghost.getPosition())
            curr = manhattanDistance(newPos,ghost.getPosition())
            if curr < GhostDistance:
                GhostDistance = curr
        maxScaredTime = max(newScaredTimes)
        
        # print(GhostDistance/FoodDistance)
    
        # if scared:
        #     return successorGameState.getScore()+0.7*GhostDistance+1/FoodDistance
        # else:
        #     return successorGameState.getScore()-7/(GhostDistance+1)+1/FoodDistance
        # print(foodleft)
        # print("f",FoodDistance)
        # print("g",GhostDistance)
        return  5/(FoodDistance+0.1)-20/(GhostDistance+0.1)

def scoreEvaluationFunction(currentGameState: GameState):
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
    Your minimax agent (question 2)
    """
    def minimizer(self,gameState: GameState,agentIndex,curdepth=1):
        print("min")
        finalVal = 9999999
        finalAct = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)
        nextAgent = agentIndex+1
        nextDepth = curdepth
        if agentIndex == gameState.getNumAgents()-1:
            nextAgent = 0
            nextDepth = curdepth+1
        for act in actions:
            successor = gameState.generateSuccessor(agentIndex,act)
            currentVal,_ = self.value(successor,nextAgent,nextDepth)
            if currentVal < finalVal:
                finalVal = currentVal
                finalAct = act
        # print(finalVal,finalAct)
        return finalVal, finalAct
    
    def maximizer(self,gameState: GameState,agentIndex, curdepth=1):
        # print("max")
        finalVal = -9999999
        finalAct = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)
        for act in actions:
            # print(act)
            successor = gameState.generateSuccessor(agentIndex,act)
            currentVal,_ = self.value(successor,1,curdepth)
            # print(currentVal)
            if currentVal > finalVal:
                finalVal = currentVal
                finalAct = act
        # print(finalVal,finalAct)
        return finalVal, finalAct
    
    def value(self,gameState: GameState, agentIndex=0, curdepth=1):
        if curdepth > self.depth or gameState.isWin() or gameState.isLose():
            # print("depth-w/l",curdepth)
            # print("stop")
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex ==0:
            val, mov = self.maximizer(gameState,agentIndex,curdepth)
            # print("val,mov=",val,mov)  
            return val,mov
        else:    
            val, mov = self.minimizer(gameState,agentIndex,curdepth)
            # print("val,mov=",val,mov)
            return val, mov
        # if (ghostNum == gameState.getNumAgents()-1) and (curdepth < self.depth):
        
    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # print("**********Start***********")
        val, act= self.value(gameState,0,1)
        # print("**********End***********")
        return act


        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def minimizer(self,gameState: GameState,agentIndex,curdepth,Alpha,Beta):
        # print("min")
        finalVal = 9999999
        finalAct = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)
        nextAgent = agentIndex+1
        nextDepth = curdepth
        currentAlpha = Alpha
        currentBeta = Beta
        if agentIndex == gameState.getNumAgents()-1:
            nextAgent = 0
            nextDepth = curdepth+1
        for act in actions:
            successor = gameState.generateSuccessor(agentIndex,act)
            currentVal,_ = self.value(successor,nextAgent,nextDepth,currentAlpha,currentBeta)
            if currentVal < finalVal:
                finalVal = currentVal
                finalAct = act
            # if (currentVal < currentAlpha) and (agentIndex != 1) : return currentVal, act
            if (currentVal < currentAlpha) : return currentVal, act
            currentBeta = min(currentBeta,currentVal)

        # print(finalVal,finalAct)
        return finalVal, finalAct
    
    def maximizer(self,gameState: GameState,agentIndex, curdepth,Alpha,Beta):
        # print("max")
        finalVal = -9999999
        finalAct = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)
        currentAlpha = Alpha
        currentBeta = Beta
        for act in actions:
            # print(act)
            successor = gameState.generateSuccessor(agentIndex,act)
            currentVal,_ = self.value(successor,1,curdepth,currentAlpha,currentBeta)
            # print(currentVal)
            if currentVal > finalVal:
                finalVal = currentVal
                finalAct = act
            if (currentVal > currentBeta) : return currentVal, act
            currentAlpha = max(currentAlpha,currentVal)

        # print(finalVal,finalAct)
        return finalVal, finalAct
    
    def value(self,gameState: GameState, agentIndex, curdepth,bestmax,bestmin):
        if curdepth > self.depth or gameState.isWin() or gameState.isLose():
            # print("depth-w/l",curdepth)
            # print("stop")
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex ==0:
            val, mov = self.maximizer(gameState,agentIndex,curdepth,bestmax,bestmin)
            # print("val,mov=",val,mov)  
            return val,mov
        else:    
            val, mov = self.minimizer(gameState,agentIndex,curdepth,bestmax,bestmin)
            # print("val,mov=",val,mov)
            return val, mov
        # if (ghostNum == gameState.getNumAgents()-1) and (curdepth < self.depth):

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # print("**********Start***********")
        val, act= self.value(gameState,0,1,-999999,999999)
        # print("**********End***********")
        return act

        util.raiseNotDefined()
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimizer(self,gameState: GameState,agentIndex,curdepth=1):
        # print("min")
        totalVal = 0
        actions = gameState.getLegalActions(agentIndex)
        nextAgent = agentIndex+1
        nextDepth = curdepth
        if agentIndex == gameState.getNumAgents()-1:
            nextAgent = 0
            nextDepth = curdepth+1
        for act in actions:
            successor = gameState.generateSuccessor(agentIndex,act)
            currentVal,_ = self.value(successor,nextAgent,nextDepth)
            totalVal += currentVal
        expectVal = totalVal/len(actions)
        return expectVal, Directions.STOP
    
    def maximizer(self,gameState: GameState,agentIndex, curdepth=1):
        # print("max")
        finalVal = -9999999
        finalAct = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)
        for act in actions:
            # print(act)
            successor = gameState.generateSuccessor(agentIndex,act)
            currentVal,_ = self.value(successor,1,curdepth)
            # print(currentVal)
            if currentVal > finalVal:
                finalVal = currentVal
                finalAct = act
        # print(finalVal,finalAct)
        return finalVal, finalAct
    
    def value(self,gameState: GameState, agentIndex=0, curdepth=1):
        if curdepth > self.depth or gameState.isWin() or gameState.isLose():
            # print("depth-w/l",curdepth)
            # print("stop")
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex ==0:
            val, mov = self.maximizer(gameState,agentIndex,curdepth)
            # print("val,mov=",val,mov)  
            return val,mov
        else:    
            val,mov = self.expectimizer(gameState,agentIndex,curdepth)
            return val, mov
        # if (ghostNum == gameState.getNumAgents()-1) and (curdepth < self.depth):

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # print("**********Start***********")
        val, act= self.value(gameState,0,1)
        # print("**********End***********")
        return act

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # successorGameState = currentGameState.generatePacmanSuccessor(action)
    # newPos = currentGameState.getPacmanPosition()
    # newFood = currentGameState.getFood()
    # newGhostStates = currentGameState.getGhostStates()
    # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # "*** YOUR CODE HERE ***"
    # # print("succesor",successorGameState)
    # # print("newPos",newPos)
    # # print("newFood",newFood)
    # # print("newGhostStates",newGhostStates)
    # # print("newScaredTimes",newScaredTimes)
    # #add food location factor
    # FoodDistance = 999999
    # for food in newFood:
    #     curr  = manhattanDistance(newPos,food)
    #     if curr < FoodDistance:
    #         FoodDistance = curr
    # # add ghost factor
    # GhostDistance = 999999
    # for ghost in newGhostStates:
    #     curr = manhattanDistance(newPos,ghost.getPosition())
    #     if curr < GhostDistance:
    #         GhostDistance = curr
    # # add capsule factor
    # # CapsuleDistance = 999999
    # # for capsule in currentGameState.getCapsules():
    # #     curr = manhattanDistance(newPos,capsule)
    # #     if curr < CapsuleDistance:
    # #         CapsuleDistance = curr

    # return currentGameState.getScore()+GhostDistance+1/FoodDistance

    "*** YOUR CODE HERE ***"
    # print("succesor",successorGameState)
    # print("newPos",newPos)
    # print("newFood",newFood)
    # print("newGhostStates",newGhostStates)
    # print("newScaredTimes",newScaredTimes)

    newScaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]
    # print(newScaredTimes)

    #add food location factor
    scared = False
    foodleft = currentGameState.getFood().count()
    FoodDistance = 99999
    if foodleft == 0:
        FoodDistance = 1
    else:
        for food in currentGameState.getFood().asList():
            # print("n",newPos)
            # print("f",food)
            curr  = manhattanDistance(currentGameState.getPacmanPosition(),food)
            if curr < FoodDistance:
                FoodDistance = curr
    # add ghost factor
    # Ghostpositions = newGhostStates.getGhostPositions()
    GhostDistance = 999
    for ghost in currentGameState.getGhostPositions():
        # print(ghost.getPosition())
        curr = manhattanDistance(currentGameState.getPacmanPosition(),ghost)
        if curr < GhostDistance:
            GhostDistance = curr
       
    # print(GhostDistance/FoodDistance)

    # if scared:
    #     return successorGameState.getScore()+0.7*GhostDistance+1/FoodDistance
    # else:
    #     return successorGameState.getScore()-7/(GhostDistance+1)+1/FoodDistance
    # print(foodleft)
    # print("f",FoodDistance)
    # print("g",GhostDistance)
        #add capsule factor
    CapsuleDistance = 999999
    for capsule in currentGameState.getCapsules():
        curr = manhattanDistance(currentGameState.getPacmanPosition(),capsule)
        if curr < CapsuleDistance:
            CapsuleDistance = curr
    if newScaredTimes[0] == 0:
        return  currentGameState.getScore()+5/(FoodDistance+0.1)-20/(GhostDistance+0.1)+5/(CapsuleDistance+0.1)
    else:
        return  currentGameState.getScore()+5/(FoodDistance+0.1)+20/(GhostDistance+0.1)+5/(CapsuleDistance+0.1)
       


    util.raiseNotDefined()
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
