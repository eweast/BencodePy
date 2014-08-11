#BencodePy
A small Python 3 library for encoding and decoding Bencode data licensed under the GPLv2.

##Overview
Although Bencoding is mainly, if not exclusively, used for BitTorrent metadata (.torrent) files, this library seeks to
provide a generic means of transforming Bencode from/to Python data structures independent of torrent files.


##Quickstart

### Installation
`pip install bencodepy`

### Encode
todo

### Decode
todo

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


##License
Copyright © 2014 by Eric Weast

Licensed under the [GPLv2](https://www.gnu.org/licenses/gpl-2.0.html "gnu.org")

