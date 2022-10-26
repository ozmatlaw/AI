from fabiola import *


def null_heuristic(state):
    """
    Heuristic that receives a state and do nothing - returns always zero
    :param state: A Simulator object
    :return: 0
    """
    return 0


def lost_score_heuristic(state):
    """
    Returns the reachable score. By summing up all order scores and subtracting all the penalties
    and adding the current score.
    :param state: a State of current simulator
    :return int the current reachable score
    """
    return sum(order.get_score() for order in state.orders if not state.can_finish_in_time(order)) + \
           sum(x.get_score() for x in state.missed_orders) - \
           state.total_score


def max_ing_heuristic(state):
    """
    This heuristic prefers to take the active order with the maximum ingredients
    """
    if not state.active_order.is_order_active():
        return 0
    return len(state.active_order.order.get_ingredients())


def max_can_be_reached_heuristic(state):
    """
    This heuristic prefers to take all the orders that still can be done
    """
    res = 0
    overhead = 0
    if state.active_order.is_order_active():
        order = state.active_order.order
        overhead = 1
        ings = len(order.get_ingredients() - order.get_added_ing())
        time = ings + 1
        res = max(res, time)
    for order in state.get_orders():
        ings = len(order.get_ingredients() - order.get_added_ing())
        time = overhead + ings + 1
        if time < order.get_timeout():
            res = max(order.get_score(), res)
    return res


def max_score_heuristic(state):
    """
    Returns the reachable score. By summing up all order scores and subtracting all the penalties
    and adding the current score.
    :param state: a State of current simulator
    :return int the current reachable score
    """
    return sum(order.get_score() for order in state.orders if state.can_finish_in_time(order))
