"""Shared pipeline configuration for the application."""

from ..decorators import pipeline
from ..middlewares import (
    container_builder_middleware,
    error_handling_middleware,
    inject_dependency_middleware,
    jwt_authentication_middleware,
    logger_middleware,
    performance_middleware,
    redis_cache_middleware,
    request_validation_middleware,
    session_management_middleware,
    time_middleware,
    typed_request_middleware,
)

di_container_builder_middleware = container_builder_middleware()

# Shared pipeline configuration used across the application
shared_pipeline = pipeline(
    di_container_builder_middleware,
    inject_dependency_middleware,
    typed_request_middleware,
    request_validation_middleware,
    logger_middleware,
    time_middleware,
    performance_middleware,
    error_handling_middleware,
)

# HTTP-specific pipeline with comprehensive middleware for aspect-oriented programming
http_pipeline = pipeline(
    di_container_builder_middleware,
    inject_dependency_middleware,
    typed_request_middleware,
    request_validation_middleware,
    logger_middleware,
    time_middleware,
    performance_middleware,
    error_handling_middleware,
)

# Authenticated pipeline with JWT authentication, Redis cache, and session management
authenticated_pipeline = pipeline(
    di_container_builder_middleware,
    inject_dependency_middleware,
    jwt_authentication_middleware,
    typed_request_middleware,
    request_validation_middleware,
    redis_cache_middleware,
    session_management_middleware,
    logger_middleware,
    time_middleware,
    performance_middleware,
    error_handling_middleware,
)

__all__ = ["shared_pipeline", "http_pipeline", "authenticated_pipeline"]
