from functools import wraps


def retry_on_unauthorized(func):
    """
    Decorator to retry a function if it raises a 401 Unauthorized error.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        response = func(self, *args, **kwargs)
        if response.status_code == 401:
            self.login()
            response = func(self, *args, **kwargs)
        response.raise_for_status()
        return response

    return wrapper
