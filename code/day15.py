def parse(filename):
    with open(filename) as f:
        for line in f:
            return [int(x) for x in line.strip().split(',')]

def get_init_map(arr):
    ret_val = dict()
    for i in range(0, len(arr)):
        val = arr[i]
        ret_val[val] = (None, i+1)
    return ret_val

def puzzle1(filename, limit):
    init = parse(filename)
    visited = get_init_map(init)
    val = init[-1]
    curr_idx = len(init) + 1
    last_was_new = True
    # print(",".join(str(i) for i in init))

    while curr_idx <= limit:
        if last_was_new:
            val = 0
        else:
            tuple = visited.get(val)
            val = tuple[1] - tuple[0]

        # print(val)
        last_was_new = val not in visited
        if last_was_new:
            visited[val] = (None, curr_idx)
        else:
            update_map_val(visited, val, curr_idx)
        curr_idx += 1

        # debugging statement to see how far along we are
        if curr_idx % 100000 == 0:
            print(f'idx = {curr_idx}')

    print(val)

def update_map_val(map, val, curr_idx):
    tuple = map.get(val)
    map[val] = (tuple[1], curr_idx)



# puzzle1('../data/helper.txt', 2020)
puzzle1('../data/helper.txt', 30000000)