#!/usr/bin/python

import sys

current_key = None
current_value = 0
key = None

for line in sys.stdin:
     
     line = line.strip()

     # 分隔一次
     key, value = line.split('\t', 1)

     # convert value (currently a string) to int


     if current_key == key and '2017' in key:
          try:
              value = int(value)
          except ValueError as err:
               continue
          current_value += value

     elif current_key == key and '2017' not in key:
          current_value = value

     else:
          if current_key:
               print('%s\t%s' % (current_key, current_value))
          current_value = value
          current_key = key

if current_key == key:
    print('%s\t%s' % (current_key, current_value))
