"""Session Management Middleware for handling user and organization context."""

from typing import Any, Dict, Optional

from ..decorators.pipeline_decorator import Context, Next
from ..logger.logger_strategies.logger_strategy import LoggerStrategy


def session_management_middleware(context: Context, next: Next, logger: LoggerStrategy):
    """Middleware to manage user and organization session context."""

    logger.info(f"[SESSION_MGMT] Processing {context.func.__name__}")

    # Get session information from previous middleware
    session_id = context.kwargs.get("session_id")
    user_context = context.kwargs.get("user_context")
    org_context = context.kwargs.get("org_context")

    if not session_id or not user_context or not org_context:
        logger.warning("[SESSION_MGMT] Missing session context information")
        return {"error": "Session context incomplete", "status": 401}

    try:
        # Validate session context
        if not _validate_user_context(user_context, logger):
            return {"error": "Invalid user context", "status": 401}

        if not _validate_org_context(org_context, logger):
            return {"error": "Invalid organization context", "status": 401}

        # Add session management information to context
        context.kwargs["session_info"] = {
            "session_id": session_id,
            "user_id": user_context.get("user_id"),
            "username": user_context.get("username"),
            "org_id": org_context.get("org_id"),
            "org_name": org_context.get("org_name"),
            "permissions": user_context.get("permissions", []),
            "roles": user_context.get("roles", []),
        }

        # Log session information
        logger.info(f"[SESSION_MGMT] Session validated for user: {user_context.get('username')}")
        logger.info(f"[SESSION_MGMT] Organization: {org_context.get('org_name')}")
        logger.info(f"[SESSION_MGMT] Permissions: {len(user_context.get('permissions', []))}")

        # Continue with the request
        result = next()
        return result

    except Exception as e:
        logger.error(f"[SESSION_MGMT] Session management error: {str(e)}")
        return {"error": "Session management error", "status": 500}


def _validate_user_context(user_context: Dict[str, Any], logger: LoggerStrategy) -> bool:
    """Validate user context data."""
    required_fields = ["user_id", "username", "email"]

    for field in required_fields:
        if not user_context.get(field):
            logger.warning(f"[SESSION_MGMT] Missing required user field: {field}")
            return False

    # Validate user permissions
    permissions = user_context.get("permissions", [])
    if not isinstance(permissions, list):
        logger.warning("[SESSION_MGMT] User permissions must be a list")
        return False

    # Validate user roles
    roles = user_context.get("roles", [])
    if not isinstance(roles, list):
        logger.warning("[SESSION_MGMT] User roles must be a list")
        return False

    return True


def _validate_org_context(org_context: Dict[str, Any], logger: LoggerStrategy) -> bool:
    """Validate organization context data."""
    required_fields = ["org_id", "org_name"]

    for field in required_fields:
        if not org_context.get(field):
            logger.warning(f"[SESSION_MGMT] Missing required organization field: {field}")
            return False

    # Validate organization settings
    org_settings = org_context.get("settings", {})
    if not isinstance(org_settings, dict):
        logger.warning("[SESSION_MGMT] Organization settings must be a dictionary")
        return False

    return True


def get_session_info(context: Context) -> Optional[Dict[str, Any]]:
    """Utility function to get session information from context."""
    return context.kwargs.get("session_info")


def get_user_permissions(context: Context) -> list:
    """Utility function to get user permissions from context."""
    session_info = get_session_info(context)
    return session_info.get("permissions", []) if session_info else []


def get_user_roles(context: Context) -> list:
    """Utility function to get user roles from context."""
    session_info = get_session_info(context)
    return session_info.get("roles", []) if session_info else []


def has_permission(context: Context, required_permission: str) -> bool:
    """Utility function to check if user has a specific permission."""
    permissions = get_user_permissions(context)
    return required_permission in permissions


def has_role(context: Context, required_role: str) -> bool:
    """Utility function to check if user has a specific role."""
    roles = get_user_roles(context)
    return required_role in roles


def require_permission(permission: str):
    """Decorator to require a specific permission for a function."""

    def decorator(func):
        def wrapper(context: Context, next: Next, **kwargs):
            if not has_permission(context, permission):
                logger = kwargs.get("logger")
                if logger:
                    logger.warning(f"[SESSION_MGMT] Permission denied: {permission}")
                return {"error": "Insufficient permissions", "status": 403}
            return func(context, next, **kwargs)

        return wrapper

    return decorator


def require_role(role: str):
    """Decorator to require a specific role for a function."""

    def decorator(func):
        def wrapper(context: Context, next: Next, **kwargs):
            if not has_role(context, role):
                logger = kwargs.get("logger")
                if logger:
                    logger.warning(f"[SESSION_MGMT] Role denied: {role}")
                return {"error": "Insufficient role", "status": 403}
            return func(context, next, **kwargs)

        return wrapper

    return decorator
