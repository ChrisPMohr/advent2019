from collections import defaultdict, Counter


def main():
    size = 25 * 6
    with open('input.txt', 'r') as f:
        line = f.readline().strip()
        most_0 = 10000
        answer = 0
        while line:
            layer = line[:size]
            line = line[size:]
            c = Counter(layer)
            print(c)
            if c['0'] < most_0:
                print("best")
                most_0 = c['0']
                answer = c['1']*c['2']

    print(answer)


if __name__ == '__main__':
    main()
