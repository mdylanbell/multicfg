========
multicfg
========

Load multiple configurations from various sources and merge them together.

Example json file at: ``/path/to/config.json``

.. code-block:: json
    {
        "id": "mr_example",
        "token": "ABCDEFGHIJ",
        "some": {
            "nested": {
                "bits": {
                    "value": 15,
                    "other_thing": 8
                }
            }
        }
    }

.. code-block:: python
    from multicfg.config import load_configuration

    config = load_configuration([
        ('json', {'file': '/path/to/config.json'})
    ])

    config.id == "mr_example"
    config.token == "ABCDEFGHIJ"
    config.some.nested.bits.value == 15


In active development
---------------------

Support for sqlalchemy, yaml, python are all coming soon.
You can also add your own parsers very easily.

More Information
----------------

load_configuration takes an array of tuples in the form of:
(type, location, path)

`type`: a defined ConfigType class, like 'json', 'sqlalchemy' or 'yaml'

`location`: This is a pointer to where to find the data.  Each ConfigType can
specify available locations, such as files, raw strings, database
connection information, etc.

You can specify a dictionary for precision, but the parser will try to
guess your meaning if you simply pass a string, by trying all available
options until one works.

    For example, with json type, location could be any of:
|        ``{'file': '/etc/myconfig.json'}``
|        ``'/etc/myconfig.json'``
|        ``{'string': '{"some_data": 15, "another_thing": "some_string"}'}``
|        ``'{"some_data": 15, "another_thing": "some_string"}'``

`path`: optional config path-prefix

Returns: The root Config() object that is the base of the configuration,
which can be traversed with attribute notation.

Further Examples
----------------

Example: given 'json' type that looks like:

.. code-block:: json
    {
        "a": {
            "b": {
                "c": {
                    "d": 15
                }
            }
        }
    }


.. code-block:: python
    config = load_configuration([
            ('json', {'file': '/path/to/above/config.json'}, 'h.i.j')
    ])

    config.h.i.j.a.b.c.d == 15
