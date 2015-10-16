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


python_data *= 6000
print('Number of objects to decode: {0}.'.format(len(python_data)))

results = []


def bench():
    global results
    results = [encode(r) for r in python_data]


def print_size():
    global results
    s = 0
    for r in results:
        s += len(r)
    print('Total encode size: %.3f MB.' % (s/1024/1024))


def check_first_file():
    if file_data[0] == results[0]:
        print('Match')
    else:
        print('WARNING: Encoded and original data does not match.')

cProfile.run('bench()', 'encode_stats')
check_first_file()
print_size()
p = pstats.Stats('encode_stats')
p.strip_dirs().sort_stats('tottime').print_stats()




