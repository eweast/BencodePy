from os import listdir
import cProfile
import pstats
from bencodepy.decoder import decode
from bencodepy.encode import encode


folder_path = '../torrent meta testing samples/'

file_data = []
for file_name in listdir(folder_path):
    with open(folder_path + file_name, 'rb') as f:
        data = f.read()
        file_data.append(data)

python_data = [decode(d) for d in file_data]

for i, obj in enumerate(python_data):
    print('Sample data {0}: {1} .'.format(i, obj))


python_data *= 1650
print('Number of objects to decode: {0}.'.format(len(python_data)))


def bench():
    results = [encode(r) for r in python_data]

cProfile.run('bench()', 'encode_stats')
p = pstats.Stats('encode_stats')
p.strip_dirs().sort_stats('tottime').print_stats()