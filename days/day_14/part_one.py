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

    leftover = defaultdict(int)
    needed = defaultdict(int)
    needed["FUEL"] = 1
    while len(needed) > 1 or "ORE" not in needed:
        needed_ing, needed_amount = [(k,v) for k,v in needed.items() if k != "ORE"][0]
        recipe_amount, recipe_ings = recipes[needed_ing]
        print("Want", needed_amount, needed_ing)
        recipe_quantity = math.ceil(needed_amount / recipe_amount)
        print("Making", recipe_quantity, "of recipe", recipe_ings)
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
        print('leftovers', leftover)
        del needed[needed_ing]

    print(needed["ORE"])
    print(leftover)


if __name__ == '__main__':
    main()
