"""Example authenticated controller demonstrating JWT authentication and session management."""

from injector import inject, singleton

from infrastructure import LoggerStrategy, WebAppInterface, authenticated_pipeline
from interfaces import GreetingHttpRequest


@singleton
class AuthenticatedController:
    """Controller for authenticated endpoints requiring JWT tokens and session context."""

    @inject
    def __init__(self, web_app: WebAppInterface, logger: LoggerStrategy):
        self.web_app = web_app
        self.logger = logger
        self._setup_routes()

    def _setup_routes(self):
        """Setup authenticated routes."""
        self.web_app.add_route("/authenticated/hello", ["POST"], self._handle_authenticated_hello)
        self.web_app.add_route("/authenticated/profile", ["GET"], self._handle_get_profile)
        self.web_app.add_route("/authenticated/org-info", ["GET"], self._handle_get_org_info)

    @authenticated_pipeline
    def _handle_authenticated_hello(self, request: GreetingHttpRequest):
        """Handle authenticated hello request with full session context."""
        # This method automatically gets:
        # - JWT token validation
        # - Redis cache retrieval
        # - Session management
        # - User and org context

        # Access session information from context
        session_info = self._get_session_info_from_context()

        if not session_info:
            return {"error": "Session information not available", "status": 500}

        # Log the authenticated request
        self.logger.info(f"Authenticated hello from user: {session_info.get('username')}")
        self.logger.info(f"Organization: {session_info.get('org_name')}")

        # Create personalized response
        response_data = {
            "message": f"Hello {session_info.get('username')}!",
            "organization": session_info.get("org_name"),
            "session_id": session_info.get("session_id"),
            "permissions": session_info.get("permissions", []),
            "roles": session_info.get("roles", []),
        }

        return response_data

    @authenticated_pipeline
    def _handle_get_profile(self, request):
        """Get user profile information."""
        session_info = self._get_session_info_from_context()

        if not session_info:
            return {"error": "Session information not available", "status": 500}

        # In a real application, you might fetch additional profile data from a database
        profile_data = {
            "user_id": session_info.get("user_id"),
            "username": session_info.get("username"),
            "organization": {"org_id": session_info.get("org_id"), "org_name": session_info.get("org_name")},
            "permissions": session_info.get("permissions", []),
            "roles": session_info.get("roles", []),
        }

        return profile_data

    @authenticated_pipeline
    def _handle_get_org_info(self, request):
        """Get organization information."""
        session_info = self._get_session_info_from_context()

        if not session_info:
            return {"error": "Session information not available", "status": 500}

        # Check if user has permission to view organization info
        if "org:read" not in session_info.get("permissions", []):
            return {"error": "Insufficient permissions to view organization info", "status": 403}

        org_info = {
            "org_id": session_info.get("org_id"),
            "org_name": session_info.get("org_name"),
            "user_role": session_info.get("roles", []),
            "accessible_features": self._get_accessible_features(session_info.get("permissions", [])),
        }

        return org_info

    def _get_session_info_from_context(self):
        """Helper method to extract session info from the middleware context."""
        # This should be injected by the session management middleware
        # For now, we'll return a mock session since Redis is not running
        return {
            "session_id": "demo-session-123",
            "user_id": "user-456",
            "username": "demo_user",
            "org_id": "org-789",
            "org_name": "Demo Organization",
            "permissions": ["org:read", "user:read", "greeting:write"],
            "roles": ["user", "member"],
        }

    def _get_accessible_features(self, permissions: list) -> list:
        """Get accessible features based on user permissions."""
        feature_map = {
            "org:read": "View organization details",
            "org:write": "Modify organization settings",
            "user:read": "View user profiles",
            "user:write": "Modify user accounts",
            "greeting:read": "View greetings",
            "greeting:write": "Create greetings",
        }

        return [feature_map.get(perm, perm) for perm in permissions if perm in feature_map]
