from os import listdir
from os import path
import cProfile
import pstats
from bencodepy.decoder import decode


folder_path = '../torrent meta testing samples/'

file_data = []
file_sizes = []
for file_name in listdir(folder_path):
    file_sizes.append(path.getsize(folder_path + file_name))
    with open(folder_path + file_name, 'rb') as f:
        data = f.read()
        file_data.append(data)

file_data *= 1

num_of_files = len(file_data)
avg_size = sum(file_sizes) / 1024 / len(file_sizes)

print('Avg. file size: %.2f KB' % avg_size)
print('Number of files (in memory): %i' % num_of_files)
print('Total size processed: %.3f MB' % (avg_size * num_of_files / 1024))


def bench():
    results = [decode(d) for d in file_data]


cProfile.run('bench()', 'decode_stats')
p = pstats.Stats('decode_stats')
p.strip_dirs().sort_stats('tottime').print_stats()