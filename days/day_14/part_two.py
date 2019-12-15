from collections import defaultdict, Counter
import math


def parse_ingredient(s):
    amount, ing = s.split()
    return ing, int(amount)


def parse_line(line):
    ingredients, result = line.split(" => ")
    ingredient_list = ingredients.split(", ")
    return parse_ingredient(result), [parse_ingredient(i) for i in ingredient_list]


def main():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        recipes = {}
        for line in lines:
            result, ingredients = parse_line(line)
            recipes[result[0]] = (result[1], ingredients)

    ore_per_fuel = make_fuel(recipes, 1)
    total_ore = 1000000000000

    # find upper bound
    lower_bound = total_ore // ore_per_fuel
    while True:
        upper_bound = math.floor(lower_bound * 1.1)
        if make_fuel(recipes, upper_bound) > total_ore:
            break
        lower_bound = upper_bound

    # binary search between bounds
    while upper_bound - lower_bound > 1:
        current_test = (upper_bound - lower_bound) // 2 + lower_bound
        print(lower_bound, current_test, upper_bound)
        needed_ore = make_fuel(recipes, current_test)
        if needed_ore > total_ore:
            upper_bound = current_test
        else:
            lower_bound = current_test

    print(lower_bound)


def make_fuel(recipes, n_fuel):
    leftover = defaultdict(int)
    needed = defaultdict(int)
    needed["FUEL"] = n_fuel
    while len(needed) > 1 or "ORE" not in needed:
        needed_ing, needed_amount = [(k,v) for k,v in needed.items() if k != "ORE"][0]
        recipe_amount, recipe_ings = recipes[needed_ing]
        # print("Want", needed_amount, needed_ing)
        recipe_quantity = math.ceil(needed_amount / recipe_amount)
        # print("Making", recipe_quantity, "of recipe", recipe_ings)
        for ing, amount in recipe_ings:
            amount *= recipe_quantity
            if ing in leftover:
                leftover_amount = min(leftover[ing], amount)
                leftover[ing] -= leftover_amount
                amount -= leftover_amount
                if leftover[ing] == 0:
                    del leftover[ing]
            if amount > 0:
                needed[ing] += amount
        made_amount = recipe_quantity * recipe_amount
        leftover[needed_ing] += made_amount - needed_amount
        # print('leftovers', leftover)
        del needed[needed_ing]

    return needed["ORE"]


if __name__ == '__main__':
    main()
