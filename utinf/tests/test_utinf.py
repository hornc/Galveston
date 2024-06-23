import utinf
from utinf import chrinf, strinf
import codecs
import pytest


def test_registered():
    name = 'utinf'
    info = codecs.lookup(name)
    print(info)
    assert info
    print('NAME:', info.name)
    assert info.name == 'UTF∞'


def test_undefined_search():
    # a bad search_function might always return an encoding result
    # regardless of the encoding_name
    # test we haven't created a catch-all
    with pytest.raises(LookupError):
        info = codecs.lookup('not_a_real_encoding')


def test_infinity_symbol_match():
    # because this is silly, check we do match
    # on any string containing an infinity symbol:
    #info = codecs.lookup('not_a_real_encoding_but_its_got_∞')  # fails
    info = codecs.lookup('ut∞')
    assert info.name == 'UTF∞'
    info = codecs.lookup('utf∞')
    assert info.name == 'utf-8'  # this is not what we want, but it's what we get.
    info = codecs.lookup('utinf∞')
    #info = codecs.lookup('utf∞') #  this matches utf-8
    assert info.name == 'UTF∞'
    # The ∞ symbol is stripped before it gets to our search function.
    # some strings still match anyway, even though our fn does not have an 
    # explict matcher... not really sure of the mechanism. 🤷
    # It appears to be some sort of default+sensilbe fuzzy string match helper magic.
    # RESULT: The ∞ can't be used as the main identifier anyway.


def test_basic_encode():
    b = 'hello'.encode('utinf')
    print(b)
    assert isinstance(b, bytes)


unicode = [
   'hello',
   'This is a test!!!',
   'BLAH\u0350 BLAH',
   'τηισ ισ α ωερυ γοοδ τεστ οφ Θνιψοδε.',
   '😀 	😁 	😂 	😃 	😄 	😅 	😆 	😇 	😈',
]

@pytest.mark.parametrize('u', unicode)
def test_encode(u):
    # test that this codec generally behaves the same as utf-8
    print(u)
    assert u.encode('utf-8') == u.encode('utf∞')  # urgh, this resolves to utf-8
    assert u.encode('utf-8') == u.encode('ut∞')
    assert u.encode('utf-8') == u.encode('utinf')


class TestChr:
    @pytest.mark.xfail(reason='chr() arg not in range(0x110000)', strict=True)
    def test_chr(self):
        # https://docs.python.org/3/library/functions.html#chr
        # ValueError: chr() arg not in range(0x110000)
        c = chr(6000000)
        assert isinstance(c, str)
        assert len(c) == 1
        print(c)

    def test_chrinf(self):
        c = chrinf(6000000)
        assert isinstance(c, str)
        assert len(c) == 1
        print(c)
        d = chrinf(0x66FFFF)
        assert len(d) == 1
        assert c != d
        print(f'{c} != {d}')
        print(f'{repr(c)} != {repr(d)}')



def test_strinf():
    s = strinf(r'a\u123456789abcdefABCDEF\u0063')
    print(repr(s))
    assert len(s) == 3
    assert str(s) == 'a�c'
    print(s)


unicode_inf = [
   r'hello \u12345678 there',
   r'This is a test!!!',
   r'BLAH\ufffff34\u0350 BLAH',
   r'τηισ ισ α ωερυ γοοδ τεστ οφ Θνιψοδε.',
   r'😀 	😁 	😂 	😃 	😄 	😅 	😆 	😇 	😈',
]

@pytest.mark.parametrize('u', unicode_inf)
def test_encode_inf(u):
    # test that this codec generally behaves the same as utf-8
    print(strinf(u))
    assert u.encode('utf-8') == strinf(u).encode('utinf')


# TODO:
# len() tests
# ord() tests

