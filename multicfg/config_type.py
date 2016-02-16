import importlib
import sys

from abc import ABCMeta, abstractmethod

from multicfg.exceptions import ConfigError


TYPE_MODULE_PREFIX = 'multicfg.config_types.'


class ConfigType(metaclass=ABCMeta):
    @abstractmethod
    def pretty_print(data):
        raise NotImplementedError('pretty_print not defined by derived class')

    @staticmethod
    def load_module(name):
        module = importlib.__import__(TYPE_MODULE_PREFIX + name,
                                      fromlist=[name])
        klass = getattr(module, name)

        return klass

    @classmethod
    def load(cls, location):
        options = cls.location_options

        if isinstance(location, dict):
            for opt in options:
                if opt in location.keys():
                    method = cls._get_method('load_from_' + opt)

                    # Try to call the implementation method.  If there's an
                    # exception, let it go
                    return method(location[opt])
            else:
                print('Unknown {0} location option: {1}'.format(
                    cls.__name__, opt), file=sys.stderr)

        elif isinstance(location, str):
            # They just passed in a string.  Try the location options in
            # order they were defined.
            errors = []

            for opt in options:
                method = cls._get_method('load_from_' + opt)

                try:
                    return method(location)
                except Exception as e:
                    errors.append(e)
                    continue
            else:
                raise ConfigError("Exhausted all configuration load options "
                                  "while attempting to load: '{0}'. "
                                  "Captured errors:\n{1}".format(
                                      location, '\n'.join([str(err) for err
                                                           in errors])))

    @classmethod
    def _get_method(cls, name):
        try:
            method = getattr(cls, name)
            if callable(method):
                return method
        except AttributeError:
            raise NotImplementedError('A derived class did not implement an '
                                      'expected method: ' + name)
