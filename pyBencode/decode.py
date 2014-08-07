__author__ = 'eric.weast'

from pyBencode.errors import DecodingError
import collections


def decode(data: bytes):

    decoded_dict = collections.OrderedDict()
    active_targets = list()
    current_dict_key = None

    def set_new_target(obj):
        nonlocal active_targets
        active_targets.append(obj)

    def append_value_to_list(value):
        active_targets[-1].append(value)

    def assgn_value_to_dict(value):
        nonlocal current_dict_key
        if current_dict_key:
            active_targets[-1][current_dict_key] = value
            current_dict_key = None
        else:
            current_dict_key = value

    def add_value(value):
        nonlocal active_targets
        if active_targets[-1] is collections.OrderedDict:
            assgn_value_to_dict(value)
        elif active_targets[-1] is list:
            append_value_to_list(value)
        else:
            raise DecodingError('Unable to assign value to existing internal dictionary or list.')

    def parse_dict():
        nonlocal decoded_dict
        nonlocal current_dict_key
        nonlocal idx

        active_target = active_targets[-1] if active_targets else None

        if not active_target:
            active_targets.append(decoded_dict)
        elif active_target is collections.OrderedDict:
            if current_dict_key:
                key_name = current_dict_key
            else:
                raise DecodingError('Invalid dictionary key at index ' + str(idx) + '.')
            active_target[key_name] = collections.OrderedDict()
            set_new_target(active_target[key_name])
            current_dict_key = None
        elif active_target is list:
            d = collections.OrderedDict()
            active_target.append(d)
            set_new_target(d)

    def parse_list():
        nonlocal decoded_dict
        nonlocal current_dict_key
        nonlocal idx

        if current_dict_key[-1] is collections.OrderedDict():
            if current_dict_key:
                key_name = current_dict_key
            else:
                raise DecodingError('Invalid dictionary key at index ' + str(idx) + '.')
            ct = get_current_target()
            ct[key_name] = list()
            set_new_target(ct)
            current_dict_key = None
        elif get_current_target is list:
            set_new_target(list())

    def parse_str():
        nonlocal idx
        nonlocal data
        i = 1
        while b':' not in data[idx + i:idx+i+1]:
            i += 1
        string_length = int(data[idx + i - 1])
        string = data[idx + i + 1:idx + i + 1 + string_length]
        add_value(string)

    length = len(data)
    idx = 0
    while idx < length:
        token = data[idx:idx+1]

        if token == b'd':
            parse_dict()
        elif token == b'l':
            parse_list()
        elif token == b'i':
            pass
        elif token == b'e':
            pass
        elif token.decode('utf-8', errors='ignore').isdigit():
            pass
        else:
            raise DecodingError('Invalid character token at index ' + str(idx) + '.')

        idx += 1


def decode_from_file(path: str):
    b = open(path, 'rb').read()
    print(b)
    decode(b)


if __name__ == '__main__':
    tor_path = "../tests/TorB.torrent"
    decode_from_file(tor_path)