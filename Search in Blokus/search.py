"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    "*** YOUR CODE HERE ***"
    return none_priority_search(problem, util.Stack())


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    return none_priority_search(problem, util.Queue())


def successor_nodes(children):
    nodes = []
    for child in children:  # successor, actions, cost
        node = Node(child[2], child[0], child[1])  # cost, cur_board, moves
        nodes.append(node)
    return nodes


def none_priority_search(problem, fringe):
    fringe.push(Node(0, problem.get_start_state(), []))

    visited = set()

    while not fringe.isEmpty():  # keep on going until goal is achieved
        cur_node = fringe.pop()
        if problem.is_goal_state(cur_node.cur_board):
            return cur_node.moves

        if hasattr(cur_node.cur_board, "state"):
            cur_state = hash(str(cur_node.cur_board.state))
        else:
            cur_state = cur_node.cur_board  # no idea what to do if no state

        # cur_state = hash(str(cur_node.cur_board.state))  # todo - what to do if doesnt have a state
        if cur_state not in visited:
            visited.add(cur_state)
            children = problem.get_successors(cur_node.cur_board)
            children = successor_nodes(children)

            for child in children:
                if hasattr(cur_node.cur_board, "state"):
                    child_state = hash(str(child.cur_board.state))  # no idea what to do if no state
                else:
                    child_state = child.cur_board  # no idea what to do if no state
                if child_state not in visited:
                    fringe.push(Node(cur_node.cost + child.cost, child.cur_board, cur_node.moves + [child.moves]))
    # return no sol


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    return priority_search(problem.get_start_state(), problem, util.PriorityQueue())


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    return priority_search(problem.get_start_state(), problem, util.PriorityQueue(), heuristic)


class Node:
    def __init__(self, cost, cur_board, moves):
        self.cost = cost
        self.cur_board = cur_board
        self.moves = moves  # actions already taken


# todo can combine into one modular function just need to figure out what to do if there is no state
def priority_search(state, problem, fringe, heuristic=null_heuristic):
    priority = heuristic(state, problem)
    fringe.push(Node(0, state, []), priority)
    visited = set()

    while not fringe.isEmpty():  # keep on going until goal is achieved
        cur_node = fringe.pop()
        if problem.is_goal_state(cur_node.cur_board):
            return cur_node.moves

        if hasattr(cur_node.cur_board, "state"):
            cur_state = hash(str(cur_node.cur_board.state))
        else:
            cur_state = cur_node.cur_board

        if cur_state not in visited:
            visited.add(cur_state)
            children = problem.get_successors(cur_node.cur_board)
            children = successor_nodes(children)

            for child in children:
                if hasattr(cur_node.cur_board, "state"):
                    child_state = hash(str(child.cur_board.state))  # no idea what to do if no state
                else:
                    child_state = child.cur_board  # no idea what to do if no state
                if child_state not in visited:
                    fringe.push(Node(cur_node.cost + child.cost, child.cur_board, cur_node.moves + [child.moves]),
                                cur_node.cost + child.cost + heuristic(child.cur_board, problem))


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
