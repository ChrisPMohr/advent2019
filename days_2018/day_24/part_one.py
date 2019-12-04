import re


def main():
    with open('input.txt', 'r') as f:
        text = f.read()
        immune_text, infection_text = text.split("\n\n", 1)
        immune_lines = immune_text.strip().split("\n")[1:]
        infection_lines = infection_text.strip().split("\n")[1:]

        immune_armies = [parse_army(line) for line in immune_lines]
        infection_armies = [parse_army(line) for line in infection_lines]

        while immune_armies and infection_armies:
            #print("Immune: {}".format([(army.group_number, army.units) for army in immune_armies]))
            #print("Infection: {}".format([(army.group_number, army.units) for army in infection_armies]))

            targets = target_selection(immune_armies, infection_armies)
            make_attacks(immune_armies, infection_armies, targets)

    print(sum(army.units for army in immune_armies) + sum(army.units for army in infection_armies))


def make_attacks(armies_1, armies_2, targets):
    armies = armies_1 + armies_2
    sorted_armies = sorted(armies, key=lambda army: army.initiative, reverse=True)
    for army in sorted_armies:
        if army not in targets:
            continue
        target = targets[army]
        if target:
            #print("{} is attacking {}".format(army.group_number, target.group_number))
            damage = army.calculate_damage(target)
            target.take_damage(damage)
            if target.units == 0:
                try:
                    armies_1.remove(target)
                except ValueError:
                    pass
                try:
                    armies_2.remove(target)
                except ValueError:
                    pass
                armies.remove(target)


def target_selection(armies_1, armies_2):
    armies_1_to_target = list(armies_1)
    armies_2_to_target = list(armies_2)
    targets = {}
    armies = [(army, 1) for army in armies_1] + [(army, 2) for army in armies_2]
    sorted_armies = sorted(armies, key=target_selection_priority, reverse=True)
    for army, team_num in sorted_armies:
        #print("Picking target for group {}".format(army.group_number))
        target = None
        if team_num == 1:
            if armies_2_to_target:
                target = sorted(armies_2_to_target, key=target_priority(army), reverse=True)[0]
                if army.calculate_damage(target):
                    armies_2_to_target.remove(target)
                    targets[army] = target
        else:
            if armies_1_to_target:
                target = sorted(armies_1_to_target, key=target_priority(army), reverse=True)[0]
                if army.calculate_damage(target):
                    armies_1_to_target.remove(target)
                    targets[army] = target
        #if target:
        #    print("is targeting group {}".format(target.group_number))

    return targets


def target_selection_priority(input):
    army, team_num = input
    return army.effective_power, army.initiative


def target_priority(army):
    def target_priority_for_army(other_army):
        return army.calculate_damage(other_army), other_army.effective_power, other_army.initiative
    return target_priority_for_army


group_number = 1


class Army(object):
    def __init__(self, units: int, hp: int, elements, attack_damage: int, attack_element: str, initiative: int):
        global group_number
        self.group_number = group_number
        group_number += 1

        self.units = units
        self.hp = hp
        self.weaknesses = elements[0]
        self.immunities = elements[1]
        self.attack_damage = attack_damage
        self.attack_element = attack_element
        self.initiative = initiative

    @property
    def effective_power(self):
        return self.units * self.attack_damage

    def calculate_damage(self, defending_army) -> int:
        multiplier = 1
        if defending_army.weaknesses and self.attack_element in defending_army.weaknesses:
            multiplier = 2
        elif defending_army.immunities and self.attack_element in defending_army.immunities:
            multiplier = 0
        #print(self.attack_element, defending_army.weaknesses, defending_army.immunities, multiplier)
        return multiplier * self.effective_power

    def take_damage(self, damage):
        lost_units = min(damage // self.hp, self.units)
        #print("Group {} lost {} units".format(self.group_number, lost_units))
        self.units -= lost_units


def parse_elements(elements_string):
    """
    input: "(immune to bludgeoning, cold; weak to radiation) "
    response: (weaknesses, immunities)
    """
    if not elements_string:
        return None, None

    elements_string = elements_string[1:-2]
    weakness_string = None
    immunity_string = None
    if ';' in elements_string:
        str1, str2 = elements_string.split('; ', 1)
        if 'weak' in str1:
            weakness_string = str1
            immunity_string = str2
        else:
            immunity_string = str1
            weakness_string = str2
    else:
        if 'weak' in elements_string:
            weakness_string = elements_string
        else:
            immunity_string = elements_string
    weaknesses = weakness_string[len("weak to "):].split(', ') if weakness_string else None
    immunities = immunity_string[len("immune to "):].split(', ') if immunity_string else None
    return weaknesses, immunities


def parse_army(line):
    match = re.match(
        r"(\d+) units each with (\d+) hit points (\([^)]+\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)",
        line)
    return Army(
        int(match.group(1)),
        int(match.group(2)),
        parse_elements(match.group(3)),
        int(match.group(4)),
        match.group(5),
        int(match.group(6))
    )


if __name__ == '__main__':
    main()
