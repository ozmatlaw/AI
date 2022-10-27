import numpy as np
import abc
import util
from game import Agent, Action
from math import inf


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.
        """

        successor_game_state = current_game_state.generate_successor(action=action)
        board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score
        adjacent, empty_tiles = get_adj_and_empty(board)
        board_diff = np.sum(np.abs(np.diff(board)) + np.sum(np.abs(np.diff(board, axis=0))))
        dist_from_corner = distance_of_max_tile_from_corner(board,max_tile)

        return 8 * empty_tiles + 6 * adjacent - 1 * board_diff + 2 * score + 5 * max_tile - \
            3 * dist_from_corner


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """

        depth = 0
        actions = game_state.get_legal_actions(0)
        values = []
        for a in actions:
            values.append(self.min_value(game_state.generate_successor(action=a), depth)[0])
        return actions[np.argmax(np.array(values))]

    def max_value(self, game_state, depth):
        """
        a function to calculate the max value of a game state.
        :param game_state: the current game state.
        :param depth: the current tree depth.
        :return: the value of the game state, an action.
        """
        if depth == self.depth or game_state._done:
            return self.evaluation_function(game_state), Action.STOP
        v, action = -inf, None
        actions = game_state.get_legal_actions(0)
        min_vals = [
            (self.min_value(game_state.generate_successor(agent_index=0, action=a), depth)[0], a)
            for a in actions]

        for a in range(len(actions)):
            if v < max(v, min_vals[a][0]):
                v = min_vals[a][0]
                action = min_vals[a][1]
        return v, action

    def min_value(self, game_state, depth):
        """
        a function to calculate the min value of a game state.
        :param game_state: the current game state.
        :param depth: the current tree depth.
        :return: the value of the game state, an action.
        """
        if depth == self.depth or game_state._done:
            return self.evaluation_function(game_state), Action.STOP
        v, action = inf, None
        actions = game_state.get_legal_actions(1)
        max_vals = [(self.max_value(game_state.generate_successor(agent_index=1, action=a),
                                      depth + 1)[0], a) for a in actions]
        for a in range(len(actions)):
            if v > min(v, max_vals[a][0]):
                v = max_vals[a][0]
                action = max_vals[a][1]
        return v, action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        depth = 0
        actions = game_state.get_legal_actions(0)
        values = []
        for a in actions:
            values.append(
                self.min_value(game_state.generate_successor(action=a), depth, -inf, inf)[0])
        return actions[np.argmax(np.array(values))]

    def max_value(self, game_state, depth, alpha, beta):
        """
        a function to calculate the max value of a game state.
        :param game_state: the current game state.
        :param depth: the current tree depth.
        :param alpha: the initial alpha value for the game state.
        :param beta: the initial beta value for the game state.
        :return: the value of the game state, an action.
        """
        if depth == self.depth or game_state._done:
            return self.evaluation_function(game_state), Action.STOP
        v, action = -inf, None
        actions = game_state.get_legal_actions(0)
        min_vals = [(self.min_value(game_state.generate_successor(agent_index=0, action=a), depth,
                                      alpha, beta)[0], a) for a in actions]

        for a in range(len(actions)):
            if v < max(v, min_vals[a][0]):
                v = min_vals[a][0]
                action = min_vals[a][1]
            if v >= beta:
                return v, action
            alpha = max(alpha, v)
        return v, action

    def min_value(self, game_state, depth, alpha, beta):
        """
        a function to calculate the min value of a game state.
        :param game_state: the current game state.
        :param depth: the current tree depth.
        :param alpha: the initial alpha value for the game state.
        :param beta: the initial beta value for the game state.
        :return: the value of the game state, an action.
        """
        if depth == self.depth or game_state._done:
            return self.evaluation_function(game_state), Action.STOP
        v, action = inf, None
        actions = game_state.get_legal_actions(1)
        max_vals = [(self.max_value(game_state.generate_successor(agent_index=1, action=a),
                                      depth + 1, alpha, beta)[0], a) for a in actions]
        for a in range(len(actions)):
            if v > min(v, max_vals[a][0]):
                v = max_vals[a][0]
                action = max_vals[a][1]
            if v <= alpha:
                return v, action
            beta = min(beta, v)
        return v, action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """

        depth = 0
        actions = game_state.get_legal_actions(0)
        values = []
        for a in actions:
            values.append(self.min_value(game_state.generate_successor(action=a), depth)[0])
        return actions[np.argmax(np.array(values))]

    def max_value(self, game_state, depth):
        """
        a function to calculate the max value of a game state.
        :param game_state: the current game state.
        :param depth: the current tree depth.
        :return: the value of the game state, an action.
        """
        if depth == self.depth or game_state._done:
            return self.evaluation_function(game_state), Action.STOP
        v, action = -inf, None
        actions = game_state.get_legal_actions(0)
        min_vals = [(self.min_value(game_state.generate_successor(agent_index=0, action=a),
                                      depth)[0], a) for a in actions]

        for a in range(len(actions)):
            if v < max(v, min_vals[a][0]):
                v = min_vals[a][0]
                action = min_vals[a][1]
        return v, action

    def min_value(self, game_state, depth):
        """
        a function to calculate the min value of a game state.
        :param game_state: the current game state.
        :param depth: the current tree depth.
        :return: the value of the game state, an action.
        """
        if depth == self.depth or game_state._done:
            return self.evaluation_function(game_state), Action.STOP
        v, action = inf, None
        actions = game_state.get_legal_actions(1)
        max_vals = [(self.max_value(game_state.generate_successor(agent_index=1, action=a),
                                      depth + 1)[0], a) for a in actions]
        v = sum([s[0] for s in max_vals]) / len(max_vals)
        return v, action


def better_evaluation_function(current_game_state):
    """
    A function to evaluate a game state based on different features of the current game state.
    Please refer to the README for more information.
    :param current_game_state: the current game state
    :return: a value
    """
    max_tile = current_game_state.max_tile
    board = current_game_state.board
    board_diff = np.sum(np.abs(np.diff(board))) + np.sum(
        np.abs(np.diff(board, axis=0)))  # smoothness
    monotonicity = get_monotonicity(board)
    adjacent, empty_tiles = get_adj_and_empty(board)
    score = current_game_state.score
    distance_from_corner = distance_of_max_tile_from_corner(board, max_tile)

    return 3 * max_tile + 3.2 * adjacent + 5 * empty_tiles - 3 * monotonicity - 1 * board_diff + \
        0.4 * score - 3 * distance_from_corner  # above 15k


def distance_of_max_tile_from_corner(board, max_tile):
    """
    A function to calculate the minimal distance between a tile with max value and the corners.
    :param board: the game board
    :param max_tile: the tile with max value
    :return: the minimal distance between max tile and the corners
    """
    corners = {(0, 0), (0, len(board) - 1), (len(board) - 1, 0), (len(board) - 1, len(board) - 1)}
    max_tile_location = np.argwhere(board == max_tile)
    return min(abs(max_tile_location[0][0] - corner[0]) + abs(max_tile_location[0][1] - corner[1])
               for corner in corners)


def get_adj_and_empty(board):
    """
    Returns the number of empty tiles and of tiles with same value that are adjacent to each other.
    :param board: the game board
    :return: the number of empty tiles and of tiles with same value that are adjacent to each other.
    """
    empty_tiles = 0
    adjacent = 0
    for i in range(len(board) - 1):
        for j in range(len(board[i]) - 1):
            if board[i][j] <= 0:
                empty_tiles += 1
            if board[i][j] == board[i + 1][j] or board[i][j] == board[i][j + 1]:
                adjacent += 1
    return adjacent, empty_tiles


def get_monotonicity(board):
    """
    A function to calculate the monotonicity of a board.
    :param board: the game board
    :return: the monotonicity
    """
    ascending_y = 0
    descending_y = 0
    for y in range(len(board) - 1):
        tile = 0
        next_tile = 1
        while next_tile < len(board) - 1:
            if board[next_tile][y] == 0:  # skip empty cells
                next_tile += 1
                continue

            if next_tile == 4:  # end of row all zeros
                ascending_y += board[tile][y]

            if board[tile][y] < board[next_tile][y]:
                ascending_y += board[next_tile][y] - board[tile][y]
            else:
                descending_y += board[tile][y] - board[next_tile][y]

            tile = next_tile
            next_tile += 1
    RL_mono = min(ascending_y, descending_y)

    ascending_x = 0
    descending_x = 0
    for x in range(len(board) - 1):
        tile = 0
        next_tile = 1
        while next_tile < len(board) - 1:
            if board[x][next_tile] == 0:  # skip empty cells
                next_tile += 1
                continue

            if next_tile == 4:  # end of row all zeros
                ascending_x += board[x][tile]

            if board[x][tile] < board[x][next_tile]:
                ascending_x += board[x][next_tile] - board[x][tile]
            else:
                descending_x += board[x][tile] - board[x][next_tile]

            tile = next_tile
            next_tile += 1
    UD_mono = min(ascending_x, descending_x)
    return RL_mono + UD_mono



# Abbreviation
better = better_evaluation_function
