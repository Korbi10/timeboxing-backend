import json
from http import HTTPStatus

from .read_appointments import inject_appointment_mock_data
from .extract_path_parameters import extract_path_parameter, ID_REGEX

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


@inject_appointment_mock_data()
@extract_path_parameter("id", function_parameter_name="appointmentId", regex=ID_REGEX)
def handler_get_by_id(event, context, appointment_mock, **kwargs):
    appointment_id = kwargs.pop("appointmentId")
    try:
        appointments_dict = list(eval(appointment_mock))
        appointment = next((item for item in appointments_dict if item['id'] == appointment_id), None)
        if appointment is None:
            return {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "headers": {
                    "content-type": CONTENT_TYPE,
                },
                "body": "Appointment could not be found"
            }
        else:
            return {
                "statusCode": HTTPStatus.OK,
                "headers": {
                    "content-type": CONTENT_TYPE,
                },
                "body": json.dumps(appointment)
            }
    except:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "headers": {
                "content-type": CONTENT_TYPE,
            },
            "body": "Wrong parameter"
        }

