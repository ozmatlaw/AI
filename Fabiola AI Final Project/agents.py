import abc
import heapq
import logging
from abc import ABC
from fabiola import *
from heuristics import *
from constants import *

is_offline = False


class Agent(ABC):
    """
    Basic agent: an abstract class representing an agent, to be inherited by all agents
    """

    def __init__(self, *args, **kwargs):
        """
        A constructor for agent
        """

    @abc.abstractmethod
    def get_move(self, state):
        """
        :param state: state
        :return: A string that represent the next move
        """
        raise NotImplementedError()


class PriorityQ:
    """
    Class of Priority Queue
    """

    def __init__(self):
        """
        Constructor for the class
        """
        self.heap = []

    def push(self, priority, item):
        """
        A method that pushes an argument to the queue
        :param priority: the item's priority
        :param item: argument to add
        :return:
        """
        pair = (priority, item)
        heapq.heappush(self.heap, pair)

    def pop(self):
        """
        A method that pop the lowest priority item from the queue
        :return: the item it removed
        """
        (priority, item) = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        """
        Checks if the queue is empty
        :return: True ot False
        """
        return len(self.heap) == 0


class NodeToFringe:
    """
    a node that will be added to the fringe when using the search algorithm
    """

    def __init__(self, state, prev, move):
        """
        Constructor for NodeToFringe
        :param state: the state the node represents
        :param prev: the state that led to the current state
        :param move: the move done in the simulator to get from prev to state
        """
        self.state = state
        self.prev = prev
        self.move = move

    def __lt__(self, other):
        """
        Implemented to enable insertion of nodes to the PriorityQueue.
        """
        return self.state < other.state

    def __eq__(self, other):
        """
        Implemented in order to enable comparing objects
        :param other: NodeToFringe object
        :return: True if both objects are equal
        """
        return self.state == other.state

    def __hash__(self):
        """
        Implemented for adding nodes to a set
        :return: the hash of the node's state
        """
        return hash(self.state)


def goal_state(node):
    """
    Checks if node is the goal state
    :param node: NodeToFringe object
    :return: True if all orders have been satisfied by this node or timed out
    """
    return node.state.finished()


def search(fringe, start_state, heuristic=lost_score_heuristic):
    """
    this algorithm simulates the restaurant using search, it uses a PriorityQ to optimize its choices
    :param fringe: a PriorityQueue object
    :param start_state: the initial state represented by a State object
    :param heuristic: a heuristic function (optional) set to null_heuristic by default
    :return: a list of moves to be executed, chosen by the algorithm to maximize score
    """
    expanded_nodes = 0
    num_of_iterations = 0
    visited = set()
    fringe.push(priority=0, item=NodeToFringe(state=start_state, prev=None, move=None))

    while not fringe.is_empty():
        num_of_iterations += 1
        current_node = fringe.pop()
        if goal_state(current_node):
            moves = []
            curr = current_node
            move = current_node.move

            while curr.prev:
                moves.append((move, curr.prev.state))
                curr = curr.prev
                move = curr.move

            moves.reverse()
            return moves, expanded_nodes

        if current_node.state not in visited:
            successors = current_node.state.get_successors_simulators()

            expanded_nodes += 1
            for successor in successors:
                successor_state, successor_move = successor
                score = sum(x.get_score() for x in successor_state.missed_orders) + heuristic(successor_state)
                fringe.push(score, NodeToFringe(state=successor_state, prev=current_node, move=successor_move))

            visited.add(current_node.state)


class OfflineAgent(Agent):
    """
    this class implements an offline agent using a search algorithm
    """

    def __init__(self, heuristic=null_heuristic, *args, **kwargs):
        """
        Constructor
        """
        super().__init__(*args, **kwargs)
        self.moves = []
        self.heuristic = heuristic
        self.expanded_nodes = 0

    def run_search(self, start_state):
        """
        sets the agents orders to the given orders, and calls the search algorithm to update the agents moves
        accordingly
        :param: orders: the orders to be set
        """
        self.moves, self.expanded_nodes = search(PriorityQ(), start_state, self.heuristic)

    def get_move(self, state):
        """
        in each call to this method, the next move in the agents moves is returned
        :param state: the state given, irrelevant to the offline agent
        :return: a string representing the agents next move
        """
        return self.moves.pop(0)[0] if len(self.moves) else WAIT


class OnlineMainAgent(Agent):
    """
    this class implements the online agent - The main agent we created
    """

    def __init__(self, heuristic=null_heuristic, *args, **kwargs):
        """
        initializes an object
        """
        super().__init__(*args, **kwargs)
        self.moves = []
        self.heuristic = heuristic

    def get_move(self, state):
        """
        returns the agents next move.
        :param state: an object of Simulator representing the current state
        :return: a string representing the agents next move
        """
        # hadars implementation-
        if len(self.moves):
            move, expected_state = self.moves.pop(0)
            if state == expected_state:
                return move

        # in case of no pending orders - do nothing
        if len(state.get_orders()) == 0:
            return WAIT

        self.moves, expanded_nodes = search(PriorityQ(), state, self.heuristic)
        return self.moves.pop(0)[0]

    def get_offline(self, start_state):
        global is_offline
        is_offline = True
        return search(PriorityQ(), start_state, self.heuristic)


class FCFSSearchAgent(Agent):
    """
    This class implements an FCFS agent
    """

    def __init__(self, ignored=None, *args, **kwargs):
        """
        Constructor
        """
        super().__init__(*args, **kwargs)
        self.moves = []
        self.current_order_moves = []
        self.cur_active_order = None

    def get_move(self, state):  # todo what to do with the state
        """
        In each call to this method, the next move in the agents moves is returned
        :param state: the state given
        :return: a string or char representing the agents next move
        """
        # no orders to work on
        if len(state.get_orders()) == 0:
            return WAIT

        # working on an order take the next ingredient
        if state.working_on_an_order():
            moves = state.active_order.get_ing_not_yet_added()
            return moves.pop() if moves else SERVE

        # not working take the first oldest order to fulfill
        # state.active_order.start_order(min(state.get_orders(), key=lambda x: x.order_time))
        return min(state.get_orders(), key=lambda x: x.order_time)


class SJFSearchAgent(Agent):
    """
    This class implements an SJF (shortest job first) agent without preemption
    """

    def __init__(self, ignored=None, *args, **kwargs):
        """
        Constructor
        """
        super().__init__(*args, **kwargs)
        self.current_order_moves = []
        self.cur_active_order = None
        self.moves = []

    def get_move(self, state):
        """
        In each call to this method, the next move in the agents moves is returned
        :param state: the state given
        :return: a string or char representing the agents next move
        """
        if len(state.get_orders()) == 0:
            return WAIT

        # working on an order take the next ingredient
        if state.working_on_an_order():
            moves = state.active_order.get_ing_not_yet_added()
            return moves.pop() if moves else SERVE

        # not working take the shortest order to fulfill
        return min(state.get_orders(), key=lambda x: len(x.get_ingredients() - x.get_added_ing()))
