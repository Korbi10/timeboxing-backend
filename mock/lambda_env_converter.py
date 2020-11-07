import os
from functools import wraps
from http import HTTPStatus
from typing import Optional


def convert(env_var_name: str, parameter_name: str, default: Optional[str] = None):
    """
    The convert decorator converts the specified environment variable into a function parameter. If the environment
    variable does not exist, the decorator returns HTTPStatus.INTERNAL_SERVER_ERROR.

    In the following example the foo parameter is populated with the content of the environment variable FOO.
    @convert(env_var_name="FOO", parameter_name="foo")
    def do_something(foo):
        print(foo)
    """

    def decorator(func):
        @wraps(func)
        def converter(*args, **kwargs):
            if default is not None:
                kwargs[parameter_name] = os.getenv(env_var_name, default)
                return func(*args, **kwargs)

            optional_env_var = os.getenv(env_var_name)
            if optional_env_var is None:
                return {
                    "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "body": f"environment variable '{env_var_name}' not defined"
                }

            kwargs[parameter_name] = optional_env_var

            return func(*args, **kwargs)

        return converter

    return decorator
