from board import Board
from search import SearchProblem, priority_search, a_star_search
import util
import numpy


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        self.start_point = starting_point
        self.targets = [(0, 0), (0, board_h - 1), (board_w - 1, board_h - 1), (board_w - 1, 0)]
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)  # todo: one player?

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        return state.get_position(0, 0) != -1 and state.get_position(0, state.board_h - 1) != -1 and \
               state.get_position(state.board_w - 1, state.board_h - 1) != -1 and \
               state.get_position(state.board_w - 1, 0) != -1

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        cost = 0
        for action in actions:
            cost += action.piece.get_num_tiles()
        return cost


def calc_dist(a, b):
    a1 = (a[0] - 1, a[0] - 1)
    a2 = (a[0] + 1, a[0] + 1)
    a3 = (a[0] + 1, a[0] - 1)
    a4 = (a[0] - 1, a[0] + 1)

    d1 = (abs(a1[0] - b[0]) + abs(a1[1] - b[1])) / 2
    d2 = (abs(a2[0] - b[0]) + abs(a2[1] - b[1])) / 2
    d3 = (abs(a3[0] - b[0]) + abs(a3[1] - b[1])) / 2
    d4 = (abs(a4[0] - b[0]) + abs(a4[1] - b[1])) / 2
    return min(d1, d2, d3, d4)


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def uncovered_targets(problem):
    return [target for target in problem.targets if problem.board.get_position(target[0], target[1]) == -1]


def get_dists(start_point, targets, dist_func):
    return [dist_func(start_point, target) for target in targets]


def get_covered_pieces(state):
    return numpy.argwhere(state.state != -1)


def blokus_heuristic(state, problem, needs_addition):
    if problem.is_goal_state(state):
        return 0
    targets_to_reach = uncovered_targets(problem)
    res = get_dists(problem.start_point, targets_to_reach, calc_dist)
    filled_tiles = get_covered_pieces(state)
    for i, target in enumerate(targets_to_reach):
        for piece in filled_tiles:
            res[i] = min(res[i], calc_dist(target, piece))
    final = max(res) + (len(targets_to_reach) - 1) if len(targets_to_reach) > 1 else 0
    return final if final > 0 else 1


def calc_dist_corners(target, piece):
    return (abs(target[0] - piece[0]) + abs(target[1] - piece[1])) / 2


def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    if problem.is_goal_state(state):
        return 0
    targets_to_reach = uncovered_targets(problem)
    res = get_dists(problem.start_point, targets_to_reach, calc_dist_corners)
    filled_tiles = get_covered_pieces(state)
    for i, target in enumerate(targets_to_reach):
        for piece in filled_tiles:
            res[i] = min(res[i], calc_dist_corners(target, piece))
    return max(res) + (len(targets_to_reach) - 1) if (len(targets_to_reach) > 1) else 0


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.start_point = starting_point
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        for target in self.targets:
            if state.get_position(target[1], target[0]) == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        cost = 0
        for action in actions:
            cost += action.piece.get_num_tiles()
        return cost


def blokus_cover_heuristic(state, problem):
    if problem.is_goal_state(state):
        return 0
    targets_to_reach = uncovered_targets(problem)
    res = get_dists(problem.start_point, targets_to_reach, calc_dist)
    filled_tiles = get_covered_pieces(state)
    for i, target in enumerate(targets_to_reach):
        for piece in filled_tiles:
            res[i] = min(res[i], calc_dist(target, piece))
    final = max(res) + (len(targets_to_reach) - 1) if len(targets_to_reach) > 1 else 0
    return final if final > 0 else 1


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        self.start_point = starting_point
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace

        return backtrace
        """
        "*** YOUR CODE HERE ***"
        current_state = self.board.__copy__()
        backtrace = []
        targets_to_cover = self.targets
        problem = BlokusCoverProblem(current_state.board_w,
                                     current_state.board_h,
                                     current_state.piece_list,
                                     self.start_point,
                                     self.targets)
        while targets_to_cover:
            problem.targets = [targets_to_cover.pop(numpy.argmin(
                numpy.array(get_dists(self.start_point, targets_to_cover, calc_dist))))]
            actions = priority_search(current_state, problem, util.PriorityQueue())
            for action in actions:
                current_state.add_move(0, action)  # now when it goes it counts it twice
            backtrace += actions
            self.expanded += problem.expanded
        return backtrace


def closest_heuristic(state, problem):
    min_dist = calc_dist_corners(problem.targets[0], problem.start_point)
    filled = get_covered_pieces(state)
    for piece in filled:
        min_dist = min(min_dist, calc_dist_corners(piece, problem.targets[0]))
    return min_dist


def calc_dist_closest(target, position):
    return max(abs(target[0]-position[0]), abs(target[1]-position[1]))


class MiniContestSearch:
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.targets = targets.copy()
        self.expanded = 0
        self.problem = BlokusCoverProblem(board_w, board_h, piece_list, starting_point, self.targets)
        self.board = self.problem.board
        self.start_point = starting_point
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.problem.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        actions = priority_search(self.board, self.problem, util.PriorityQueue(), blokus_cover_heuristic)
        self.expanded += self.problem.expanded
        return actions
