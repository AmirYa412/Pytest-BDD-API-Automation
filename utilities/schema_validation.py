import json
from jsonschema import validate, ValidationError


def validate_schema(response: dict, schema: dict):
    """
    Validates a dictionary against a JSON schema.

    Args:
        response: The API response dictionary to validate.
        schema: The Pydantic or dict-based JSON schema.

    Raises:
        AssertionError: With a formatted message if validation fails.
    """
    try:
        validate(instance=response, schema=schema)
    except ValidationError as e:
        # Pretty print the response for easier debugging in the report
        formatted_json = json.dumps(response, indent=2)
        error_message = (
            f"\n Schema Validation Failed!"
            f"\nReason: {e.message}"
            f"\nSchema Path: {list(e.path)}"
            f"\n\nReceived Response:\n{formatted_json}"
        )
        raise AssertionError(error_message) from e