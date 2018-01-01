from collections import defaultdict, deque

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
    def __init__(self, p_value, program: Program):
        self._registers = defaultdict(int)
        self._registers['p'] = p_value
        self._out_signal = None
        self._in_signals = deque()
        self._is_waiting = False
        self._program = program
    
    @property
    def is_blocked(self):
        return self._is_waiting and not self._in_signals
    
    def _get_val(self, val):
        try:
            return int(val)
        except ValueError:
            return self._registers[val]
        
    def send_signal(self, value):
        self._in_signals.append(value)
    
    def read_signal(self):
        """ Destructive reading the value """
        val = self._out_signal
        self._out_signal = None
        return val
    
    def read_register(self, name):
        return self._registers[name]
    
    def step(self):
        
        op = self._program[self._registers['op_id']]
        
        if op[0] == 'snd':
            self._registers['sends'] += 1
            self._out_signal = self._get_val(op[1])
            
        elif op[0] == 'set':
            self._registers[op[1]] = self._get_val(op[2])
            
        elif op[0] == 'add':
            self._registers[op[1]] += self._get_val(op[2])
            
        elif op[0] == 'mul':
            self._registers[op[1]] *= self._get_val(op[2])
            
        elif op[0] == 'mod':
            self._registers[op[1]] %= self._get_val(op[2])
        
        elif op[0] == 'rcv':
            if self._in_signals:
                self._is_waiting = False
                self._registers[op[1]] = self._in_signals.popleft()
            else:
                self._is_waiting = True
                return  # without increasing command register
            
        elif op[0] == 'jgz':
            if self._get_val(op[1]) > 0:
                self._registers['op_id'] += self._get_val(op[2]) - 1
        else:
            raise ValueError(f'Unexpected operation {op[1]}')
        
        self._registers['op_id'] += 1
    

def _try_transfer_signal(cpu_from, cpu_to):
    signal = cpu_from.read_signal()
    
    if signal is None:
        return

    cpu_to.send_signal(signal)


def main():
    program = Program()
    
    with open('data_part2.txt') as fd:
        program.load_commands(fd.read().split('\n'))

    cpu0 = CPU(0, program)
    cpu1 = CPU(1, program)
    
    for _ in range(100000):  # Just in case
        cpu0.step()
        cpu1.step()
        
        _try_transfer_signal(cpu0, cpu1)
        _try_transfer_signal(cpu1, cpu0)
        
        if cpu0.is_blocked and cpu1.is_blocked:
            break
    else:
        raise RuntimeError('Failed to find a solution')
        
        
    print('Part 2 solution:', cpu1.read_register('sends'))
    
if __name__ == '__main__':
    main() 
