'''
--- Day 7: Handy Haversacks ---
You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)


--- Part Two ---
It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

faded blue bags contain 0 other bags.
dotted black bags contain 0 other bags.
vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?


'''

import re

PATTERN = re.compile('([\d]+) ([a-zA-Z ]+)')


def parse_container_str(container):
    return container.replace('bags', '').strip()

def parse_content_str(content):
    # strip bag or bags and trailing periods
    if content == 'no other bags.':
        return None, None
    else:
        count_and_descr = content.strip().replace('bags', '').replace('bag', '').strip()
        match = PATTERN.match(count_and_descr)
        num = int(match.group(1))
        descr = match.group(2).strip()
        return num, descr


def parse1():
    ret_val = {}
    with open('../data/day7.txt') as f:
        for line in f:
            rule_data = line.strip().split('contain')
            container = parse_container_str(rule_data[0])
            contents = [r.strip() for r in rule_data[1].split(',')]
            for c in contents:
                clean_content = parse_content_str(c)
                descr = clean_content[1]
                if not clean_content or not descr:
                    continue
                if descr not in ret_val:
                    ret_val[descr] = [container]
                else:
                    ret_val.get(descr).append(container)
    return ret_val


def trace_up_tree(bag_descr, bags_to_containers):
    curr_containers = bags_to_containers.get(bag_descr) # a list of valid containers
    all_containers = set()
    while curr_containers:
        for c in curr_containers:
            curr_containers.remove(c)
            all_containers.add(c)
            x = bags_to_containers.get(c)
            if x:
                new_containers = [item for item in x if item not in all_containers] # only add containers we haven't checked before
                curr_containers.extend(new_containers)
    return len(all_containers)


def puzzle1():
    # key is a bag, value is a list of valid IMMEDIATE containers of this bag
    bags_to_containers = parse1()
    print(trace_up_tree('shiny gold', bags_to_containers))


def parse2():
    ret_val = {}
    with open('../data/day7.txt') as f:
        for line in f:
            rule_data = line.strip().split('contain')
            container = parse_container_str(rule_data[0])
            contents = [parse_content_str(r.strip()) for r in rule_data[1].split(',')]
            if contents[0][0]:
                ret_val[container] = contents
            else:
                ret_val[container] = None
    return ret_val


def tree_count_helper(parent_to_child, parent):
    ''' returns the size of tree including this parent '''
    children = parent_to_child.get(parent)
    if not children:
        # leaf node
        return 1
    else:
        total = 1 # include the parent
        for c in children:
            num = c[0]
            descr = c[1]
            total += num * tree_count_helper(parent_to_child, descr)
        return total


def puzzle2():
    container_to_contents = parse2()
    total = tree_count_helper(container_to_contents, 'shiny gold')
    print(total - 1)

puzzle1()
puzzle2()