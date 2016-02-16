import pprint

from multicfg.config_type import ConfigType


class Config(object):
    """ Config class:
    Config instances are basically nodes that represent the various points
    in the ultimate configuration path.  Each node in a path is an instance
    of Config.
    """
    def update_config(self, data, path=None):
        # If we have a path, we need to recurse to create Config objects
        # at each level (for easy traversal and calling)
        if path:
            try:
                (path_next, path_remainder) = path.split('.', 1)
            except ValueError:
                (path_next, path_remainder) = (path, None)

            if not hasattr(self, path_next):
                setattr(self, path_next, Config())

            layer = getattr(self, path_next)
            layer.update_config(data, path_remainder)
        else:
            # We don't have a specified path, but we still need to make paths
            # for nested dictionary items.
            for (key, value) in data.items():
                if isinstance(value, dict):
                    self.update_config(value, key)
                else:
                    # Finally, an actual data point.  Just set the attribute.
                    setattr(self, key, value)

    def print(self, format='python', indent=4, **kwargs):
        """ print
        This method prints out our nested Config.  It primarily leans on our
        defined ConfigType classes to do so.

        format: the format/ConfigType to use to display the data
        indent: Since most/all config parsers understand indent, it was
            left here for readability and a default value.
        kwargs: Used to pass through other arguments to the ConfigType
            pretty_print methods for use with config parser pretty print
            options.
        """
        data = self.as_dict()

        if format == 'python':
            pp = pprint.PrettyPrinter(indent=indent, **kwargs)
            pp.pprint(data)
        else:
            type_obj = ConfigType.load_module(format)
            type_obj.pretty_print(data, indent=indent, **kwargs)

    def as_dict(self):
        """ as_dict
        Return a dictionary representation of our nested Config scheme.
        """
        config = {}

        for (key, value) in self.__dict__.items():
            if isinstance(value, Config):
                config[key] = value.as_dict()
            else:
                config[key] = value

        return config


def load_configuration(locations):
    """ load_configuration
    Takes an array of tuples in the form of (type, location, path)

    type: a defined ConfigType class, like 'json', 'sqlalchemy' or 'yaml'
    location: This is a pointer to where to find the data.  Each ConfigType can
       specify available locations, such as files, raw strings, database
       connection information, etc.

       You can specify a dictionary for precision, but the parser will try to
       guess your meaning if you simply pass a string, by trying all available
       options until one works.

       For example, with json type, location could be any of:
           {'file': '/etc/myconfig.json'}
           '/etc/myconfig.json'}
           {'string': '{"some_data": 15, "another_thing": "some_string"}'}
           '{"some_data": 15, "another_thing": "some_string"}'

    path: optional config path-prefix

    Returns: The root Config() object that is the base of the configuration,
    which can be traverssed with attribute notation.

    Example: given 'json' type that looks like:
        {
            "a": {
                "b": {
                    "c": {
                        "d": 15
                    }
                }
            }
        }

    passing ('json', '/path/to/above/config.json') will return an object where
    a.b.c.d = 15

    config = load_configuration([
            ('json', {'file': '/path/to/above/config.json'})
    ])

    config.a.b.c.d == 15

    if the last tuple elementi representing 'path' is 'h.i.j',
    the value is accessible at h.i.j.a.b.c.d
    """
    config = Config()

    for loc in locations:
        try:
            _type = loc[0]
            _location = loc[1]
        except IndexError:
            raise SystemExit('One of "config type" or "location" not '
                             'specified')

        try:
            _path = loc[2]
        except IndexError:
            _path = None

        type_class = ConfigType.load_module(_type)
        type_config = type_class.load(_location)

        config.update_config(type_config, _path)

    return config
