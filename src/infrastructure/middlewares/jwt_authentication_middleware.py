"""JWT Authentication Middleware for extracting and validating JWT tokens."""

from typing import Any, Dict, Optional

from ..decorators.pipeline_decorator import Context, Next
from ..logger.logger_strategies.logger_strategy import LoggerStrategy
from ..repositories import AuthRepository


def jwt_authentication_middleware(context: Context, next: Next, logger: LoggerStrategy, auth_repository: AuthRepository):
    """Middleware to extract and validate JWT tokens from requests."""

    logger.info(f"[JWT_AUTH] Processing {context.func.__name__}")

    # Extract JWT token from request headers
    jwt_token = _extract_jwt_token(context)

    if not jwt_token:
        logger.warning("[JWT_AUTH] No JWT token found in request")
        return {"error": "Authentication required", "status": 401}

    try:
        # Decode and validate JWT token using AuthRepository
        decoded_token = auth_repository.decode_jwt_token(jwt_token)
        if not decoded_token:
            logger.warning("[JWT_AUTH] Invalid JWT token")
            return {"error": "Invalid JWT token", "status": 401}

        # Extract session ID from JWT payload
        session_id = _extract_session_id(decoded_token, logger)
        if not session_id:
            return {"error": "Invalid session in JWT token", "status": 401}

        # Validate session using AuthRepository
        session_valid, user_context, org_context = auth_repository.validate_session(session_id)
        if not session_valid:
            logger.warning(f"[JWT_AUTH] Invalid session: {session_id}")
            return {"error": "Invalid session", "status": 401}

        # Add session information to context for downstream middleware
        context.kwargs["jwt_token"] = jwt_token
        context.kwargs["decoded_token"] = decoded_token
        context.kwargs["session_id"] = session_id
        context.kwargs["user_context"] = user_context
        context.kwargs["org_context"] = org_context

        logger.info(f"[JWT_AUTH] JWT token validated successfully for session: {session_id}")

        # Continue with the request
        result = next()
        return result

    except Exception as e:
        logger.error(f"[JWT_AUTH] JWT authentication error: {str(e)}")
        return {"error": "Authentication error", "status": 500}


def _extract_jwt_token(context: Context) -> Optional[str]:
    """Extract JWT token from request headers."""
    if not context.args or len(context.args) == 0:
        return None

    request = context.args[1]

    # Check Authorization header
    if hasattr(request, "headers"):
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove 'Bearer ' prefix

    # Check for JWT in query parameters (alternative)
    if hasattr(request, "args") and hasattr(request.args, "get"):
        return request.args.get("token")

    return None


# This function is no longer needed as we use AuthRepository.decode_jwt_token


def _extract_session_id(decoded_token: Dict[str, Any], logger: LoggerStrategy) -> Optional[str]:
    """Extract session ID from decoded JWT token."""
    # Extract session ID from JWT payload
    # Adjust the key based on your JWT structure
    session_id = decoded_token.get("session_id") or decoded_token.get("sid") or decoded_token.get("sub")

    if not session_id:
        logger.warning("[JWT_AUTH] No session ID found in JWT token")
        return None

    return str(session_id)
