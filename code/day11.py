import itertools

class SeatMatrix:
    OCCUPIED = '#'
    EMPTY = 'L'
    FLOOR = '.'

    def __init__(self, arr):
        self.matrix = arr
        self.num_rows = len(self.matrix)
        self.num_cols = len(self.matrix[0])

    def get_seat_val(self, r, c):
        return self.matrix[r][c]

    def count_immediate_neighbors(self, row, column):
        rows = [row + r for r in [-1, 0, 1] if 0 <= row + r < self.num_rows]
        columns = [column + c for c in [-1, 0, 1] if 0 <= column + c < self.num_cols]
        neighbors = 0
        for r in rows:
            for c in columns:
                if r == row and c == column:
                    continue
                if self.get_seat_val(r, c) == SeatMatrix.OCCUPIED:
                    neighbors += 1
        return neighbors

    def count_next_neighbors(self, row, column):
        neighbors = 0

        # 'directions' contains tuples representing the direction the person is looking
        # -1, -1 means they are looking at the towards the row and column behind them
        # 'scalar' represents how far in that direction they are looking
        # Increase scalar until a border has been reached
        directions = list(itertools.product([-1, 0, 1], [-1, 0, 1]))
        for dr, dc in directions:
            scalar = 1
            if dr == 0 and dc == 0:
                continue
            r = row + dr * scalar
            c = column + dc * scalar
            while r in range(0, self.num_rows) and c in range(0, self.num_cols):
                curr_neighbor = self.get_seat_val(r, c)
                if curr_neighbor == SeatMatrix.EMPTY:
                    break
                elif curr_neighbor == SeatMatrix.OCCUPIED:
                    neighbors +=1
                    break   #no need to look in this direction, found an occupied seat
                scalar += 1
                r = row + dr * scalar
                c = column + dc * scalar

        return neighbors

    def equals(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            return False
        for i in range(0, self.num_rows):
            for j in range(0, self.num_cols):
                if self.get_seat_val(i, j) != other.get_seat_val(i, j):
                    return False
        return True


    def __str__(self):
        return '\n'.join([''.join(row) for row in self.matrix])

    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.matrix])


def load_matrix(filename):
    ret_val = []
    with open(filename) as f:
        for line in f:
            ret_val.append(list(line.strip()))
    return SeatMatrix(ret_val)


def empty_matrix(num_rows, num_columns):
    return [[0 for i in range(num_columns)] for j in range(num_rows)]

def recommended_state_change(matrix, row, column):
    '''
    - If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    - If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    - Otherwise, the seat's state does not change.
    '''
    curr_val = matrix.get_seat_val(row, column)
    if curr_val == SeatMatrix.FLOOR:
        return curr_val
    else:
        num_neighbors = matrix.count_immediate_neighbors(row, column)
        if curr_val == SeatMatrix.EMPTY and num_neighbors == 0:
            return SeatMatrix.OCCUPIED
        elif curr_val == SeatMatrix.OCCUPIED and num_neighbors >= 4:
            return SeatMatrix.EMPTY
        else:
            return curr_val


def recommended_state_change2(matrix, row, column):
    '''
        - If a seat is empty (L) and there are no occupied seats visible to it in 8 directions, the seat becomes occupied.
        - If a seat is occupied (#) and FIVE or more seats visible to it are also occupied, the seat becomes empty.
        - Otherwise, the seat's state does not change.
        '''
    curr_val = matrix.get_seat_val(row, column)
    if curr_val == SeatMatrix.FLOOR:
        return curr_val
    else:
        num_neighbors = matrix.count_next_neighbors(row, column)
        if curr_val == SeatMatrix.EMPTY and num_neighbors == 0:
            return SeatMatrix.OCCUPIED
        elif curr_val == SeatMatrix.OCCUPIED and num_neighbors >= 5:
            return SeatMatrix.EMPTY
        else:
            return curr_val


def get_updated_seating_matrix(matrix, recommendation_func):
    after_matrix = empty_matrix(matrix.num_rows, matrix.num_cols)
    for r in range(0, matrix.num_rows):
        for c in range(0, matrix.num_cols):
            after_matrix[r][c] = recommendation_func(matrix, r, c)
    return SeatMatrix(after_matrix)


def get_num_occupied(matrix):
    count = 0
    for r in range(0, matrix.num_rows):
        for c in range(0, matrix.num_cols):
            if matrix.get_seat_val(r, c) == SeatMatrix.OCCUPIED:
                count += 1
    return count


def puzzle1(filename):
    matrix = load_matrix(filename)
    stabilized_seating = False

    while not stabilized_seating:
        new_seat_matrix = get_updated_seating_matrix(matrix, recommended_state_change)

        print(new_seat_matrix)
        stabilized_seating = matrix.equals(new_seat_matrix)
        print()

        matrix = new_seat_matrix

    # count occupied seats
    print(get_num_occupied(matrix))


def puzzle2(filename):
    matrix = load_matrix(filename)
    stabilized_seating = False

    while not stabilized_seating:
        new_seat_matrix = get_updated_seating_matrix(matrix, recommended_state_change2)

        print(new_seat_matrix)
        stabilized_seating = matrix.equals(new_seat_matrix)
        print()

        matrix = new_seat_matrix

    # count occupied seats
    print(get_num_occupied(matrix))


# puzzle1('../data/day11.txt')
puzzle2('../data/day11.txt')