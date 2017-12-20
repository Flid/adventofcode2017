"""
Read from input file, generate SQL to solve the task
"""

print('''CREATE TABLE public.layers
(
  id int NOT NULL,
  width int NOT NULL,
  PRIMARY KEY (id)
); 
''')


input_data = []

with open('data.txt') as fd:
    for line in fd:
        layer_id, width = line.strip().split(': ')
        input_data.append(f'({layer_id}, {width})')
    
input_data_sql = ', '.join(input_data)
print(
    f'INSERT INTO public.layers (id, width) VALUES {input_data_sql};' 
    
)

print('''
SELECT SUM(CASE 
    WHEN id % ((width-1)*2) = 0 
    THEN id*width 
    ELSE 0 
END) from layers;
''')

print('Drop all the text above into an SQL shell and execute to get the asnwer.')
