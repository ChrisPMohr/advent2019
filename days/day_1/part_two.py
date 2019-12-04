def main():
    fuel_values = []
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            mass = int(line.strip())
            total_fuel = calc_fuel(mass)
            fuel_values.append(total_fuel)
    print(sum(fuel_values))


def calc_fuel(mass):
    total_fuel = 0
    while mass > 0:
        fuel = max(mass // 3 - 2, 0)
        total_fuel += fuel
        mass = fuel
    return total_fuel

if __name__ == '__main__':
    main()
