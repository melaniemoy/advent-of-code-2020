# read a file and find 2 numbers that sum to 2020.  Return the product of these two numbers


def sum_exists(arr, sum):
    entries = set()

    for i in arr:
        if sum - i in entries:
            return (i, sum-i)
        else:
            entries.add(i)
    return (None, None)


def puzzle1():
    with open('../data/day1.txt') as f:
        input_array = [int(line.strip()) for line in f]
        x,y = sum_exists(input_array, 2020)
        if x:
            print(x*y)


def puzzle2():
    with open('../data/day1.txt') as f:
        input_array = [int(line.strip()) for line in f]
        copy_array = input_array.copy()
        for curr_int in input_array:
            copy_array.remove(curr_int)
            x,y = sum_exists(copy_array, 2020-curr_int)
            if x:
                # print('%s, %s, %s' % (curr_int, x, y))
                print(curr_int * x * y)
            else:
                copy_array.append(curr_int)

puzzle1()
puzzle2()