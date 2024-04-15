class EmptyFieldsError(Exception):
    """
    raised in: loginwindow.py
    Raise for empty Login or Password fields
    """
               
class LoginFailedError(Exception):
    """
    raised in: loginwindow.py
    Raised when Login fails. It is raised in loginwindow.py
    """

class DatabaseSelectError(Exception):
    """
    raised in: fileuploadcontainer.py
    Raised when Login fails. It is raised in loginwindow.py
    """

class DatabaseConnectionError(Exception):
    """
    raised in: magicDB.py
    Raised when connection fails.
    """
