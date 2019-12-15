from collections import defaultdict, Counter
import math


def parse_ingredient(s):
    amount, ing = s.split()
    return ing, int(amount)


def parse_line(line):
    ingredients, result = line.split(" => ")
    ingredient_list = ingredients.split(", ")
    return parse_ingredient(result), [parse_ingredient(i) for i in ingredient_list]


def apply_recipes(recipes, needed, leftover, flag=False):
    all_needs = [(k, v) for k, v in needed.items() if k != "ORE"]
    for needed_ing, needed_amount in all_needs:
        recipe_amount, recipe_ings = recipes[needed_ing]
        recipe_quantity = math.ceil(needed_amount / recipe_amount)
        if flag:
            recipe_map = {ing:v for ing,v in recipe_ings}
            if "ORE" in recipe_map.keys():
                ore_recipe_quantity = math.floor(leftover["ORE"] / recipe_map["ORE"])
                if ore_recipe_quantity < recipe_quantity:
                    # print("Limited by ore")
                    pass
                recipe_quantity = min(recipe_quantity, ore_recipe_quantity)
            # print("making", recipe_amount, needed_ing, "<-", recipe_ings, "*", recipe_quantity)
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
        if made_amount >= needed_amount:
            leftover[needed_ing] += made_amount - needed_amount
            del needed[needed_ing]
            return needed, leftover
    raise RuntimeError("Can't satisfy anything")

made = defaultdict(int)
used = defaultdict(int)

def main():
    with open('input1.txt', 'r') as f:
        lines = f.readlines()
        recipes = {}
        for line in lines:
            result, ingredients = parse_line(line)
            recipes[result[0]] = (result[1], ingredients)

    amount_ore = 1000000000000
    init_amount_ore = 1000000000000 // 100000
    extra_ore_1 = init_amount_ore * 1000
    extra_ore_2 = amount_ore - init_amount_ore - extra_ore_1

    leftover = defaultdict(int)
    needed = defaultdict(int)
    needed["FUEL"] = 1
    while len(needed) > 1 or "ORE" not in needed:
        needed, leftover = apply_recipes(recipes, needed, leftover)

    made_fuel = leftover["FUEL"] + 1

    print('-'*80)
    print("single sample")
    print("fuel:", made_fuel)
    print("n", needed)
    print("l", leftover)

    del leftover["FUEL"]
    ore_per_fuel_recipe = needed["ORE"]
    amount_ore = init_amount_ore
    num_fuel_recipes = math.floor(amount_ore/ore_per_fuel_recipe)
    num_fuel_recipes = int(num_fuel_recipes * 8 / 10)
    total_made_fuel = num_fuel_recipes * made_fuel
    del needed["ORE"]
    for ing in leftover:
        leftover[ing] *= num_fuel_recipes
    leftover["ORE"] = amount_ore - num_fuel_recipes * ore_per_fuel_recipe

    print('-'*80)
    print("mass production 1")
    print("fuel:", total_made_fuel)
    print("n", needed)
    print("l", leftover)

    spent_ore = init_amount_ore

    got_extra = False

    while "ORE" not in needed:
        try:
            if not needed:
                needed["FUEL"] = 1
            while len(needed) > 0:
                # print("n", needed)
                # print("l", leftover)
                needed, leftover = apply_recipes(recipes, needed, leftover, True)
            total_made_fuel += leftover["FUEL"] + 1
            del leftover["FUEL"]
        except RuntimeError:
            if got_extra:
                break
            else:
                print('-' * 80)
                print("injecting extra ore")
                print("fuel:", total_made_fuel)
                print("n", needed)
                print("l", leftover)
                leftover["ORE"] += extra_ore_1
                spent_ore += extra_ore_1
                got_extra = True

    print('-'*80)
    print("finished extra stage 1")
    print("fuel:", total_made_fuel)
    print("n", needed)
    print("l", leftover)

    ore_per_fuel_recipe = spent_ore - leftover["ORE"]
    print("ore per fuel recipe", ore_per_fuel_recipe)
    leftover["ORE"] += extra_ore_2
    num_fuel_recipes = math.floor(leftover["ORE"]/ore_per_fuel_recipe)
    print("num fuel recipes", num_fuel_recipes)
    print("spending ore", num_fuel_recipes * ore_per_fuel_recipe)
    total_made_fuel *= num_fuel_recipes
    for ing in leftover:
        if ing != "ORE":
            leftover[ing] *= num_fuel_recipes
    leftover["ORE"] -= num_fuel_recipes * ore_per_fuel_recipe

    print('-'*80)
    print("mass production 2")
    print("fuel:", total_made_fuel)
    print("n", needed)
    print("l", leftover)

    while "ORE" not in needed:
        try:
            if not(needed):
                needed["FUEL"] = 1
            while len(needed) > 0:
                # print("n", needed)
                # print("l", leftover)
                needed, leftover = apply_recipes(recipes, needed, leftover, True)
            total_made_fuel += leftover["FUEL"] + 1
            del leftover["FUEL"]
        except RuntimeError:
            print("Done")
            print("fuel:", total_made_fuel)
            print("n", needed)
            print("l", leftover)


if __name__ == '__main__':
    main()
