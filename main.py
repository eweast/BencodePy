__author__ = 'eric.weast'

import collections


class Bencode():
    def __init__(self):
        self.__coded_byte_str = b''
        self.encoding = 'utf-8'

        self.encode_options = {
            str: self.__encode_str,
            bytes: self.__encode_byte_str,
            int: self.__encode_int,
            list: self.__encode_list,
            dict: self.__encode_dict
        }

    def encode(self, obj):
        self.__select_encoder(obj)
        return self.__coded_byte_str

    def __select_encoder(self, obj):
        """Calls the appropriate function to encode the passed object (obj)."""
        if isinstance(obj, str):
            self.__encode_str(obj)
        elif isinstance(obj, bytes):
            self.__encode_byte_str(obj)
        elif isinstance(obj, int):
            self.__encode_int(obj)
        elif isinstance(obj, dict):
            self.__encode_dict(obj)
        elif isinstance(obj, list):
            self.__encode_list(obj)
        else:
            print('Error, encoder not found.')

    def __encode_str(self, s: str):
        """Converts the input string to bytes and passes it the __encode_byte_str function for encoding."""
        b = bytes(s, self.encoding)
        self.__encode_byte_str(b)

    def __encode_byte_str(self, b: bytes):
        """Ben-encodes string from bytes."""
        length = len(b)
        self.__coded_byte_str += bytes(str(length), 'utf-8') + b':'
        self.__coded_byte_str += b

    def __encode_int(self, i: int):
        """Ben-encodes integer from int."""
        self.__coded_byte_str += b'i'
        self.__coded_byte_str += bytes(str(i), 'utf-8')
        self.__coded_byte_str += b'e'

    def __encode_list(self, l: list):
        """Ben-encodes list from list."""
        self.__coded_byte_str += b'l'
        for i in l:
            self.__select_encoder(i)
        self.__coded_byte_str += b'e'

    def __encode_dict(self, d: dict):
        """Ben-encodes dictionary from dict."""
        self.__coded_byte_str += b'd'
        for k in d:
            self.__select_encoder(k)
            self.__select_encoder(d[k])
        self.__coded_byte_str += b'e'


mydict = {'keyA': [142, '2ndListitemInA', {'innerKey2': 'innerValue2'} ], b'keyB': b'valueBstr'}
ben = Bencode()
bs = ben.encode(mydict)
print(bs)

