def main():
    fuel_values = []
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            mass = int(line.strip())
            total_fuel = mass // 3 - 2
            fuel_values.append(total_fuel)
    print(sum(fuel_values))


if __name__ == '__main__':
    main()
