from collections import defaultdict, Counter
import math
import itertools

def fft(seq):
    result = []
    for i in range(1, len(seq) + 1):
        vals = [0] * i + [1] * i + [0] * i + [-1]*i
        total = 0
        for j, v in enumerate(seq):
            p = vals[(j+1) % len(vals)]
            total += v*p
        result.append(abs(total) % 10)
    return result


def main():
    result = None
    with open('input.txt', 'r') as f:
        line = f.readline().strip()
        ints = [int(c) for c in line]
        for i in range(100):
            print(i)
            ints = fft(ints)
    print(ints[:8])


if __name__ == '__main__':
    main()
