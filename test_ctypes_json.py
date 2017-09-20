# -*- coding: utf-8 -*-

from ctypes import Structure, c_bool, c_int, c_float, c_char,  c_char_p, c_wchar, c_wchar_p
import json

import pytest

from ctypes_json import CDataJSONEncoder


def test_bool():
    assert json.dumps(c_bool(True), cls=CDataJSONEncoder) == 'true'


def test_int():
    assert json.dumps(c_int(10), cls=CDataJSONEncoder) == '10'


def test_float():
    assert json.dumps(c_float(1.0), cls=CDataJSONEncoder) == '1.0'


def test_char():
    with pytest.raises(TypeError):
        _ = json.dumps(c_char(), cls=CDataJSONEncoder)


def test_char_p():
    assert json.dumps(c_char_p(), cls=CDataJSONEncoder) == 'null'


def test_wchar():
    assert json.dumps(c_wchar('A'), cls=CDataJSONEncoder) == '"A"'


def test_wchar_p():
    assert json.dumps(c_wchar_p('Hello, World!'), cls=CDataJSONEncoder) == '"Hello, World!"'
    assert json.dumps(c_wchar_p(), cls=CDataJSONEncoder) == 'null'


def test_array():
    assert json.dumps((c_int * 5)(), cls=CDataJSONEncoder) == '[0, 0, 0, 0, 0]'


def test_structure():
    class Data(Structure):
        _fields_ = [
            ('bool', c_bool),
            ('int', c_int),
            ('float', c_float),
            ('wchar', c_wchar),
            ('wchar_p', c_wchar_p),
            ('array', c_int * 5),
        ]

    data = Data()

    data.bool = True
    data.int = 10
    data.float = 1.0
    data.wchar = 'A'
    data.wchar_p = 'Hello, World!'
    data.array = (c_int * 5)()

    assert json.dumps(data, cls=CDataJSONEncoder) == json.dumps({
        'bool': True,
        'int': 10,
        'float': 1.0,
        'wchar': 'A',
        'wchar_p': 'Hello, World!',
        'array': [0] * 5,
    })
