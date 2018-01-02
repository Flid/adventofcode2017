directions = {
    'up': [0, -1],
    'down': [0, 1],
    'left': [-1, 0],
    'right': [1, 0],
}

turn_left = {
    'up': 'left',
    'down': 'right',
    'left': 'down',
    'right': 'up',
}

turn_right = {v: k for k, v in turn_left.items()}

turn_back = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left',
}


def main(): 
    M = {}
    
    with open('data.txt') as fd:
        for y_abs, line in enumerate(fd):
            line = line.strip()
            
            if not line:
                continue
            
            n = len(line)
            
            for x_abs in range(n):
                if line[x_abs] == '.':
                    continue
                
                M[(x_abs - n // 2, y_abs - n // 2)] = 'I'
    
    M_backup = M.copy()
    direction = 'up'
    x = 0
    y = 0
    infections = 0
    
    for _ in range(10000):
        current_infected = (x, y) in M
        
        if current_infected:
            direction = turn_right[direction]
            del M[(x, y)]
        else:
            direction = turn_left[direction]
            M[(x, y)] = 'I'
            infections += 1
        
        x += directions[direction][0]
        y += directions[direction][1]
        
    print('Part 1 solution:', infections)
    
    # Part 2
    M = M_backup
    
    direction = 'up'
    x = 0
    y = 0
    infections = 0
    
    for _ in range(10000000):
        current_state = M.get((x, y))
        
        if current_state is None:
            direction = turn_left[direction]
            M[(x, y)] = 'W'
        elif current_state == 'W':
            infections += 1
            M[(x, y)] = 'I'
        elif current_state == 'I':
            direction = turn_right[direction]
            M[(x, y)] = 'F'
        elif current_state == 'F':
            direction = turn_back[direction]
            del M[(x, y)]
        else:
            raise RuntimeError
        
        
        x += directions[direction][0]
        y += directions[direction][1]
    
    print('Part 2 solution:', infections)

if __name__ == '__main__':
    main()
