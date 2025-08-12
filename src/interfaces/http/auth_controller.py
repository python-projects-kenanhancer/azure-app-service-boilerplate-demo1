"""Authentication controller for login, logout, and session management."""

from typing import Any, Dict, Optional

from injector import inject, singleton

from infrastructure import LoggerStrategy, WebAppInterface, pipeline, shared_pipeline
from infrastructure.repositories import AuthRepository


@singleton
class AuthController:
    """Controller for authentication endpoints."""

    @inject
    def __init__(self, web_app: WebAppInterface, logger: LoggerStrategy, auth_repository: AuthRepository):
        self.web_app = web_app
        self.logger = logger
        self.auth_repository = auth_repository
        self._setup_routes()

    def _setup_routes(self):
        """Setup authentication routes."""
        self.web_app.add_route("/auth/login", ["POST"], self._handle_login)
        self.web_app.add_route("/auth/logout", ["POST"], self._handle_logout)
        self.web_app.add_route("/auth/refresh", ["POST"], self._handle_refresh_token)
        self.web_app.add_route("/auth/me", ["GET"], self._handle_get_current_user)

    @pipeline(shared_pipeline)
    def _handle_login(self, request):
        """Handle user login and create session."""
        try:
            # Extract login credentials from request
            request_data = self.web_app.get_json_data(request)
            username = request_data.get("username")
            password = request_data.get("password")

            if not username or not password:
                return self.web_app.create_response({"error": "Username and password are required"}, 400)

            # Authenticate user (in a real app, this would check against database)
            user_data = self._authenticate_user(username, password)
            if not user_data:
                return self.web_app.create_response({"error": "Invalid credentials"}, 401)

            # Create user context data
            user_context = {
                "user_id": user_data["user_id"],
                "username": user_data["username"],
                "email": user_data["email"],
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "permissions": user_data["permissions"],
                "roles": user_data["roles"],
            }

            # Create organization context data
            org_context = {"org_id": user_data["org_id"], "org_name": user_data["org_name"], "org_slug": user_data["org_slug"]}

            # Create session using AuthRepository
            session_created, session_id, jwt_token = self.auth_repository.create_session(user_context, org_context)

            if not session_created:
                self.logger.error("Failed to create session")
                return self.web_app.create_response({"error": "Failed to create session"}, 500)

            # Log successful login
            self.logger.info(f"User {username} logged in successfully with session: {session_id}")

            return self.web_app.create_response(
                {
                    "message": "Login successful",
                    "token": jwt_token,
                    "user": {
                        "user_id": user_data["user_id"],
                        "username": user_data["username"],
                        "email": user_data["email"],
                        "first_name": user_data["first_name"],
                        "last_name": user_data["last_name"],
                        "organization": {"org_id": user_data["org_id"], "org_name": user_data["org_name"]},
                    },
                    "expires_in": 3600,
                },
                200,
            )

        except Exception as e:
            self.logger.error(f"Login error: {str(e)}")
            return self.web_app.create_response({"error": "Internal server error"}, 500)

    @pipeline(shared_pipeline)
    def _handle_logout(self, request):
        """Handle user logout and invalidate session."""
        try:
            # Extract JWT token from request
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return self.web_app.create_response({"error": "Authorization header required"}, 401)

            jwt_token = auth_header[7:]  # Remove 'Bearer ' prefix

            # Decode JWT to get session ID
            payload = self.auth_repository.decode_jwt_token(jwt_token)
            if not payload:
                return self.web_app.create_response({"error": "Invalid token"}, 401)

            session_id = payload.get("session_id")
            if not session_id:
                return self.web_app.create_response({"error": "Invalid token"}, 401)

            # Invalidate session using AuthRepository
            session_invalidated = self.auth_repository.invalidate_session(session_id)
            if session_invalidated:
                self.logger.info(f"Session invalidated: {session_id}")
            else:
                self.logger.warning("Failed to invalidate session")

            return self.web_app.create_response({"message": "Logout successful"}, 200)

        except Exception as e:
            self.logger.error(f"Logout error: {str(e)}")
            return self.web_app.create_response({"error": "Internal server error"}, 500)

    @pipeline(shared_pipeline)
    def _handle_refresh_token(self, request):
        """Handle token refresh."""
        try:
            # Extract current JWT token
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return self.web_app.create_response({"error": "Authorization header required"}, 401)

            current_token = auth_header[7:]
            payload = self.auth_repository.decode_jwt_token(current_token)

            if not payload:
                return self.web_app.create_response({"error": "Invalid token"}, 401)

            session_id = payload.get("session_id")
            if not session_id:
                return self.web_app.create_response({"error": "Invalid token"}, 401)

            # Validate session and get user context
            session_valid, user_context, org_context = self.auth_repository.validate_session(session_id)
            if not session_valid:
                return self.web_app.create_response({"error": "Session expired"}, 401)

            # Refresh session
            session_refreshed = self.auth_repository.refresh_session(session_id)
            if not session_refreshed:
                return self.web_app.create_response({"error": "Failed to refresh session"}, 500)

            # Generate new JWT token
            if user_context:
                new_token = self.auth_repository.generate_jwt_token(session_id, user_context)
            else:
                return self.web_app.create_response({"error": "Invalid user context"}, 500)

            return self.web_app.create_response(
                {"message": "Token refreshed successfully", "token": new_token, "expires_in": 3600}, 200
            )

        except Exception as e:
            self.logger.error(f"Token refresh error: {str(e)}")
            return self.web_app.create_response({"error": "Internal server error"}, 500)

    @pipeline(shared_pipeline)
    def _handle_get_current_user(self, request):
        """Get current user information from session."""
        try:
            # Extract JWT token
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return self.web_app.create_response({"error": "Authorization header required"}, 401)

            jwt_token = auth_header[7:]
            payload = self.auth_repository.decode_jwt_token(jwt_token)

            if not payload:
                return self.web_app.create_response({"error": "Invalid token"}, 401)

            session_id = payload.get("session_id")
            if not session_id:
                return self.web_app.create_response({"error": "Invalid token"}, 401)

            # Validate session and get user context
            session_valid, user_context, org_context = self.auth_repository.validate_session(session_id)
            if not session_valid or not user_context:
                return self.web_app.create_response({"error": "Session expired"}, 401)

            return self.web_app.create_response({"user": user_context}, 200)

        except Exception as e:
            self.logger.error(f"Get current user error: {str(e)}")
            return self.web_app.create_response({"error": "Internal server error"}, 500)

    def _authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user credentials (mock implementation)."""
        # In a real application, this would check against a database
        # For demo purposes, we'll use a mock user

        if username == "demo_user" and password == "demo_password":
            return {
                "user_id": "user-456",
                "username": "demo_user",
                "email": "demo@example.com",
                "first_name": "Demo",
                "last_name": "User",
                "org_id": "org-789",
                "org_name": "Demo Organization",
                "org_slug": "demo-org",
                "permissions": ["org:read", "user:read", "greeting:write"],
                "roles": ["user", "member"],
            }

        return None
