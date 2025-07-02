import protocols.broker
from .injector_rest import injector as rest_injector

# pylint: disable=line-too-long


def _frms_call(operation, endpoint, payload=None, content_type="application/json"):
    args = {
        "operation": operation,
        "headers": {"Content-Type": content_type},
        "path": f"/rm/services{endpoint}",
        "payload": payload,
    }
    response = protocols.broker.injector(args, "defaultKey", rest_injector)

    if response.status_code != 200 and response.status_code != 204:
        raise ValueError(f"Call to {args} failed with status {response.status_code}")

    if response.status_code == 204:
        return None

    response_json = response.json()

    # Check response does not contain error message
    if "messages" in response_json and len(response_json["messages"]) > 0:
        error = next(
            filter(
                lambda message: message["severity"] == "ERROR"
                or message["severity"] == "CRITICAL",
                response_json["messages"],
            ),
            None,
        )
        if error:
            raise ValueError(f"Call to {args} failed with error: {error}")

    return response_json
