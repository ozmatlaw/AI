import random
import json
import orders
import agents
from agents import *
from orders import *
from heuristics import *


def read_order_file(file_name):
    """
    Reads the file and translate it into set of orders
    :param file_name
    :return: set of orders
    """
    orders_set = set()
    with open(file_name, 'r') as orders:
        data = json.load(orders)
        for order_num, items in data.items():
            order = Order(items["meal_type"], set(items["ingredient"]), items["order_time"], order_num)
            orders_set.add(order)

    return orders_set


def write_orders_to_json(orders):
    """
    Writes orders to file
    :param orders: set of orders
    :return: -
    """
    orders = sorted(list(orders), key=lambda order: int(order.get_order_num()))
    with open("log.json", "w") as orders_file:
        orders_file.write("{\n")
        buf = []
        for order in orders:
            meal_type = order.get_meal_type()
            ing = order.get_ingredients()
            time = order.get_order_time()
            num = order.get_order_num()

            meal = {str(num): {"meal_type": meal_type, "ingredient": list(ing), "order_time": time}}
            buf.append(str(meal)[1:-1].replace("'", '"'))

        orders_file.write(',\n'.join(buf))
        orders_file.write("\n}")


class Simulator:
    """
    this class defines the main simulator of this project
    """

    def __init__(self):
        """
        Constructor
        initializes the simulator
        """
        self.take_orders = True
        self.stock = {}
        self.generate_stock()
        self.total_score = 0
        self.current_time = 0
        self.orders = set()
        self.active_order = ActiveOrder()
        self.orders_satisfied = set()
        self.missed_orders = set()

        self.max_score = 0

    def generate_stock(self):
        """
        Generates the current ingredient stock to random values
        """
        for ing in ALL_INGREDIENTS:
            self.restock_ingredient(ing)

    def get_orders(self):
        """
        Getter: return the orders of the Simulator
        :return: set of orders
        """
        return self.orders

    def remove_order(self, order):
        """
        Removes an order
        :param order: order to remove
        :return: None
        """
        for x in self.orders:
            if x.get_order_num() == order.get_order_num():
                self.orders.remove(x)
                break
        for x in self.missed_orders:
            if x.get_order_num() == order.get_order_num():
                self.missed_orders.remove(x)
                break

    def serve(self):
        """
        serves the order to the customer and removes it from the orders
        """
        order = self.active_order.get_order()
        self.orders_satisfied.add(order)
        self.total_score += self.active_order.get_order().get_score()
        self.remove_order(order)
        self.active_order.reset()

    def drop_order(self):
        """
        Drops current order
        """
        self.active_order.reset()

    def working_on_an_order(self):
        """
        checks if currently working on an order
        :return: true if working on an order false otherwise
        """
        return self.active_order.is_order_active()

    def updated_max_score(self, order):
        """
        Updated the max score of the simulator
        """
        self.max_score += order.get_score()

    def do_move(self, move):
        """
        Performs a move, returning a new simulator state
        """
        if move == WAIT:
            self.do_nothing()
        elif move == DROP:
            self.drop_order()
        elif move == SERVE:
            self.serve()
        elif move == RESTOCK:
            self.restock_station()
        elif move in ALL_INGREDIENTS:
            self.take_ingredient(move)
        else:
            self.active_order.start_order(move)

    def take_ingredient(self, cur_ing):
        """
        Takes the ingredient that the worker is currently on and adds it to the active order if it is relevant to the
        order
        """
        self.active_order.add_ingredient(cur_ing)
        self.stock[cur_ing] -= 1

    def get_legal_moves(self):
        """
        Returns a list of legal moves of this board state
        1. move right/ left + take or not
        2. start order
        3. drop order
        4. serve
        5. wait
        6. restock ingredient
        """
        moves = set()
        if not len(self.orders):
            moves.add(WAIT)
            return moves
        # if working on an order
        # add all the relevant ingredients + restock if necessary
        if self.active_order.is_order_active():
            if self.active_order.done():
                moves.add(SERVE)
            else:
                for ing in self.active_order.get_ing_not_yet_added():
                    if self.stock[ing] == 0:
                        moves.add(RESTOCK)
                    else:
                        moves.add(ing)
                if len(self.orders) > 1:
                    moves.add(DROP)
        else:  # not working on and order can wait or take a new order
            if len(self.orders):
                for order in self.orders:
                    moves.add(order)

        return moves

    def restock_ingredient(self, ing):
        """
        restocks the given ingredient
        :param: ingredient to restock
        """
        self.stock[ing] = RESTOCK_VAL

    def restock_station(self):
        for ing in MEALS[self.active_order.order.get_meal_type()]:
            self.restock_ingredient(ing)

    def can_finish_in_time(self, order):
        """
        Checks if the order still can be finished
        """
        return order.timeout >= len(order.get_ing_not_yet_added()) + (1 if order == self.active_order.order else 0)

    def get_score(self):
        """
        Getter: return the score
        :return: int
        """
        return self.total_score

    def get_time(self):
        """
        Getter: return current simulator time
        :return: int
        """
        return self.current_time

    def get_max_score(self):
        """
        Getter: return the max score reachable in the current sim
        :return: int of max score
        """
        return self.max_score

    def get_reachable_score(self):
        """
        Return the maximum score the simulator can be reach
        :return: int
        """
        return self.get_max_score() - sum(order.get_score() for order in self.missed_orders)

    def get_successors_simulators(self):
        """
        Calculate the successors of the simulator and return them
        """
        simulators = set()
        for move in self.get_legal_moves():
            cur = self.__copy__()
            cur.inc_time(future_orders=True)
            cur.do_move(move)
            simulators.add((cur, move))
        return simulators

    def finished(self):
        """
        :return: True if no orders are left in the game
        """
        return not self.orders

    def do_nothing(self):
        """
        does nothing
        """
        return

    def __str__(self):
        """
        __str__ for the class
        """
        return "stock: " + str(self.stock) + '\n' + \
               "total_score: " + str(self.total_score) + '\n' + \
               "orders: " + str(self.orders) + '\n' + \
               "orders_satisfied: " + str(self.orders_satisfied) + '\n' + \
               "missed_orders: " + str(self.missed_orders) + '\n' + \
               "time: " + str(self.current_time) + '\n' + \
               "active_order: " + str(self.active_order) + '\n' + \
               "take_orders: " + str(self.take_orders) + '\n'

    def __repr__(self):
        """
        __repr__ for the class
        """
        return str(self)

    def __lt__(self, other):
        """
        __lt__ for the class
        """
        return self.get_score() < other.get_score()

    def start_order(self, order):
        """
        start perform this order
        """
        self.active_order.start_order(order)


