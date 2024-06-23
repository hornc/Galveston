import codecs


def chrinf(i):
    if i > 0x110000:
        return '\ufffd'
    else:
        return chr(i)


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
