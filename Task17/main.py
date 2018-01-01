import pyximport; pyximport.install()
import worker

input_value = 344

print('Part 1 solution')
print(worker.calculate_part1(input_value, 2017))

print('Part 2 solution')
print(worker.calculate_part2(input_value, 50000000))
