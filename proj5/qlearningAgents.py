# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import gridworld

import random,util,math
import copy

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent
      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update
      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        self.values = util.Counter() # A Counter is a dict with default 0

        "*** YOUR CODE HERE ***"

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.values[(state,action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        actions = self.getLegalActions(state)
        if not actions:
            return 0
        else:
            maxVal = -999
            for action in actions:
                current = self.getQValue(state,action)
                if current>maxVal:
                    maxVal = current
            return maxVal
               
    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        temp = util.Counter()
        actions = self.getLegalActions(state)
        if actions:
            maxVal = -999
            maxAct = None
            for action in actions:
                temp = self.values[(state,action)]
                if temp>maxVal:
                  maxAct = action
                  maxVal = temp
            return maxAct
        return None
    

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if legalActions:
            if util.flipCoin(self.epsilon):
                return random.choice(legalActions)
        return self.computeActionFromQValues(state)
    


    def update(self, state, action, nextState, reward: float):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # legalActions = self.getLegalActions(nextState)

        # for action in legalActions:
        sample = reward + self.discount*self.getValue(nextState)
        self.values[(state,action)] = (1-self.alpha)*self.getQValue(state,action)+(sample*self.alpha)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action

class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent
       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        # for feature in self.featExtractor.getFeatures(state, action).keys():
        #     if feature in self.weights.keys():
        #         return self.weights[feature] * self.featExtractor.getFeatures(state, action)
        # sum = 0
        # for key in self.weights.keys():
        #     # print(key)
        #     features = self.featExtractor.getFeatures(state, action)
        #     # print(features)
        #     if key in features.keys():
        #         # return self.weights[feature] * self.featExtractor.getFeatures(state, action)
        #         sum += self.weights[key]*features[key]
        # return sum
    
        return self.weights * self.featExtractor.getFeatures(state, action)


    def update(self, state, action, nextState, reward: float):
        """
           Should update your weights based on transition
        """
        
        # if self.weights:
            # legalActions = self.getLegalActions(nextState)
            # maxVal = -999
            # for act in legalActions:
            #     current = self.getQValue(nextState,act)
            #     if current>maxVal:
            #         maxVal = current
            # difference = (reward + self.gamma * maxVal) - self.getQValue(state,action)
        nextact = self.getAction(nextState)
        # print(nextact)
        difference = (reward + self.discount * self.getValue(nextState)) - self.getQValue(state,action)
        temp = util.Counter()
        # for weight in self.weights.keys():
        #     features = self.featExtractor.getFeatures(state, action)
        #     if weight in features.keys():
        #         temp[weight] = self.weights[weight] + self.alpha * difference * features[weight]
        #     else:
        #         temp[weight] = self.weights[weight]
        #     # print(self.weights[weight])

        # self.weights = temp
        # print(self.weights)

        for feature in self.featExtractor.getFeatures(state, action):
            self.weights[feature] += self.alpha * difference * self.featExtractor.getFeatures(state, action)[feature] 
    

    def final(self, state):
        """Called at the end of each game."""
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
