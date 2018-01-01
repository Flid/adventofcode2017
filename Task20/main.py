import re
from collections import namedtuple


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


def main():
    particles = []
    
    with open('data.txt') as fd:
        for i, line in enumerate(fd):
            res = re_particle.match(line.strip())
            values = list(map(int, res.groups()))
            values.append(i)
            particles.append(Particle(*values))


    # We don't really care about particle initial speed or position, just get the one with the lowest acceleration.
    # If two particles have the same acceleration - the one with lowest initial speed wins.
    # Same for initial position.
    particles.sort(
        key=lambda p: [abs_sum(p.ax, p.ay, p.az), abs_sum(p.vx, p.vy, p.vz), abs_sum(p.px, p.py, p.pz)],
    )
    
    print('Target particle index:', particles[0].ind)

if __name__ == '__main__':
    main()
