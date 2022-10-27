# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
import numpy

import mdp, util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0

        "*** YOUR CODE HERE ***"
        states = mdp.getStates()
        for it in range(self.iterations):
            prev_values = self.values.copy()
            self.values = util.Counter()

            for state in states:
                possible_actions = mdp.getPossibleActions(state)
                if possible_actions:
                    max_sum = float('-inf')
                    for act in possible_actions:
                        max_sum = max(max_sum, self.getSumProbablity(act, state, prev_values))
                else:
                    max_sum = 0
                self.values[state] = discount * max_sum + mdp.getReward(state, None, None)

    def getValue(self, state):
        """
      Return the value of the state (computed in __init__).
    """
        return self.values[state]

    def getQValue(self, state, action):
        """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
        "*** YOUR CODE HERE ***"
        return self.discount * self.getSumProbablity(action, state, self.values) + self.mdp.getReward(state, None, None)

    def getSumProbablity(self, action, state, values):
        result = 0
        for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            result += prob * values[next_state]
        return result

    def getPolicy(self, state):
        """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
        "*** YOUR CODE HERE ***"
        if not self.mdp.getPossibleActions(state):
            return None

        action_to_q = {act: self.getQValue(state, act) for act in self.mdp.getPossibleActions(state)}
        return max(action_to_q, key=action_to_q.get)



    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)
