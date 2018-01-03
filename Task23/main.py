from collections import defaultdict

_two_param_ops = {'set', 'sub', 'mul', 'jnz'}


class Program:
    def __init__(self):
        self._commands = []
    
    def load_commands(self, commands):
        for cmd in commands:
            cmd = cmd.strip()
            
            if not cmd:
                continue
            
            items = cmd.split()
            
            if items[0] in _two_param_ops:
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
        for _ in range(100000000):  # just in case
            try:
                op = program[self._registers['op_id']]
            except IndexError:
                return self._registers['mul']
            
            if op[0] == 'set':
                self._registers[op[1]] = self._get_val(op[2])
                
            elif op[0] == 'sub':
                self._registers[op[1]] -= self._get_val(op[2])
                
            elif op[0] == 'mul':
                self._registers['mul'] += 1
                self._registers[op[1]] *= self._get_val(op[2])
                
            elif op[0] == 'jnz':
                if self._get_val(op[1]) != 0:
                    self._registers['op_id'] += self._get_val(op[2]) - 1
            else:
                raise ValueError(f'Unexpected operation {op[1]}')
            
            self._registers['op_id'] += 1
        else:
            raise RuntimeError('Failed to stop properly')
    

def main():
    program = Program()
    
    with open('data.txt') as fd:
        program.load_commands(fd.read().split('\n'))
    
    cpu = CPU()
    freq = cpu.execute(program)
    print('Part 1 solution:', freq)
    
    h = 0
    
    for b in range(107900, 124901, 17):
        for d in range(2, b):
            if b % d == 0:
                h += 1
                break

    print('Part 2 solution:', h)
    
if __name__ == '__main__':
    main()
