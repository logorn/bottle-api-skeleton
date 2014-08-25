import importlib

class Settings(object):

    def __init__(self, settings_module):
        settings_module = 'local'
        try:
            mod = importlib.import_module(
                "." + settings_module,
                "apps.settings"
            )
        except ImportError as e:
            raise ImportError(
                "Could not import settings " +
                "'%s' (Is it on sys.path? Is " +
                "there an import error in the settings file?): %s"
                % (settings_module, e)
            )

        for setting in dir(mod):
            if setting == setting.upper():
                setattr(self, setting, getattr(mod, setting))

        from .. import di
        di.config(self)
