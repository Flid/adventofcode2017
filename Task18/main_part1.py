from collections import defaultdict

_one_param_ops = {'snd', 'rcv'}
_two_param_ops = {'set', 'add', 'mul', 'mod', 'jgz'}


class Program:
    def __init__(self):
        self._commands = []
    
    def load_commands(self, commands):
        for cmd in commands:
            cmd = cmd.strip()
            
            if not cmd:
                continue
            
            items = cmd.split()
            
            if items[0] in _one_param_ops:
                op, param = items
                self._commands.append((op, param))
                
            elif items[0] in _two_param_ops:
                op, param1, param2 = items
                self._commands.append((op, param1, param2))
            else:
                raise ValueError('Wrong input')
    
    def __getitem__(self, ind):
        return self._commands[ind]

            
class CPU:
    def __init__(self):
        self._registers = defaultdict(int)
    
    def _get_val(self, val):
        try:
            return int(val)
        except ValueError:
            return self._registers[val]
    
    def execute(self, program: Program):
        while True:
            op = program[self._registers['op_id']]
            
            if op[0] == 'snd':
                self._registers['snd'] = self._get_val(op[1])
                
            elif op[0] == 'set':
                self._registers[op[1]] = self._get_val(op[2])
                
            elif op[0] == 'add':
                self._registers[op[1]] += self._get_val(op[2])
                
            elif op[0] == 'mul':
                self._registers[op[1]] *= self._get_val(op[2])
                
            elif op[0] == 'mod':
                self._registers[op[1]] %= self._get_val(op[2])
            
            elif op[0] == 'rcv':
                if self._registers['snd'] != 0:
                    return self._registers['snd']
                
            elif op[0] == 'jgz':
                if self._get_val(op[1]) > 0:
                    self._registers['op_id'] += self._get_val(op[2]) - 1
            else:
                raise ValueError(f'Unexpected operation {op[1]}')
            
            self._registers['op_id'] += 1
    

def main():
    program = Program()
    
    with open('data_part1.txt') as fd:
        program.load_commands(fd.read().split('\n'))

    cpu = CPU()
    freq = cpu.execute(program)
    print('Part 1 solution:', freq)
    
if __name__ == '__main__':
    main()
