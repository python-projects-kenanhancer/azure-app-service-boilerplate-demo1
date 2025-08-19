import inspect

from cloudevents.http import CloudEvent, from_http
from flask import Request, Response, make_response

from ..decorators.pipeline_decorator import Context, Next


def typed_cloud_event_middleware(context: Context, next: Next):
    """Middleware that handles both CloudEvent and typed model input."""
    func = context.func
    args = context.args

    # 1. Get function signature info
    sig = inspect.signature(func)
    parameters = list(sig.parameters.values())
    if not parameters:
        raise TypeError(f"Function {func.__name__} has no parameters. Cannot infer typed cloud event parameter.")

    # 2. Check first parameter type annotation
    first_param = parameters[0]
    annotated_type = first_param.annotation
    if annotated_type is inspect._empty:
        raise TypeError(
            f"Function {func.__name__}'s first parameter '{first_param.name}' "
            "is not annotated with a type. Please provide a type annotation."
        )

    # 3. Check first argument
    if not args:
        raise ValueError("No arguments provided at runtime.")

    maybe_request = args[0]

    # If the argument is already the correct type, pass it through
    if isinstance(maybe_request, annotated_type):
        next()
        # return Response("OK", 200)  # Return OK response like functions_framework
        return make_response("OK")

    # Convert Flask Request to CloudEvent if needed
    if isinstance(maybe_request, Request):
        try:
            headers = dict(maybe_request.headers)
            cloud_event = from_http(headers, maybe_request.get_data())
            maybe_cloud_event = cloud_event
        except Exception as e:
            raise TypeError(f"Failed to convert Flask Request to CloudEvent: {str(e)}") from e
    else:
        maybe_cloud_event = maybe_request

    # If it's not a CloudEvent type after conversion, raise error
    if not isinstance(maybe_cloud_event, CloudEvent):
        raise TypeError(
            f"Expected first argument to be either {annotated_type.__name__} or CloudEvent, but got {type(maybe_cloud_event)}"
        )

    # Convert CloudEvent to typed object
    if not hasattr(annotated_type, "from_cloud_event"):
        raise AttributeError(f"Type '{annotated_type.__name__}' does not have a 'from_cloud_event' method.")

    typed_obj = annotated_type.from_cloud_event(maybe_cloud_event)

    # Replace first argument
    context.args = (typed_obj,) + args[1:]

    # Call next and return OK response
    next()

    return Response("OK", status=200)
