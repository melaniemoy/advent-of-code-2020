import re

class TicketFieldRule:

    def __init__(self, name, ranges):
        self.name = name
        self.ranges = ranges

    def is_valid(self, value):
        for r in self.ranges:
            if value in range(r[0], r[1]+1):
                return True
        return False

    def contains_one_valid_val(self, arr):
        # returns true if even one value falls in acceptable ranges
        for x in arr:
            if self.is_valid(x):
                return True
        return False

    def is_valid_for_all(self, values):
        for v in values:
            if not self.is_valid(v):
                return False
        return True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def parse(filename):
    # first set of lines is the fields
    # second set of lines is your ticket
    # third set is nearby tickets

    rule_pattern = re.compile('([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)')
    rules = []
    your_ticket = None
    nearby_tickets = []
    set = 1
    with open(filename) as f:
        for line in f:
            if line == '\n':
                set += 1
                continue

            if set == 1:
                # create rules
                match = rule_pattern.match(line.strip())
                ranges = [(int(match.group(2)), int(match.group(3))),
                          (int(match.group(4)), int(match.group(5)))]
                rules.append(TicketFieldRule(match.group(1), ranges))

            elif set == 2 and not line.startswith('your'):
                # create your ticket
                your_ticket = parse_ticket(line.strip())

            elif set == 3 and not line.startswith('nearby'):
                # create nearby tickets
                nearby_tickets.append(parse_ticket(line.strip()))

    return rules, your_ticket, nearby_tickets


def parse_ticket(line):
    return [int(x) for x in line.split(',')]


def puzzle1(filename):
    rules, your_ticket, nearby_tickets = parse(filename)
    invalid_values = get_global_invalid_values(rules, nearby_tickets)
    print (sum(invalid_values))


def get_global_invalid_values(rules, tickets):
    invalid_values = [val for ticket in tickets for val in ticket]
    for r in rules:
        invalid_values = [x for x in invalid_values if not r.is_valid(x)]
    return invalid_values


def get_valid_tickets(rules, tickets):
    global_invalids = set(get_global_invalid_values(rules, tickets))
    ret_val = []
    for t in tickets:
        if len((set(t) & global_invalids)) == 0:
            ret_val.append(t)
    return ret_val


def pivot_matrix(matrix):
    ret_val = []
    for j in range(0, len(matrix[0])):
        new_row = []
        for i in range(0, len(matrix)):
            new_row.append(matrix[i][j])
        ret_val.append(new_row)
    return ret_val


def get_possible_rules(values_by_position, rules):
    ret_val = []
    for column in values_by_position:
        valid_rules = []
        for r in rules:
            if r.is_valid_for_all(column):
                valid_rules.append(r)
        ret_val.append(valid_rules)

    return ret_val


def reduce_possible_rules(possible_rules):
    # get just the names of the rules
    for i in range(0, len(possible_rules)):
        prs = possible_rules[i]
        possible_rules[i] = [x.name for x in prs]

    # find any position that has one one possible rule.  Remove that rule from all other positions.
    # repeat to remove any positions that only have 1 possibility
    determined_rules=[None] * len(possible_rules)

    while True:
        newly_determined_rules = []
        for i in range(0, len(possible_rules)):
            pr = possible_rules[i]
            if len(pr) == 1:
                rule = pr[0]
                determined_rules[i] = rule
                newly_determined_rules.append(rule)

        if not newly_determined_rules:
            # no new rules determined
            break

        # remove determined_rules from possible_rules
        for r in newly_determined_rules:
            for pr in possible_rules:
                if r in pr:
                    pr.remove(r)

    return determined_rules







def puzzle2(filename):
    rules, your_ticket, nearby_tickets = parse(filename)
    valid_tickets = get_valid_tickets(rules, nearby_tickets)
    possible_rules = get_possible_rules(pivot_matrix(valid_tickets), rules)
    rules_in_order = reduce_possible_rules(possible_rules)

    product = 1
    for i in range(0, len(rules_in_order)):
        if rules_in_order[i].startswith('departure'):
            product *= your_ticket[i]
    print(product)

# puzzle1('../data/day16.txt')
puzzle2('../data/day16.txt')
