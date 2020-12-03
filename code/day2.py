from abc import ABC, abstractmethod


class Rule(ABC):

    def __init__(self, rule_str):
        super().__init__()
        tokens = rule_str.split(' ')
        range_str = tokens[0]
        range = range_str.split('-')

        self.char = tokens[1].strip()
        self.min = int(range[0])
        self.max = int(range[1])

    def __str__(self):
        return '%s-%s %s' % (self.min, self.max, self.char)

    @abstractmethod
    def is_valid(self, password):
        pass


class Rule1(Rule):

    def is_valid(self, password):
        pwd_chars = list(password)
        char_only = list(filter(lambda x: (x == self.char), pwd_chars))
        return len(char_only) in range(self.min, self.max + 1)


class Rule2(Rule):

    def is_valid(self, password):
        pwd_chars = list(password)
        first_char = pwd_chars[self.min - 1]
        second_char = pwd_chars[self.max - 1]
        return (first_char == self.char) != (second_char == self.char)


def parse(filepath):
    with open(filepath) as f:
        for line in f:
            yield [x.strip() for x in line.split(':')]


def puzzle_solver(create_rule):
    count = 0
    for tokens in parse('../data/day2.txt'):
        rule = create_rule(tokens[0])
        password = tokens[1]

        # print('%s, %s -- is_valid: %s' % (rule, password, rule.is_valid(password)))
        if rule.is_valid(password):
            count += 1

    print(count)


def puzzle1():
    puzzle_solver(lambda rule_str: Rule1(rule_str))


def puzzle2():
    puzzle_solver(lambda rule_str: Rule2(rule_str))


puzzle1()
puzzle2()