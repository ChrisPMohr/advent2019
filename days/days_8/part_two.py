from collections import defaultdict, Counter


def main():
    width = 25
    height = 6
    image = [[-1] * width for _ in range(height)]
    for line in image:
        print(line)
    set_num = 0
    with open('input.txt', 'r') as f:
        line = f.readline().strip()
        while line:
            layer = line[:width*height]
            line = line[width*height:]
            for j in range(height):
                for i in range(width):
                    pixel = layer[i + j*width]
                    if image[j][i] == -1 and pixel != '2':
                        print("setting ",i,j)
                        set_num += 1
                        image[j][i] = pixel

    print(set_num)
    for line in image:
        print(line)


if __name__ == '__main__':
    main()
