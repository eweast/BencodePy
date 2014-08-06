__author__ = 'eric.weast'


class EncodingError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class BenEncoder():
    def __init__(self, encoding='utf-8', strict=True):
        self.coded_bytes = b''
        self.encoding = encoding
        self.strict = strict
        self.errors = 0

    def encode(self, obj):
        self.__reset()
        self.__select_encoder(obj)
        return self.coded_bytes

    def __reset(self):
        self.coded_bytes = b''
        self.errors = 0

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
            if self.strict:
                self.coded_bytes = b''
                raise EncodingError("Unable to encode object: " + obj.__repr__())
            else:
                print("Unable to encode object: " + str(obj))
                self.errors += 1

    def __encode_str(self, s: str):
        """Converts the input string to bytes and passes it the __encode_byte_str function for encoding."""
        b = bytes(s, self.encoding)
        self.__encode_byte_str(b)

    def __encode_byte_str(self, b: bytes):
        """Ben-encodes string from bytes."""
        length = len(b)
        self.coded_bytes += bytes(str(length), 'utf-8') + b':'
        self.coded_bytes += b

    def __encode_int(self, i: int):
        """Ben-encodes integer from int."""
        self.coded_bytes += b'i'
        self.coded_bytes += bytes(str(i), 'utf-8')
        self.coded_bytes += b'e'

    def __encode_list(self, l: list):
        """Ben-encodes list from list."""
        self.coded_bytes += b'l'
        for i in l:
            self.__select_encoder(i)
        self.coded_bytes += b'e'

    def __encode_dict(self, d: dict):
        """Ben-encodes dictionary from dict."""
        self.coded_bytes += b'd'
        for k in d:
            self.__select_encoder(k)
            self.__select_encoder(d[k])
        self.coded_bytes += b'e'


mydict = {'keyA': [142, '2ndListitemInA', {'innerKey2': 'innerValue2'} ], b'keyB': b'valueBstr'}
ben = BenEncoder()
bs = ben.encode(mydict)
print(bs)

