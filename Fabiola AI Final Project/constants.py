RIGHT = "Right"
LEFT = "Left"
WAIT = "Wait"
DROP = "Drop"
SERVE = "Serve"
START_ORDER = "Start Order"
RESTOCK = "RESTOCK"
TAKE = "TAKE"

ALL_INGREDIENTS = ['cheese', 'ketchup', 'onion', 'tuna', 'olives',
                   'egg', 'tomato', 'cucumber', 'avocado', 'lettuce',
                   'tomato sauce', 'pesto', 'alfredo', 'parmesan',
                   'salad dressing', 'milk', 'oat milk', 'ice', 'coffee']

MEAL_TYPE = ["sandwich", "toast", "salad", "pasta", "coffee"]

MEAL_TIMES = {"sandwich": 5, "toast": 5, "salad": 5, "pasta": 5, "coffee": 3}

MEAL_RNG = {"sandwich": (1, 5), "toast": (1, 5), "salad": (1, 5), "pasta": (1, 5), "coffee": (1, 3)}

MEALS = {"sandwich": ['cheese', 'ketchup', 'onion', 'tuna', 'olives',
                      'egg', 'tomato', 'cucumber', 'avocado', 'lettuce'],
         "toast": ['cheese', 'ketchup', 'onion', 'tuna', 'olives'],
         "salad": ['cheese', 'onion', 'tuna', 'olives', 'egg', 'tomato',
                   'cucumber', 'avocado', 'lettuce', 'salad dressing'],
         "pasta": ['tomato sauce', 'pesto', 'cheese', 'alfredo', 'parmesan'],
         "coffee": ['milk', 'oat milk', 'ice']}

LAYOUT = ['cheese', 'ketchup', 'egg', 'tuna', 'olives', 'X',
          'onion', 'tomato', 'cucumber', 'avocado', 'lettuce', 'salad dressing', 'X',
          'tomato sauce', 'pesto', 'alfredo', 'parmesan', 'X',
          'milk', 'oat milk', 'ice']

SPACE = 'X'

INGREDIENT_MAP = {'cheese': 0, 'ketchup': 1, 'egg': 2, 'tuna': 3, 'olives': 4,
                  'onion': 6, 'tomato': 7, 'cucumber': 8, 'avocado': 9, 'lettuce': 10, 'salad dressing': 11,
                  'tomato sauce': 13, 'pesto': 14, 'alfredo': 15, 'parmesan': 16,
                  'milk': 18, 'oat milk': 19, 'ice': 20}

ORDER_FORMAT = "Order type: {o_type}, Ingredients: {ing}, Added Ingredients: {add_ing}, Arrival time: {time}, Order num: {num}, timeout: {timeout}"

MAX_TIMEOUT = 50
INIT_QUANTUM = 3
flag = 0
RESTOCK_RNG = (5, 10)
NUM_OF_MINUTES = 60
ORDER_WAIT = 4
TIME_FOR_INGREDIENT = 3
RESTOCK_VAL = 4
INIT_ONLINE_ORDERS = 15
TAKE_ORDER_SCORE = 0
GOTO_SCORE = 0
TAKE_RESTOCK_SCORE = 1
NUM_OF_RUNS = 10
SCORE_PER_INGREDIENT = 2
HEIGHT = 714
WIDTH = 1520
