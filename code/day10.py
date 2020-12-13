
def parse(filename):
    ret_val = []
    with open(filename) as f:
        for line in f:
            ret_val.append(int(line.strip()))
    ret_val.append(0) # append the wall
    ret_val.append(max(ret_val) + 3) # append your device
    return ret_val


def puzzle1():
    adaptors = sorted(parse('../data/day10.txt'))
    count_1 = 0
    count_3 = 0
    for i in range(len(adaptors)-1):
        diff = abs(adaptors[i+1] - adaptors[i])
        if diff == 1:
            count_1 += 1
        elif diff == 3:
            count_3 += 1
        else:
            raise ValueError(f'Diff was: {diff}')
    print(f'Diff of 1: {count_1}, Diff of 3: {count_3}, Product = {count_3*count_1}')


def get_child_idxs(adaptors, curr_idx):
    ''' return the next 3 adaptors in the list assuming they are valid to use against this'''
    if len(adaptors) == 1:
        return None # last adaptor (our device)
    else:
        ret_val = []
        parent_jolt = adaptors[curr_idx]
        for i in range(curr_idx+1, min(curr_idx+4, len(adaptors))):
            if adaptors[i] - parent_jolt <= 3:
                ret_val.append(i)
        return ret_val


def num_valid_paths(adaptors, curr_idx, visited_map):
    child_idxs = get_child_idxs(adaptors, curr_idx)
    num_paths = 0

    # don't recurse if we've seen this branch before
    if curr_idx in visited_map:
        return visited_map.get(curr_idx)

    # degenerate case - leaf node
    if not child_idxs:
        num_paths = 1

    # recursive case - children exist
    for child_idx in child_idxs:
        num_paths += num_valid_paths(adaptors, child_idx, visited_map)

    # add this idx to visited with num_paths before returning
    visited_map[curr_idx] = num_paths
    return num_paths


def puzzle2():
    '''
    Approach: traverse as a tree with branch factor = 3.
    For each node in the tree, the next 3 in the array are its children.  Do a depth-first traversal, but only traverse
    if the value of the child node is 1, 2, or 3 greater than the parent.  If you reach a leaf node (our device),
    add one to a global counter.

    Return the global counter as the number of possible valid combinations
    '''
    adaptors = sorted(parse('../data/day10.txt'))
    valid_combos = num_valid_paths(adaptors, 0, {})
    print(f'# of valid combos: {valid_combos}')


# puzzle1()
puzzle2()