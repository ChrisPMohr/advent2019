from collections import defaultdict


def main():
    result = 0
    min = 372304
    max = 847060
    for i in range(min, max+1):
        digits = list(str(i))
        if is_non_decreasing(digits) and has_repeating_characters(digits):
            result += 1
    print(result)


def is_non_decreasing(digits):
    for j in range(0, 5):
        if digits[j] > digits[j+1]:
            return False
    return True


def has_repeating_characters(digits):
    return len(set(digits)) < 6


if __name__ == '__main__':
    main()
