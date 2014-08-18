cimport cython

cdef class Decoder:
    cdef public bytes data
    cdef public int idx

    @cython.locals(b = bytes)
    cpdef bytes __read(self, int i)

    @cython.locals(b = bytes, i = int)
    cpdef bytes __read_to(self, bytes terminator)

    @cython.locals(char = bytes, str_len = int)
    cpdef object __parse(self)

    cpdef object decode(self)

    @cython.locals(l = list, length = int)
    cpdef tuple __wrap_with_tuple(self)

    @cython.locals(key_name = bytes)
    cpdef object __parse_dict(self)

    @cython.locals(l = list)
    cpdef list __parse_list(self)


cpdef object decode_from_file(str path)

@cython.locals(d = Decoder)
cpdef object decode(bytes data)