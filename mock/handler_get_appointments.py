import json
from http import HTTPStatus

from .read_appointments import inject_appointment_mock_data

CONTENT_TYPE: str = "application/json"


@inject_appointment_mock_data()
def handler(event, context, appointment_mock):
    return {
        "statusCode": HTTPStatus.OK,
        "headers": {
            "content-type": CONTENT_TYPE,
        },
        "body": json.dumps(json.loads(appointment_mock))
    }
