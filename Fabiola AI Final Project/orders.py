import random
from constants import *


class Order:
    """
    this class defines an order
    """

    def __init__(self, meal_type, ingredients, order_time, order_num):
        """
        Constructor for the class
        :param meal_type: can be "sandwich", "toast", "salad", "pasta", "coffee"
        :param ingredients: the ingredients the order contains
        :param order_time: arrival time
        :param order_num: order number
        """
        self.meal_type = meal_type
        self.ingredients = ingredients
        self.order_time = order_time
        self.timeout = random.randint(len(ingredients) + 3, 10)
        self.order_num = order_num
        self.added_ingredients = set()

    def get_score(self):
        """
        Getter: returns orders score
        :return: score as int
        """
        return len(self.ingredients) * SCORE_PER_INGREDIENT

    def get_ing_not_yet_added(self):
        """
        Finds the missing ingredients
        :return: set of ingredients
        """
        return self.get_ingredients() - self.get_added_ing()

    def get_timeout(self):
        """
        Getter: returns preparation time of the order
        :return: int
        """
        return self.timeout

    def get_meal_type(self):
        """
        Getter: returns the order meal type
        :return: String of current meal type
        """
        return self.meal_type

    def get_ingredients(self):
        """
        Getter: returns the ingredient of the order
        :return: Set of strings
        """
        return self.ingredients

    def get_order_time(self):
        """
        Getter: arrival time of the order
        :return: int
        """
        return self.order_time

    def get_order_num(self):
        """
        Getter: return the order number
        :return: int
        """
        return self.order_num

    def __str__(self):
        """
        __str__ for order class
        """
        return ORDER_FORMAT.format(o_type=self.meal_type, ing=','.join(self.ingredients),
                                   add_ing=','.join(self.added_ingredients), time=self.order_time,
                                   num=self.order_num, timeout=self.timeout)

    def __repr__(self):
        """
        __repr__ for order class
        """
        return str(self)

    def get_added_ing(self):
        """
        gets the added ingredients
        :return: set of added ingredients
        """
        return self.added_ingredients

    def missed_order(self):
        """
        order timed out
        :return: true is the order timed out false otherwise
        """
        return self.timeout <= 0

    def decrease_time(self):
        """
        decreases the timeout
        """
        self.timeout -= 1

    def __copy__(self):
        cpy = Order(self.meal_type, self.ingredients.copy(), self.order_time, self.order_num)
        cpy.added_ingredients = self.added_ingredients.copy()
        cpy.timeout = self.timeout

        return cpy


class ActiveOrder:
    """
    this class defines the active order the sim is working on
    """

    def __init__(self):
        self.order = None

    def get_added_ingredients(self):
        """
        gets the ingredients that hav been added to
        :return:
        """
        return self.order.get_ingredients() if self.order else None

    def add_ingredient(self, ingredient):
        """
        adds the ingredient to the active order
        :param ingredient: ingredient to add to the order
        """
        self.order.get_added_ing().add(ingredient)

    def get_ing_not_yet_added(self):
        """
        gets the missing ingredients for the active order to be complete
        :return: Set of Strings of the missing ingredients
        """

        return self.order.get_ingredients() - self.order.get_added_ing()

    def reset(self):  # we get a new order and saving it
        """
        resets the current order
        """
        self.order = None

    def start_order(self, order):
        """
        start a new active order from a given order
        :param order: given order to change to active
        """
        self.order = order

    def is_order_active(self):
        return self.order is not None

    def __copy__(self):

        cpy = ActiveOrder()
        if self.order is None:
            cpy.order = None
        else:
            cpy.order = self.order.__copy__()
        return cpy

    def __repr__(self):
        return str(self.order)

    def done(self):
        """
        checks if the ingredient is ready to serve
        :return: true if order is done else false
        """
        return not self.get_ing_not_yet_added()

    def get_order(self):
        """
        gets the order of the active order
        :return: Order current active order
        """
        return self.order
