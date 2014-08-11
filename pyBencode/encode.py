from pyBencode import EncodingError

def encode(obj, encoding='utf-8', strict=True):
    coded_bytes = b''

    def __encode_str(s: str):
        """Converts the input string to bytes and passes it the __encode_byte_str function for encoding."""
        b = bytes(s, encoding)
        __encode_byte_str(b)

    def __encode_byte_str(b: bytes):
        """Ben-encodes string from bytes."""
        nonlocal coded_bytes
        length = len(b)
        coded_bytes += bytes(str(length), encoding) + b':'
        coded_bytes += b

    def __encode_int(i: int):
        """Ben-encodes integer from int."""
        nonlocal coded_bytes
        coded_bytes += b'i'
        coded_bytes += bytes(str(i), 'utf-8')
        coded_bytes += b'e'

    def __encode_tuple(t: tuple):
        """Converts the input tuple to lists and passes it the __encode_list function for encoding."""
        l = [i for i in t]
        __encode_list(l)

    def __encode_list(l: list):
        """Ben-encodes list from list."""
        nonlocal coded_bytes
        coded_bytes += b'l'
        for i in l:
            __select_encoder(i)
        coded_bytes += b'e'

    def __encode_dict(d: dict):
        """Ben-encodes dictionary from dict."""
        nonlocal coded_bytes
        coded_bytes += b'd'
        for k in d:
            __select_encoder(k)
            __select_encoder(d[k])
        coded_bytes += b'e'

    def __select_encoder(o: object):
        """Calls the appropriate function to encode the passed object (obj)."""
        if isinstance(o, dict):
            __encode_dict(o)
        elif isinstance(o, list):
            __encode_list(o)
        elif isinstance(o, tuple):
            __encode_tuple(o)
        elif isinstance(o, bytes):
            __encode_byte_str(o)
        elif isinstance(o, str):
            __encode_str(o)
        elif isinstance(o, int):
            __encode_int(o)
        else:
            if strict:
                nonlocal coded_bytes
                coded_bytes = b''
                raise EncodingError("Unable to encode object: " + o.__repr__())
            else:
                print("Unable to encode object: " + str(o))

    __select_encoder(obj)
    return coded_bytes
