# ctypes_json.py

`ctypes_json.py` converts Structure or Union in ctypes to JSON.

## Requirements

No dependencies.

## Usage

```python
import json
from ctypes import Structure, c_int
from ctypes_json import CDataJSONEncoder

class Data(Structure):
    _fields_ = [
        ('a', c_int),
        ('b', c_int),
        ('c', c_int),
    ]

data = Data()

data.a = 10
data.b = 20
data.c = 30

json.dumps(data, cls=CDataJSONEncoder)
```

## License

[![license](https://img.shields.io/github/license/rinatz/binaries.svg)](https://github.com/rinatz/binaries/blob/master/LICENSE)

Copyright (c) 2017 Kenichiro IDA
