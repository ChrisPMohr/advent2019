from collections import defaultdict


def main():
    result = 0
    min = 372304
    max = 847060
    for i in range(min, max+1):
        s = list(str(i))
        if len(set(s)) == 6:
            continue
        has_cond = True
        for j in range(0, 5):
            if s[j] > s[j+1]:
                has_cond = False
                break
        if not has_cond:
            continue
        print(s)
        result += 1
    print(result)


if __name__ == '__main__':
    main()
