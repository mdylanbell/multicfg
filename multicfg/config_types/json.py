import json as json_lib

from multicfg.config_type import ConfigType
from multicfg.exceptions import ConfigError


class json(ConfigType):
    location_options = ['string', 'file']

    @staticmethod
    def load_from_string(string):
        try:
            return json_lib.loads(string)
        except ValueError as e:
            raise ConfigError('Unable to load JSON string\n' + str(e))

    @staticmethod
    def load_from_file(filename):
        try:
            with open(filename, 'r') as fh:
                return json_lib.load(fh)
        except ValueError as e:
            raise ConfigError("While parsing '{0}', invalid JSON was "
                              "detected\n{1}".format(filename, e))
        except OSError:
            raise ConfigError("Unable to open JSON config file: '{0}'"
                              .format(filename))

    @staticmethod
    def pretty_print(data, **kwargs):
        print(json_lib.dumps(data, **kwargs))
