#!/usr/bin/env python

from multicfg.config import load_configuration

config = load_configuration([
    ('json', {'file': 'test.json'}),
    ('json', {'file': 'test.json'}, 'abc.def.ghi'),
    ('json', '{"first_name": "matt", "last_name": "bell"}'),
    ('json', 'test.json', 'testing_string_only_filename')
])

print('\nprint() with default formatting')
config.print()

print('\nprint() with json formatting')
config.print(format='json', sort_keys=True, indent=4)

print('\nprint() with python formatting')
config.print(format='python', indent=2, compact=True, depth=9)
