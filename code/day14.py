import re
import itertools
import copy

class Instruction:

    def __init__(self, mem_loc, value):
        self.mem_loc = mem_loc
        self.value = value

    def get_masked_val(self, mask):
        # find binary representation of 'value'
        masked_arr = list('{:036b}'.format(self.value))
        #apply the bit mask to it
        for i in range(0, len(mask)):
            if mask[i] == 'X':
                continue
            else:
                masked_arr[i] = mask[i]

        return int(''.join(masked_arr), 2)

    def get_decoder2_vals(self, mask):
        # find binary representation of 'mem_loc'
        masked_arr = list('{:036b}'.format(self.mem_loc))
        # apply the bit mask to it
        for i in range(0, len(mask)):
            if mask[i] == '0':
                continue
            elif mask[i] == '1':
                masked_arr[i] = '1'
            else:
                masked_arr[i] = 'X'
        # explode masked_arr into every combo of possible values
        # return int representations of all those combos
        return get_all_possible_mem_loc(masked_arr)

    def __str__(self):
        return f'mem[{self.mem_loc}] = {self.value}'

    def __repr__(self):
        return self.__str__()


def get_all_possible_mem_loc(mem_loc_arr):
    num_floats = mem_loc_arr.count('X')
    combos = list(itertools.product(['0', '1'], repeat=num_floats))

    ret_val = []
    for c in combos:
        # Replace the 1st elt in combo with the 1st X in mem_loc_arr, 2nd elt in combo with the 2nd X in mem_loc_arr, etc
        replacement = copy.deepcopy(mem_loc_arr)
        i = 0
        for j in range(0, len(replacement)):
            if replacement[j] == 'X':
                replacement[j] = c[i]
                i += 1
        ret_val.append(int(''.join(replacement), 2))
    return ret_val

def parse(filename):
    ret_val = []
    mask_pattern = re.compile('mask = (.*)')
    instr_pattern = re.compile('mem\[(\d+)\] = (\d+)')
    with open(filename) as f:
        for line in f:
            mask_match = mask_pattern.match(line.strip())
            if mask_match:
                ret_val.append(mask_match.group(1).strip())
            else:
                match = instr_pattern.match(line.strip())
                ret_val.append(Instruction(int(match.group(1)), int(match.group(2))))
    return ret_val


def puzzle1(filename):
    instructions = parse(filename)
    memory_map = {}
    curr_mask = None
    for instr in instructions:
        if isinstance(instr, Instruction):
            memory_map[instr.mem_loc] = instr.get_masked_val(curr_mask)
        else:
            curr_mask = list(instr)

    print(sum(memory_map.values()))


def puzzle2(filename):
    instructions = parse(filename)

    memory_map = {}
    curr_mask = None
    for instr in instructions:
        if isinstance(instr, Instruction):
            for mem_loc in instr.get_decoder2_vals(curr_mask):
                memory_map[mem_loc] = instr.value
        else:
            curr_mask = list(instr)

    print(sum(memory_map.values()))

# puzzle1('../data/day14.txt')
puzzle2('../data/day14.txt')