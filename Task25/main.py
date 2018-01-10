from collections import namedtuple, defaultdict
import re

re_begin_state = re.compile(r'^Begin in state ([A-Z]+)\.$')
re_iterations = re.compile(r'^Perform a diagnostic checksum after (\d+) steps\.$')
re_in_state = re.compile(r'^In state ([A-Z]+)\:$')
re_value = re.compile(r'^If the current value is (0|1)\:$')
re_cmd_write = re.compile(r'^\- Write the value (0|1)\.$')
re_cmd_move = re.compile(r'^\- Move one slot to the (right|left)\.$')
re_cmd_next_state = re.compile(r'^\- Continue with state ([A-Z]+)\.$')

Rule = namedtuple('Rule', 'new_value move_direction next_state')

MOVE_DIRECTIONS = {'left': -1, 'right': 1}

def parse_one_rule(lines):
    value = re_value.match(lines[0]).group(1)
    value = int(value)
    
    new_value = re_cmd_write.match(lines[1]).group(1)
    new_value = int(new_value)
    
    move_direction = re_cmd_move.match(lines[2]).group(1)
    move_direction = MOVE_DIRECTIONS[move_direction]
    
    next_state = re_cmd_next_state.match(lines[3]).group(1)
    return value, Rule(new_value, move_direction, next_state)


def main():
    rules = {}
    tape = defaultdict(int)
    
    with open('data.txt') as fd:
        blocks = []
        
        for block in fd.read().split('\n\n'):
            blocks.append(list(map(str.strip, block.split('\n'))))
            
        current_state = re_begin_state.match(blocks[0][0]).group(1)
        iterations = int(re_iterations.match(blocks[0][1]).group(1))
        
        for block in blocks[1:]:
            state = re_in_state.match(block[0]).group(1)
            val1, rule1 = parse_one_rule(block[1:5])
            val2, rule2 = parse_one_rule(block[5:])
    
            rules[state] = {
                val1: rule1,
                val2: rule2,
            }
    
    current_position = 0
    
    for _ in range(iterations):
        current_value = tape[current_position]
        rule = rules[current_state][current_value]
        
        tape[current_position] = rule.new_value
        current_position += rule.move_direction
        current_state = rule.next_state
    
    print('Part 1 solution:', sum(tape.values()))
    
if __name__ == '__main__':
    main()
