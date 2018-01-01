from string import ascii_uppercase


def main():
    with open('data.txt') as fd:
        lines = fd.read().split('\n')
    
    def can_go(x1, y1, expected_char):
        cell = lines[y1][x1]
        return cell == expected_char or cell in ascii_uppercase
    
    x = lines[0].index('|')
    y = 0
    direction = [0, 1]
    
    found_letters = []
    
    while True:
        x += direction[0]
        y += direction[1]
        
        if x == -1:
            break
        
        cell = lines[y][x]
        
        if cell in ascii_uppercase:
            found_letters.append(cell)
        
        if cell == '+':
            if direction[1]:  # moving vertically
                if x > 0 and can_go(x - 1, y, '-'):
                    direction = [-1, 0]
                else:
                    direction = [1, 0]
            else:  # moving horizontally
                if y > 0 and can_go(x, y - 1, '|'):
                    direction = [0, -1]
                else:
                    direction = [0, 1]
            
    print(''.join(found_letters))
        
    
if __name__ == '__main__':
    main()
