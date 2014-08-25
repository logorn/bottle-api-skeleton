
class ImproperlyConfigured(Exception):
    """Raised on an improperly configured setting
    """
    pass


class ImproperlyImplemented(Exception):
    """Raised when a missing resource is missing
    """
    pass


class InvalidData(Exception):
    """Raised when a request with invalide data is sent
    """
    pass


class ConnectionFailed(Exception):
    """Raised when a connectino with a hardware failed
    """
    pass
