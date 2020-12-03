class TopologyMatrix:
    TREE = '#'
    SPACE = '.'

    def __init__(self, arr):
        self.matrix = arr
        self.num_rows = len(self.matrix)
        self.num_cols = len(self.matrix[0])

    def is_tree(self, x, y):
        x_coord = x % self.num_cols
        return self.matrix[y][x_coord] == TopologyMatrix.TREE


def load_matrix(filename):
    ret_val = []
    with open(filename) as f:
        for line in f:
            ret_val.append(list(line.strip()))
    return TopologyMatrix(ret_val)


def count_trees(matrix, x, y):
    curr_x = 0
    curr_y = 0
    count = 0

    while curr_y + y < matrix.num_rows:
        curr_x += x
        curr_y += y

        if matrix.is_tree(curr_x, curr_y):
            count += 1

    return count


def puzzle1():

    # load input into matrix
    matrix = load_matrix('../data/day3.txt')
    print(count_trees(matrix, 3, 1))

def puzzle2():

    attempts = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    matrix = load_matrix('../data/day3.txt')

    product = 1
    for x,y in attempts:
        product *= count_trees(matrix, x, y)

    print(product)

puzzle1()
puzzle2()