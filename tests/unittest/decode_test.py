import unittest
from bencodepy.decoder import Decoder
from bencodepy.exceptions import DecodingError
from collections import OrderedDict


class DecodeTestCase(unittest.TestCase):

    def test__read(self):
        decoder = Decoder(b'abcdefg')
        decoder.idx = 1
        b = decoder._Decoder__read(3)
        self.assertEqual(b, b'bcd', msg='__read(i) failed to copy the correct bytes.')

    def test__read_exception(self):
        decoder = Decoder(b'abcdefg')
        decoder.idx = 1
        with self.assertRaises(DecodingError):
            decoder._Decoder__read(10)

    def test__read_to(self):
        decoder = Decoder(b'abc:def')
        decoder.idx = 0
        b = decoder._Decoder__read_to(b':')
        self.assertEqual(b, b'abc', msg='__read_to(b) failed to copy the correct bytes.')

    def test__read_to_exception(self):
        decoder = Decoder(b'a:bcdef')
        decoder.idx = 3
        with self.assertRaises(DecodingError):
            decoder._Decoder__read_to(b':')

    def test_parse_a_string(self):
        decoder = Decoder(b'ab3:cdefhijklmnop')
        decoder.idx = 2
        b = decoder._Decoder__parse()
        self.assertIsInstance(b, bytes, msg='Bencode string returned wrong type.')
        self.assertEqual(b, b'cde', msg='Failed to decode bencode string.')

    def test_parse_escaped_byte_string(self):
        decoder = Decoder(b'ab3:\x01\x01\x01f')
        decoder.idx = 2
        b = decoder._Decoder__parse()
        print(b)
        self.assertIsInstance(b, bytes, msg='Bencode string returned wrong type.')
        self.assertEqual(b, b'\x01\x01\x01', msg='Failed to decode bencode escaped byte string.')

    def test_parse_a_integer(self):
        decoder = Decoder(b'abi42eefhijklmnop')
        decoder.idx = 2
        b = decoder._Decoder__parse()
        self.assertIsInstance(b, int, msg='Bencode integer returned wrong type.')
        self.assertEqual(b, 42, msg='Failed to decode bencode integer.')

    def test_parse_a_dictionary(self):
        decoder = Decoder(b'abd1:A1:Beghijklmn')
        decoder.idx = 2
        b = decoder._Decoder__parse()
        self.assertIsInstance(b, dict, msg='Bencode dictionary returned wrong type.')
        self.assertEqual(b, {b'A': b'B'}, msg='Failed to decode bencode dictionary.')

    def test_parse_a_list(self):
        decoder = Decoder(b'abl1:A1:Becdefghijklmn')
        decoder.idx = 2
        b = decoder._Decoder__parse()
        self.assertIsInstance(b, list, msg='Bencode list returned wrong type.')
        self.assertEqual(b, [b'A', b'B'], msg='Failed to decode bencode list.')

    def test__parse_eof_exception(self):
        decoder = Decoder(b'abc')
        decoder.idx = 3
        with self.assertRaises(DecodingError):
            decoder._Decoder__parse()

    def test__parse_invalid_character_exception(self):
        decoder = Decoder(b'abc')
        decoder.idx = 0
        with self.assertRaises(DecodingError):
            decoder._Decoder__parse()

    def test_decode_tuple_case(self):
        decoder = Decoder(b'1:A1:B')
        b = decoder.decode()
        self.assertIsInstance(b, tuple, msg="Decode return wrong type for elements without root collection.")
        self.assertEqual(b, (b'A', b'B'), msg='Decode failed for special case of tuple return type.')

    def test_nested_complex(self):
        expected_result = OrderedDict()
        expected_result[b'KeyA'] = b'Value'
        expected_result[b'KeyB'] = [b'item1', b'item2']
        expected_result[b'KeyC'] = 42
        decoder = Decoder(b'd4:KeyA5:Value4:KeyBl5:item15:item2e4:KeyCi42ee')
        b = decoder._Decoder__parse()
        self.assertIsInstance(b, OrderedDict, msg='Incorrect type.')
        self.assertIsInstance(b[b'KeyA'], bytes, msg='Incorrect type.')
        self.assertIsInstance(b[b'KeyB'], list, msg='Incorrect type.')
        self.assertIsInstance(b[b'KeyC'], int, msg='Incorrect type.')
        self.assertDictEqual(b, expected_result, msg='Failed to decode bencode complex type. ')
