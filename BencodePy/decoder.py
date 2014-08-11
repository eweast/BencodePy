import collections

from .exceptions import DecodingError


class Decoder:
    def __init__(self, data):

        self.view = memoryview(data)
        self.length = len(data)
        self.idx = 0

        self.frame = bytearray()

        self.decoded_dict = collections.OrderedDict()
        self.active_targets = list()
        self.current_key = None

    def __read(self, i):
        v = self.view[self.idx: self.idx + i]
        self.idx += i
        if self.idx > self.length:
            raise DecodingError('Unexpected EOF.')
        return v

    @property
    def __current_target(self):
        return self.active_targets[-1]

    def __new_target(self, obj):
        self.active_targets.append(obj)

    def decode(self) -> collections.OrderedDict:
        while self.idx < self.length:
            char = self.__read(1)
            if char in [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0']:
                self.__parse_str(char)
            elif char == b'i':
                self.__parse_int()
            elif char == b'd':
                self.__parse_dict()
            elif char == b'l':
                self.__parse_list()
            elif char == b'e':
                self.__parse_terminator()
            else:
                raise DecodingError('Invalid token character at position ' + str(self.idx) + '.')
        return self.decoded_dict

    def __parse_dict(self):
        if not self.active_targets:
            self.active_targets.append(self.decoded_dict)
        elif isinstance(self.__current_target, dict):
            if self.current_key:
                key_name = self.current_key
            else:
                raise DecodingError('Internal error at __parse_dict(self) for token at index ' + str(self.idx) + '.')
            self.__current_target[key_name] = collections.OrderedDict()
            self.__new_target(self.__current_target[key_name])
            self.current_key = None
        elif isinstance(self.__current_target, list):
            d = collections.OrderedDict()
            self.__current_target.append(d)
            self.__new_target(d)
        else:
            raise DecodingError('Internal error at __parse_dict(self) for token at index ' + str(self.idx) + '.')

    def __parse_list(self):
        if isinstance(self.__current_target, dict):
            if self.current_key:
                key_name = self.current_key
            else:
                raise DecodingError('Invalid dictionary key name at index ' + str(self.idx) + '.')
            self.__current_target[key_name] = list()
            self.__new_target(self.__current_target[key_name])
            self.current_key = None
        elif isinstance(self.__current_target, list):
            self.__new_target(list())
        else:
            raise DecodingError('Internal error at __parse_list(self) for token at index ' + str(self.idx) + '.')

    def __parse_terminator(self):
        try:
            self.active_targets.pop()
        except IndexError:
            raise DecodingError('Invalid terminator token ("e") at index ' + str(self.idx) + '.')

    def __parse_str(self, char):
        self.frame.extend(char)
        while True:
            v = self.__read(1)
            if v != b':':
                self.frame.extend(v)
            else:
                break
        string = self.__read(int(self.frame))
        self.__add_data(string)
        self.frame.clear()

    def __parse_int(self):
        while True:
            v = self.__read(1)
            if v != b'e':
                self.frame.extend(v)
            else:
                break
        self.__add_data(int(self.frame))
        self.frame.clear()

    def __add_data(self, val):
        if isinstance(self.__current_target, dict):
            self.__append_dict(val)
        elif isinstance(self.__current_target, list):
            self.__append_list(val)

    def __append_list(self, data):
        self.__current_target.append(data)

    def __append_dict(self, value):
        if self.current_key:
            self.__current_target[self.current_key] = value
            self.current_key = None
        else:
            self.current_key = value


def decode_from_file(path: str):
    with open('path', 'rb') as f:
        b = f.read()
    decoder = Decoder(b)
    return decoder.decode()


def decode(data: bytes):
    decoder = Decoder(data)
    return decoder.decode()
