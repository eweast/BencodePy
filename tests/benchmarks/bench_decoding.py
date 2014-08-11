
from os import listdir
import BencodePy.decoder
import cProfile
import pstats


folder_path = 'tests/torrent meta testing samples/'

file_data = []
file_sizes = []
for file_name in listdir(folder_path):
    file_sizes.append()
    with open(folder_path + file_name, 'rb') as f:
        data = f.read()
        file_data.append(data)

##os.path.getsize('C:\\Python27\\Lib\\genericpath.py')


file_data *= 200

print('Avg. torrent size: ' + str())
print('Number of torrents: ' + str(len(file_data)))


def bench():
    for d in file_data:
        BencodePy.decoder.decode(d)

cProfile.run('bench()', 'stats')
p = pstats.Stats('stats')
p.strip_dirs().sort_stats('tottime').print_stats()