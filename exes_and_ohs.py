"""
Given four dimensions, print a matrix of Xs and Os

mx = 3   (The count of Xs or Os per row group before it alternates)
Mx = 15  (This is the number of columns)
my = 2   (The count of Xs or Os per column group before it alternates)
My = 8   (This is the number of rows)

Should print:

XXXOOOXXXOOOXXX
XXXOOOXXXOOOXXX
OOOXXXOOOXXXOOO
OOOXXXOOOXXXOOO
XXXOOOXXXOOOXXX
XXXOOOXXXOOOXXX
OOOXXXOOOXXXOOO
OOOXXXOOOXXXOOO

"""


def print_the_matrix(mx, Mx, my, My):
    for i in range(0, Mx * My):
        if i % Mx == 0:
            print()
        if (i // (Mx * my) % 2) == 0:
            if i % Mx // mx % 2 == 0:
                print("X", end='')
            else:
                print("O", end='')
        else:
            if i % Mx // mx % 2 == 0:
                print("O", end='')
            else:
                print("X", end='')
    print()


if __name__ == '__main__':
    print_the_matrix(3, 15, 2, 8)
