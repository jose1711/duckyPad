#!/usr/bin/env python
"""
example character definition, note that only the first
10 lines are converted, width may not exceed 6 characters
character = '''

  oo
 o  o
  oo
'''

"""
character = '''
  o o
   o
  ooo
 o   o
 o
 o 
 o   o
  ooo
'''

output = ''
for line in character.splitlines()[1:]:
    bits = 0
    for pos, x in enumerate(line):
        if x != ' ':
            bits |= (x != '') << (5-pos)
    output += chr(bits + 48)

print(f'SMB {output[:10]}')
