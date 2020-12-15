'''
--- Day 12: Rain Risk ---
Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety, it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values. After staring at them for a few minutes, you work out what they probably mean:

Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.
The ship starts by facing east. Only the L and R actions change the direction the ship is facing. (That is, if the ship is facing east and the next instruction is N10, the ship would move north 10 units, but would still move east if the following action were F.)

For example:

F10
N3
F7
R90
F11
These instructions would be handled as follows:

F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
N3 would move the ship 3 units north to east 10, north 3.
F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
F11 would move the ship 11 units south to east 17, south 8.
At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?

--- Part Two ---
Before you can give the destination to the captain, you realize that the actual action meanings were printed on the back of the instructions the whole time.

Almost all of the actions indicate how to move a waypoint which is relative to the ship's position:

Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
Action F means to move forward to the waypoint a number of times equal to the given value.
The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is relative to the ship; that is, if the ship moves, the waypoint moves with it.

For example, using the same instructions as above:

F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), leaving the ship at east 100, north 10. The waypoint stays 10 units east and 1 unit north of the ship.
N3 moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The ship remains at east 100, north 10.
F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), leaving the ship at east 170, north 38. The waypoint stays 10 units east and 4 units north of the ship.
R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east and 10 units south of the ship. The ship remains at east 170, north 38.
F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), leaving the ship at east 214, south 72. The waypoint stays 4 units east and 10 units south of the ship.
After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?

'''
import re
import math


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __str__(self):
        return f'({self.x}, {self.y})'


class Instruction:
    CARDINAL_ACTIONS_MAP = {
            'N': Point(0,1),
            'S': Point(0,-1),
            'E': Point(1,0),
            'W': Point(-1,0)
        }
    TURN_ACTIONS = {'R', 'L'}

    def __init__(self, action, value):
        self.action = action
        self.value = value

    def is_cardinal(self):
        return self.action in Instruction.CARDINAL_ACTIONS_MAP

    def is_turn(self):
        return self.action in Instruction.TURN_ACTIONS

    def get_cardinal_point(self):
        if self.is_cardinal():
            return Instruction.CARDINAL_ACTIONS_MAP.get(self.action) * self.value
        else:
            raise NotImplementedError

    def __str__(self):
        return f'({self.action}, {self.value})'


def parse(filename):
    pattern = re.compile("([NSEWLRF])(\\d+)")
    ret_val = []

    with open(filename) as f:
        for line in f:
            match = pattern.match(line.strip())
            action = match.group(1)
            value = int(match.group(2))
            ret_val.append(Instruction(action, value))

    return ret_val


def get_new_angle(curr_angle, turn_instruction):
    # right is clockwise, left is counter-clockwise
    angle_sign = - 1 if turn_instruction.action == 'R' else 1
    new_angle = (curr_angle + angle_sign * turn_instruction.value) % 360
    return new_angle


def get_direction(angle):
    x = round(math.cos(math.radians(angle)))
    y = round(math.sin(math.radians(angle)))

    return Point(x,y)


def rotate(point, instr):
    angle_sign = - 1 if instr.action == 'R' else 1
    theta = math.radians(angle_sign * instr.value)
    x_prime = round(math.cos(theta) * point.x - math.sin(theta) * point.y)
    y_prime = round(math.sin(theta) * point.x + math.cos(theta) * point.y)
    return Point(x_prime, y_prime)

def get_manhattan_distance(point):
    return abs(point.x) + abs(point.y)


def puzzle1(filename):
    instructions = parse(filename)
    curr_angle = 0  # facing due east
    curr_location = Point(0, 0)
    for instr in instructions:
        if instr.is_cardinal():
            curr_location = instr.get_cardinal_point() + curr_location
        elif instr.is_turn():
            curr_angle = get_new_angle(curr_angle, instr)
        elif instr.action == 'F':
            curr_location = curr_location + (get_direction(curr_angle) * instr.value)
    print(get_manhattan_distance(curr_location))


def puzzle2(filename):
    instructions = parse(filename)
    curr_location = Point(0, 0)
    curr_waypoint = Point(10, 1) # 10 units east and 1 unit north
    for instr in instructions:
        if instr.is_cardinal():
            curr_waypoint = instr.get_cardinal_point() + curr_waypoint
        elif instr.is_turn():
            curr_waypoint = rotate(curr_waypoint, instr)
        elif instr.action == 'F':
            # move the ship towards the waypoint instr.value times
            curr_location = curr_location + curr_waypoint * instr.value

    print(get_manhattan_distance(curr_location))

# puzzle1('../data/day12.txt')
puzzle2('../data/day12.txt')