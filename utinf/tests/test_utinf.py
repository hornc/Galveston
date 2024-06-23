import utinf
from utinf import chrinf
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



def test_chr():
    # https://docs.python.org/3/library/functions.html#chr
    # ValueError: chr() arg not in range(0x110000)
    with pytest.raises(ValueError):
        c = chr(6000000)
        assert isinstance(c, str)
        assert len(c) == 1
        print(c)


def test_chrinf():
    c = chrinf(6000000)
    assert isinstance(c, str)
    assert len(c) == 1
    print(c)


# TODO:
# len() tests
# ord() tests
# chr() tests
