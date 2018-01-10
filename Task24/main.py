from collections import namedtuple

Component = namedtuple('Component', 'a b index')

def main():
    all_components = set()
    
    with open('data.txt') as fd:
        for i, line in enumerate(fd):
            line = line.strip()
            
            if not line:
                continue
            
            v1, v2 = map(int, line.split('/'))
            
            c = Component(v1, v2, i)
            all_components.add(c)
    
    # Caching makes it ~twice faster
    _CACHE = {}
    
    def _solve(start_val, components_left, weight_score=True):
        """
        We basically need to find the longest path in a graph, which has cycles.
        It's the NP-hard problem, so we'll go for a straight-forward simple solution.
        
        We know the value to start the sub-bridge with (start_val).
        We try every component available, and if it matches - solve sub-problem without this item.
        """
        key = (start_val, tuple(sorted(c.index for c in components_left)))
        
        if key in _CACHE:
            return _CACHE[key]
        
        max_score = 0
        max_components = tuple()
        
        for component in components_left:
            if component.a == start_val:
                new_start_val = component.b
            elif component.b == start_val:
                new_start_val = component.a
            else:
                continue
    
            sub_score, sub_max_components = _solve(
                new_start_val, 
                components_left - set([component]), 
                weight_score=weight_score,
            )
            
            if weight_score:
                sub_score += component.a + component.b
            else:
                sub_score += 1
            
            if sub_score > max_score:
                max_score = sub_score
                max_components = tuple([component]) + sub_max_components
        
        _CACHE[key] = (max_score, max_components)
        return max_score, max_components
    
    _, components = _solve(0, all_components, weight_score=True)
    print('Part 1 solution:', sum(c.a + c.b for c in components))
    
    _CACHE.clear()
    _, components = _solve(0, all_components, weight_score=False)
    print('Part 2 solution:', sum(c.a + c.b for c in components))
    
    
if __name__ == '__main__':
    main()
