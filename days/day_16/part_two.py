from collections import defaultdict, Counter
import math
import itertools

def fft(seq):
    result = []
    total_sum = sum(seq)
    for v in seq:
        result.append(total_sum%10)
        total_sum -= v
    return result


def main():
    result = None
    with open('input.txt', 'r') as f:
        line = f.readline().strip()
        ints = [int(c) for c in line] * 10000
        message_offset = int(line[:7])
        print(message_offset)
        print(len(ints))
        ints = ints[message_offset:]
        for i in range(100):
            print(i)
            ints = fft(ints)
    print(''.join([str(i) for i in ints[:8]]))


if __name__ == '__main__':
    main()
