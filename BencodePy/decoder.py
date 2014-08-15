import collections

from .exceptions import DecodingError


class Decoder:

    def __init__(self, data: bytes):
        self.data = data
        self.idx = 0

    def __read(self, i) -> bytes:
        b = self.data[self.idx: self.idx + i]
        self.idx += i
        return b

    def __read_to(self, terminator) -> bytes:
        i = self.data.index(terminator, self.idx)
        b = self.data[self.idx:i]
        self.idx = i + 1
        return b

    def __parse(self):
        char = self.data[self.idx: self.idx + 1]
        if char in [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0']:
            str_len = int(self.__read_to(b':'))
            return self.__read(str_len)
        elif char == b'i':
            self.idx += 1
            return int(self.__read_to(b'e'))
        elif char == b'd':
            return self.__parse_dict()
        elif char == b'l':
            return self.__parse_list()
        else:
            raise DecodingError('Invalid token character (' + str(char) + ') at position ' + str(self.idx) + '.')

    def decode(self) -> collections.OrderedDict:
        return self.__parse()

    def __parse_dict(self) -> collections.OrderedDict:
        self.idx += 1
        d = collections.OrderedDict()
        key_name = None
        while self.data[self.idx: self.idx + 1] != b'e':
            if key_name is None:
                key_name = self.__parse()
            else:
                d[key_name] = self.__parse()
                key_name = None
        self.idx += 1
        return d

    def __parse_list(self) -> list:
        self.idx += 1
        l = []
        while self.data[self.idx: self.idx + 1] != b'e':
            l.append(self.__parse())
        self.idx += 1
        return l


def decode_from_file(path: str):
    with open(path, 'rb') as f:
        b = f.read()
    decoder = Decoder(b)
    return decoder.decode()


def decode(data: bytes):
    decoder = Decoder(data)
    return decoder.decode()
