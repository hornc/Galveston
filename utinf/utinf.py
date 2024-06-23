import codecs
import re


INFCHR = re.compile(r'\\u[0-9a-fA-F]{5,}')
UCHR = re.compile(r'\\u([0-9a-fA-F]{4})')
REPL = '\ufffd'


def chrinf(i):
    if i > 0x110000:
        return strinf(r'\u' + hex(i)[2:])
    else:
        return strinf(chr(i))


def ordinf(c):
    return ord(c)


class strinf(str):
    def __len__(self):
        return len(self.__str__())

    def __str__(self):
        s = INFCHR.sub(REPL, self)
        for m in UCHR.findall(s):  # TODO: there is possibly a better way...
            s = s.replace(r'\u' + m, chr(int(m, 16)))
        return s

    def __repr__(self):
        s = ''.join([c for c in self])
        return s


class Codec(codecs.Codec):
    NAMES = ('utinf')

    @staticmethod
    def decode(data:str, errors='strict'):
        # takes str, returns Tuple, (bytes, length consumed)
        return (data.decode('utf8'), len(data))

    @staticmethod
    def encode(data, errors='strict'):
        # takes bytes, returns tuple of (bytes, length consumed)
        return (data.encode('utf8'), len(data))

    @staticmethod
    def search_function(encoding_name) -> codecs.CodecInfo:
        if (encoding_name in Codec.NAMES): # or ('∞' in encoding_name):  # ∞ is stripped before it gets here
            return codecs.CodecInfo(
                    #name='utinf',
                    name='UTF∞',  # this should probably be lowercase to be consistent
                    encode=Codec.encode,
                    decode=Codec.decode,
            )


codecs.register(Codec.search_function)
