#BencodePy
A small Python 3 library for encoding and decoding Bencode data licensed under the GPLv2.

##Overview
Although Bencoding is mainly, if not exclusively, used for BitTorrent metadata (.torrent) files, this library seeks to
provide a generic means of encoding/decoding Bencode from/to Python data structures independent of torrent files.


##Quickstart

### Installation
`pip install bencodepy`

### Encode
```python
from bencodepy.encode import encode

mydata = { 'keyA': 'valueA' } #example data

bencoded_data = encode(mydata)
```

### Decode

From bytes...
```python
from bencodepy.decode import decode

mydata = b'd4:KeyA6:valueAe'

my_ordred_dict = decode(mydata)
 
```

Alternatively from a file...
```python
from bencodepy.decode import decode_from_file

my_file_path = 'c:\whatever'

my_ordred_dict = decode_from_file(my_file_path)
```

##Encoding
Mappings: 

Python Type*  | Bencode Type
------------- | -------------
dict  | Dictionary
list  | List
tuple  | List
int  | Integer
str  | String
bytes  | String

*Includes subtypes thus both dict and OrderedDict would be represented as Bencode dictionary.


##Decoding
Mapping:

Bencode Type | Python Type
------------- | -------------
Dictionary  | OrderedDict
List  | list
Integer  | int
String  | bytes

Bencode dictionaries are decoded as Python OrderedDict to preserve the order of elements. This is necessary to correctly
calculate certain hash values such as that of a torrent file's Info Dictionary.

The `decode()` method will always return an iterable. If the root element of the bencode data is not a dictionary or 
list, `decode()` will wrap the all bencode elements in a tuple. Thus input data of `b'5:ItemA5:ItemB'` would yield
a python tuple of `('ItemA', 'ItemB')`.
  

##TODO
1. Decode is currently limited to Bencoded data that start with a root dictionary (`b'd...'`).
2. Unit tests for decoder.
3. Benchmarks for encoding.

##License
Copyright © 2014 by Eric Weast

Licensed under the [GPLv2](https://www.gnu.org/licenses/gpl-2.0.html "gnu.org")