class OnlineSimulator(Simulator):
    """
    This class defines the online simulator
    """

    def __init__(self, agent, pre_as_set=None, pre_orders=None):
        """
        Constructor
        :param agent: agent for simulator, can be SJF, FCFS, or OnlineMainAgent
        :param pre_as_set: pre-order as set
        :param pre_orders: pre-order as dictionary
        """
        super().__init__()
        self.num_of_orders = 1
        self.orders = set()
        self.agent = agent
        self.all_scores = [0]
        if pre_orders:
            self.pre_orders = pre_orders
        else:
            if pre_as_set is None:
                self.pre_orders = self.rand_orders()
            else:
                self.pre_orders = self.load_pre(pre_as_set)
        self.pre_orders_to_return = dict()

        for key in self.pre_orders:
            self.pre_orders_to_return[key] = {order.__copy__() for order in self.pre_orders[key]}

    def rand_orders(self, intervals=15):
        """
        Generates random orders
        :return: the orders generated randomly
        """

        orders = set()
        order_number = 0
        for i in range(INIT_ONLINE_ORDERS):
            meal_type = MEAL_TYPE[random.randint(0, len(MEAL_TYPE) - 1)]
            ingredients = set(random.sample(MEALS[meal_type],
                                            random.randint(*MEAL_RNG[meal_type])))
            arrival_time = random.randint(1, intervals)

            order = Order(meal_type, ingredients, arrival_time, order_number)
            orders.add(order)
            order_number += 1

        return self.load_pre(orders)

    def load_pre(self, orders):
        """
        Converting the dictionary to set of orders
        :return: the orders in a dictionary, key:arrival time, value: set of orders
        """

        pre = dict()
        for order in orders:
            arrival_time = order.get_order_time()

            if arrival_time in pre:
                pre[arrival_time].add(order)
            else:
                pre[arrival_time] = {order}

        return pre

    def set_orders(self, orders):
        """
        Set the orders
        """
        self.orders = orders

    def run(self):
        """
        runs the online simulator
        """
        set_to_json = set()
        for x in self.pre_orders.values():
            set_to_json = set_to_json.union(x)
        write_orders_to_json(set_to_json)

        moves = []
        while not self.sim_finished():
            move = self.agent.get_move(self)
            # print(self.get_legal_moves())
            # print(move)
            # print(self.get_time())
            self.do_move(move)
            self.inc_time()

            moves.append(move)
        return [self.get_score(), self.pre_orders_to_return, self.all_scores, moves]

    def update_orders(self):
        """
        Update and adding orders according to the current time
        """
        if not self.take_orders:
            return
        if self.current_time in self.pre_orders:
            self.orders = self.orders.union(self.pre_orders[self.current_time])
            for order in self.pre_orders[self.current_time]:
                self.updated_max_score(order)

    def run_offline(self):
        """
        Run the simulator in offline mode - all the orders known at initialization
        :return:
        """
        """
        runs the online sim
        """
        set_to_json = set()
        for x in self.pre_orders.values():
            set_to_json = set_to_json.union(x)
        write_orders_to_json(set_to_json)

        moves = self.agent.get_offline(self)[0]
        print("Hey")
        return [self.get_score(), self.pre_orders_to_return, self.all_scores, moves]

    def inc_time(self, future_orders=False):
        """
        Increment the time
        :param future_orders: a flag for updating the orders
        """
        self.current_time += 1
        if self.current_time >= MAX_TIMEOUT:
            self.take_orders = False
        for order in self.orders:
            order.decrease_time()
            if order.missed_order():
                self.missed_orders.add(order)

        if self.active_order.order:
            if self.active_order.order.missed_order():
                self.active_order.reset()

        self.orders = self.orders - self.missed_orders
        if not future_orders or is_offline:
            self.update_orders()
            self.all_scores.append(self.total_score)

    def __copy__(self):
        """
        Copy for the class
        """
        cpy = OnlineSimulator(self.agent, pre_orders=self.pre_orders)

        cpy.num_of_orders = self.num_of_orders
        cpy.pre_orders = self.pre_orders

        cpy.take_orders = self.take_orders
        cpy.stock = self.stock.copy()
        cpy.total_score = self.total_score
        cpy.current_time = self.current_time
        cpy.orders = {order.__copy__() for order in self.orders}
        cpy.active_order = self.active_order.__copy__()
        cpy.orders_satisfied = {order.__copy__() for order in self.orders_satisfied}
        cpy.missed_orders = self.missed_orders = {order.__copy__() for order in self.missed_orders}

        cpy.max_score = self.max_score
        return cpy

    def generate_orders(self, intervals=10):
        """
        Generates random orders
        :return: set of orders
        """
        pre = dict()
        orders = set()
        order_number = 0
        for i in range(INIT_ONLINE_ORDERS):
            meal_type = MEAL_TYPE[random.randint(0, len(MEAL_TYPE) - 1)]
            ingredients = set(random.sample(MEALS[meal_type],
                                            random.randint(*MEAL_RNG[meal_type])))
            arrival_time = random.randint(1, intervals)

            order = Order(meal_type, ingredients, arrival_time, order_number)
            orders.add(order)
            order_number += 1

            if arrival_time in pre:
                pre[arrival_time].add(order)
            else:
                pre[arrival_time] = {order}

        return pre

    def sim_finished(self):
        """
        Checks if the simulator finished it's work
        :return: True or False
        """
        return self.current_time >= MAX_TIMEOUT and not self.orders


def run_generate():
    """
    Function that runs the program with random orders
    """
    online = OnlineSimulator(OnlineMainAgent(lost_score_heuristic))
    return online


def run_Json(arg):
    """
    Function that runs the program with orders that created according to Json file
    :param arg: path to Json file
    """
    tmp = read_order_file(arg)
    online = OnlineSimulator(OnlineMainAgent(lost_score_heuristic), pre_as_set=tmp)
    return online
