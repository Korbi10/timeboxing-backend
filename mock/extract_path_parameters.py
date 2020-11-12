import re
from functools import wraps
from http import HTTPStatus
from typing import Optional, Pattern

ID_REGEX: Pattern[str] = re.compile("^[A-Za-z0-9-_]+$")


def extract_path_parameter(parameter_name: str, function_parameter_name: Optional[str] = None,
                           regex: Optional[Pattern[str]] = None):
    """
    The extract_path_parameter decorator extracts a path parameter and passes it to the function being decorated.
    Additionally, the parameter can be checked against a regular expression.

    If the parameter doesn't exist or does not match the regular expression, the decorator returns a HTTP 400 response
    and does not call the decorated function.
    """

    def decorator(func):
        @wraps(func)
        def extract_path_parameter_inner(event, *args, **kwargs):
            if parameter_name not in event["pathParameters"]:
                return {
                    "statusCode": HTTPStatus.BAD_REQUEST
                }

            parameter_value = event["pathParameters"][parameter_name]

            if regex is not None:
                if not regex.match(parameter_value):
                    return {
                        "statusCode": HTTPStatus.BAD_REQUEST
                    }

            if function_parameter_name is None:
                kwargs[parameter_name] = parameter_value
            else:
                kwargs[function_parameter_name] = parameter_value

            return func(event, *args, **kwargs)

        return extract_path_parameter_inner

    return decorator
