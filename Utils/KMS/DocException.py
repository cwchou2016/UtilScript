class LoginFailedException(Exception):
    """Raise when login failed"""
    pass


class ReadDocException(Exception):
    """Raise when document cannot be read"""
    pass

class CreateDocException(Exception):
    """Raise when document cannot be created"""
    pass

class DocInfoException(Exception):
    """Raise when document info cannot be read"""
    pass