from typing import Optional

from injector import Module

from ..decorators.pipeline_decorator import Context, Next
from ..dependency_injection_configurations import build_di_container


def container_builder_middleware(extra_modules: Optional[list[Module]] = None):
    container = build_di_container(extra_modules)

    def middleware(context: Context, next: Next):
        if "injector" not in context.kwargs:
            context.kwargs["injector"] = container
        return next()

    # Set the name dynamically
    middleware.__name__ = "container_builder_middleware"
    return middleware
