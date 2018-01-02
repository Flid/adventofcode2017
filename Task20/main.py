import re
from collections import namedtuple
import math


Particle = namedtuple(
    'Particle',
    'px py pz vx vy vz ax ay az ind'
)

re_particle = re.compile(
    r'p=<(\-?\d+),(\-?\d+),(\-?\d+)>, '
    r'v=<(\-?\d+),(\-?\d+),(\-?\d+)>, '
    r'a=<(\-?\d+),(\-?\d+),(\-?\d+)>'
)

def abs_sum(*args):
    return sum(abs(item) for item in args)


ANY_TIME = object()


def _collision_one_coord(a0, v0, p0, a1, v1, p1):
    """
    Find all integer non-negative ticks, when particles 
    meet along one coordinate.
    """
    # Special cases
    if a0 == a1:
        if v0 == v1:
            if p0 == p1:
                return ANY_TIME
            
            return []
        
        t = (p0 - p1) / (v1 - v0)
        if t >= 0 and int(t) == t:
            return [t]
        else:
            return []
    
    # General case
    # Let's solve a quadratic equation
    # Particle position is described by this formula:
    # p(t) = p0 + t*(v0 + a/2) + 0.5*a*t**2 
    # We solve p0(t) - p1(t) = 0
    d_sq = (v0 + a0/2.0 - v1 - a1/2.0) ** 2 - 2 * (a0 - a1) * (p0 - p1)
    
    if d_sq < 0:
        return []
    
    d = math.sqrt(d_sq)
    
    solutions = []
    
    t1 = (-v0 - a0/2.0 + v1 + a1/2.0 + d) / (a0 - a1)
    t2 = (-v0 - a0/2.0 + v1 + a1/2.0 - d) / (a0 - a1)
    
    if t1 >= 0 and int(t1) == t1:
        solutions.append(t1)
    
    if t2 >= 0 and int(t2) == t2:
        solutions.append(t2)
    
    return solutions


def calculate_collision(p1: Particle, p2: Particle):
    """
    Given two particles, calculate number of ticks before they collide for the first time.
    None if they never collide.
    """
    # First find all the tick numbers, when one coordinate matches
    solutions = []
    solutions.append(
        _collision_one_coord(p1.ax, p1.vx, p1.px, p2.ax, p2.vx, p2.px)
    )
    solutions.append(
        _collision_one_coord(p1.ay, p1.vy, p1.py, p2.ay, p2.vy, p2.py)
    )
    solutions.append(
        _collision_one_coord(p1.az, p1.vz, p1.pz, p2.az, p2.vz, p2.pz)
    )
    
    if not all(solutions):
        return None
    
    # We need to intersect tick numbers for all coordinates.
    # If one coordinate is `ANY_TIME` - we don't care about it.
    solutions = [item for item in solutions if item != ANY_TIME]
    
    if not solutions:
        # All coordinates ever match
        return 0
    
    intersection = set(solutions[0])
    
    for i in range(1, len(solutions)):
        intersection &= set(solutions[i])
    
    if not intersection:
        return None
    
    return int(min(intersection))


def main():
    particles = []
    
    with open('data.txt') as fd:
        for i, line in enumerate(fd):
            res = re_particle.match(line.strip())
            values = list(map(int, res.groups()))
            values.append(i)
            particles.append(Particle(*values))


    # Part 1:
    # We don't really care about particle initial speed or position, just get the one with the lowest acceleration.
    # If two particles have the same acceleration - the one with lowest initial speed wins.
    # Same for initial position.
    particles.sort(
        key=lambda p: [abs_sum(p.ax, p.ay, p.az), abs_sum(p.vx, p.vy, p.vz), abs_sum(p.px, p.py, p.pz)],
    )
    
    print('Part 1 answer:', particles[0].ind)
    
    # Find all the collisions between every point pair.
    collisions = []  # (first_collition_tick, index1, index2)
    
    for i, particle in enumerate(particles):
        for j in range(i+1, len(particles)):
            first_collision = calculate_collision(particle, particles[j])
            
            if first_collision is None:
                continue
        
            collisions.append((first_collision, i, j))
    
    collisions.sort()
    
    # Run through collisions, keep a list of terminated particles - they can only collide once!
    terimated_particle_ids = {}
    
    def teminated_before(ind, t):
        """
        If collision is already registered, but at the current tick - 
        the particle is not teriminated yet.
        """
        val = terimated_particle_ids.get(ind)
        return val is not None and val != t
    
    for t, ind1, ind2 in collisions:
        if teminated_before(ind1, t) or teminated_before(ind2, t):
            # one of the particles is already terminated, preventing this collision
            continue
        
        terimated_particle_ids[ind1] = t
        terimated_particle_ids[ind2] = t
    
    print('Part 2 solution:', len(particles) - len(terimated_particle_ids))


if __name__ == '__main__':
    main()
