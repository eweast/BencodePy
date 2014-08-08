__author__ = 'eric.weast'

from os import listdir
import pyBencode.decoder

import datetime

folder_path = 'tests/tor samples/'

file_data = []
for file_name in listdir(folder_path):
    with open(folder_path + file_name, 'rb') as f:
        data = f.read()
        file_data.append(data)

i = 0
t1 = datetime.datetime.now()
for d in file_data:
    pyBencode.decoder.decode(d)
    i+=1
t2 = datetime.datetime.now()

print(str(i))
print(str(t2 -t1))