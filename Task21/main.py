class Mattrix:
    def __init__(self, content):
        self.rows = []
        self._load_content(content)
    
    def _load_content(self, content):
        if isinstance(content, str):
            content = content.replace('.', '0').replace('#', '1')
            self.rows = list(map(
                list,
                content.split('/')
            ))
        elif isinstance(content, int):
            self.rows = [[None] * content for _ in range(content)]
        else:
            self.rows = content
    
    @property
    def size(self):
        return len(self.rows)
    
    @property
    def signature(self):
        return '/'.join(''.join(row) for row in self.rows)
    
    def __repr__(self):
        return f'M<{self.signature}>'
    
    def flip(self):
        """ Return a vertically flipped copy of the mattrix """
        return Mattrix(self.rows[::-1])
    
    def rotate(self):
        """ Return a 90 degrees rotated copy of the mattrix """
        return Mattrix(list(zip(*self.rows[::-1])))
    
    def split(self, size):
        """ 
        Split the mattrix into submatrixes. 
        | A B |
        | C D |
        Becomes [A, B, C, D], where every letter means a `size` x `size` mattrix
        """
        n = self.size // size
        
        output = []
        
        for y in range(n):
            for x in range(n):
                output.append(Mattrix([
                    row[x * size: x * size + size] 
                    for row in self.rows[y * size: y * size + size]
                ]))
        
        return output

    def insert(self, m, x, y):
        """
        Insert submattrix `m` into `self` at the specified position.
        """
        for i in range(m.size):
            self.rows[y + i][x: x + m.size] = m.rows[i]
    
    def count(self, char):
        return sum(
            sum(item == char for item in row)
            for row in self.rows
        )
        

def main():
    rules = {}  # signature to mattrix
    
    with open('data.txt') as fd:
        for line in fd:
            line = line.strip()
            
            if not line:
                continue
            
            from_str, to_str = line.split(' => ')
            
            m_to = Mattrix(to_str)
            m_original = Mattrix(from_str)
            
            m = m_original
            m_f = m.flip()
            
            for _ in range(4):
                rules[m_f.signature] = m_to
                rules[m.signature] = m_to
                
                m = m.rotate()
                m_f = m_f.rotate()
    
    m = Mattrix('.#./..#/###')
    
    for iteration in range(18):
        size = 2 if m.size % 2 == 0 else 3
        n = m.size // size
        new_m = Mattrix(m.size // size * (size + 1))
        sub_ms = m.split(size)
        
        for i, sub_m in enumerate(sub_ms):
            m_replace = rules.get(sub_m.signature)
            
            if not m_replace:
                raise Exception(f'Can\'t find a rule for {sub_m.signature}')
            
            new_m.insert(
                m_replace,
                x=(i % n) * (size + 1),
                y=(i // n) * (size + 1),
            )
        
        m = new_m
        
        if iteration == 4:
            print('Part 1 answer:', m.count('1'))
    
    print('Part 2 answer:', m.count('1'))


if __name__ == '__main__':
    main()
