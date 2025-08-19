import inspect
from typing import Any, Dict

from fastapi import Request as FastAPIRequest
from flask import Request as FlaskRequest

from ..decorators.pipeline_decorator import Context, Next


def _extract_flask_request_data(request: FlaskRequest) -> tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Extract JSON, query, and header data from Flask request"""
    json_data = request.get_json(silent=True) or {}
    query_data = dict(request.args)
    header_data = {}  # or parse headers if needed
    return json_data, query_data, header_data


def _extract_fastapi_request_data(request: FastAPIRequest) -> tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Extract JSON, query, and header data from FastAPI request"""
    json_data: Dict[str, Any] = {}
    query_data: Dict[str, Any] = {}
    header_data: Dict[str, Any] = {}

    # Extract JSON data from request body
    json_data = _extract_json_from_fastapi_request(request)

    # Extract query parameters
    try:
        query_data = dict(request.query_params) if hasattr(request, "query_params") else {}
    except Exception:
        query_data = {}

    # Extract headers
    try:
        header_data = dict(request.headers) if hasattr(request, "headers") else {}
    except Exception:
        header_data = {}

    return json_data, query_data, header_data


def _extract_json_from_fastapi_request(request: FastAPIRequest) -> Dict[str, Any]:
    """Extract JSON data from FastAPI request body"""
    # Try to get JSON from request body
    if hasattr(request, "body") and callable(getattr(request, "body")):
        try:
            body = request.body()
            if hasattr(body, "__await__"):
                # Handle async body
                import asyncio

                parsed_body_data: Any = asyncio.run(body)
            else:
                parsed_body_data = body

            # Parse body data if it exists
            if parsed_body_data:
                import json

                if isinstance(parsed_body_data, bytes):
                    return json.loads(parsed_body_data.decode("utf-8"))
                elif isinstance(parsed_body_data, str):
                    return json.loads(parsed_body_data)
        except Exception:
            pass

    # Fallback: try to get JSON from request object
    # try:
    #     if hasattr(request, "_json"):
    #         return request._json
    #     elif hasattr(request, "json"):
    #         result = request.json()
    #         # Handle case where json() returns a coroutine
    #         if hasattr(result, "__await__"):
    #             # This is a coroutine, but we can't await it in a sync function
    #             # Return empty dict as fallback
    #             return {}
    #         # Ensure result is a dictionary before returning
    #         if isinstance(result, dict):
    #             return result
    #         else:
    #             # If result is not a dict, return empty dict
    #             return {}
    # except Exception:
    #     pass

    return {}


def _extract_request_data(request) -> tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Extract request data based on request type"""
    if isinstance(request, FlaskRequest):
        return _extract_flask_request_data(request)
    elif isinstance(request, FastAPIRequest):
        return _extract_fastapi_request_data(request)
    else:
        raise TypeError(f"Unsupported request type: {type(request)}")


def _detect_class_method_and_first_param(func, parameters):
    """Detect if this is a class method and determine the first non-self parameter."""
    is_class_method = False
    first_typed_param = None

    # Multiple strategies to detect class methods:
    # 1. Check if this is a bound method (instance method)
    if inspect.ismethod(func):
        is_class_method = True
        # For bound methods, first parameter is 'self', so we need the second parameter
        if len(parameters) > 1:
            first_typed_param = parameters[1]
        else:
            # Only 'self' parameter, nothing to process
            return is_class_method, None
    else:
        # 2. Check if the first parameter is named 'self' (Python convention)
        # This handles unbound methods and pipeline-wrapped class methods
        if parameters[0].name == "self" and len(parameters) > 1:
            is_class_method = True
            first_typed_param = parameters[1]
        # 3. Check if this looks like a class method by examining the function context
        elif hasattr(func, "__qualname__") and "." in func.__qualname__:
            # This might be a class method that was wrapped by a decorator
            # Check if the first parameter could be 'self' (instance parameter)
            if len(parameters) > 0:
                first_typed_param = parameters[0]
                # We'll treat this as a regular function for now
                is_class_method = False
        else:
            # Regular function or static method
            first_typed_param = parameters[0]

    return is_class_method, first_typed_param


def _get_request_argument(args, is_class_method):
    """Get the request argument from the function arguments."""
    if not args:
        raise ValueError("No arguments provided at runtime.")

    # For class methods, the first argument is 'self', so we need the second argument
    if is_class_method:
        if len(args) < 2:
            raise ValueError("Class method called without required arguments.")
        return args[1]
    else:
        # This is a regular function or unbound method
        return args[0]


def _validate_and_extract_request(maybe_request, annotated_type):
    """Validate request type and extract data."""
    # If the argument is already the correct type, pass it through
    if isinstance(maybe_request, annotated_type):
        return None  # Signal to pass through

    # If it's not a Request type, raise error immediately
    if not isinstance(maybe_request, (FlaskRequest, FastAPIRequest)):
        raise TypeError(
            f"Expected first argument to be either {annotated_type.__name__} "
            f"or Flask/FastAPI Request, but got {type(maybe_request)}"
        )

    # Extract request data using the encapsulated methods
    try:
        json_data, query_data, header_data = _extract_request_data(maybe_request)
    except Exception:
        # If extraction fails, use empty data
        json_data, query_data, header_data = {}, {}, {}

    # Ensure all are dictionaries before unpacking
    if not isinstance(json_data, dict):
        json_data = {}
    if not isinstance(query_data, dict):
        query_data = {}
    if not isinstance(header_data, dict):
        header_data = {}

    return json_data, query_data, header_data


def typed_request_middleware(context: Context, next: Next):
    """Middleware that handles both Flask Request and typed model input."""
    func = context.func
    args = context.args

    # 1. Get function signature info
    sig = inspect.signature(func)
    parameters = list(sig.parameters.values())
    if not parameters:
        raise TypeError(f"Function {func.__name__} has no parameters. Cannot infer typed request parameter.")

    # 2. Detect if this is a class method and determine the first non-self parameter
    is_class_method, first_typed_param = _detect_class_method_and_first_param(func, parameters)

    # Ensure we found a valid parameter
    if first_typed_param is None:
        raise TypeError(f"Function {func.__name__} has no valid parameters to process.")

    # 3. Check type annotation of the first typed parameter
    annotated_type = first_typed_param.annotation
    if annotated_type is inspect._empty:
        # If no type annotation, skip processing - this method doesn't need typed request conversion
        return next()

    # 4. Get request argument at runtime
    maybe_request = _get_request_argument(args, is_class_method)

    # 5. Validate and extract request data
    result = _validate_and_extract_request(maybe_request, annotated_type)

    # If result is None, it means we should pass through (already correct type)
    if result is None:
        return next()

    # Otherwise, we have extracted data to work with
    json_data, query_data, header_data = result

    merged_data = {**json_data, **query_data, **header_data}

    # Convert to typed object
    if not hasattr(annotated_type, "from_dict"):
        raise AttributeError(f"Type '{annotated_type.__name__}' does not have a 'from_dict' method.")
    typed_obj = annotated_type.from_dict(merged_data)

    # Replace the request argument (preserve 'self' for class methods)
    if is_class_method:
        # For class methods, replace the second argument (after 'self')
        context.args = (args[0], typed_obj) + args[2:]
    else:
        # For regular functions, replace the first argument
        context.args = (typed_obj,) + args[1:]

    result = next()

    # If the result has a `.to_dict()`, convert to dict so Flask can return JSON
    #    (Only if you want that automatically.)
    # if hasattr(result, "to_dict") and callable(result.to_dict):
    #     return result.to_dict()

    return result
