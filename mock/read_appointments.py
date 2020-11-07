from functools import wraps
from http import HTTPStatus
from .lambda_env_converter import convert

import boto3


def inject_appointment_mock_data():
    """

    """

    def decorator(func):
        @wraps(func)
        @convert(env_var_name="BUCKET_NAME", parameter_name="bucket_name")
        def load_appointment_mock_data(event, *args, **kwargs):
            bucket_name = kwargs.pop("bucket_name")

            s3_client = boto3.client('s3')
            try:
                appointment_mock_input_data = s3_client.get_object(Bucket=bucket_name, Key=f"mock_appointments.json")
            except s3_client.exceptions.NoSuchKey:
                return {
                    "statusCode": HTTPStatus.NOT_FOUND,
                    "body": "File not found"
                }

            s3_object_bytes = appointment_mock_input_data['Body'].read().decode("utf-8")

            kwargs["appointment_mock"] = s3_object_bytes
            return func(event, *args, **kwargs)

        return load_appointment_mock_data

    return decorator