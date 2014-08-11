
import unittest
import bencodepy.encode
import bencodepy.exceptions
import collections


class EncodeTestCase(unittest.TestCase):

    def test_exception_when_strict(self):
        invalid_obj = None
        with self.assertRaises(bencodepy.exceptions.EncodingError):
            bencodepy.encode(invalid_obj, strict=True)

    def test_no_exception_when_not_strict(self):
        invalid_obj = None
        bencodepy.encode(invalid_obj, strict=False)
        self.assert_(True)

    def test_encode_str(self):
        coded = bencodepy.encode('ThisIsAString')
        self.assertEqual(coded, b'13:ThisIsAString', msg='Failed to encode string from str.')

    def test_encode_int(self):
        coded = bencodepy.encode(42)
        self.assertEqual(coded, b'i42e', msg='Failed to encode integer from int.')

    def test_encode_bytes(self):
        pass
        b = b"TheseAreSomeBytes"
        coded = bencodepy.encode(b)
        l = bytes(str(len(b)), 'utf-8')
        self.assertEqual(coded, l + b':' + b, msg='Failed to encode string from bytes.')

    def test_encode_list(self):
        l = ['a', 'b', 3]
        coded = bencodepy.encode(l)
        self.assertEqual(coded, b'l1:a1:bi3ee', msg='Failed to encode list from list.')

    def test_encode_tuple(self):
        t = ('a', 'b', 3)
        coded = bencodepy.encode(t)
        self.assertEqual(coded, b'l1:a1:bi3ee', msg='Failed to encode list from tuple.')

    def test_encode_dict(self):
        od = collections.OrderedDict()
        od['ka'] = 'va'
        od['kb'] = 2
        coded = bencodepy.encode(od)
        self.assertEqual(coded, b'd2:ka2:va2:kbi2ee', msg='Failed to encode dictionary from dict.')

    def test_encode_complex(self):
        od = collections.OrderedDict()
        od['KeyA'] = ['listitemA', {'k': 'v'}, 3]
        od['KeyB'] = {'k': 'v'}
        od['KeyC'] = 3
        od['KeyD'] = 'AString'
        expected_result = b'd4:KeyAl9:listitemAd1:k1:vei3ee4:KeyBd1:k1:ve4:KeyCi3e4:KeyD7:AStringe'
        coded = bencodepy.encode(od)
        self.assertEqual(coded, expected_result, msg='Failed to encode complex object.')
        pass

if __name__ == '__main__':
    unittest.main()
