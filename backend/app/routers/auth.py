from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from ..services import google_auth
from ..core.config import settings
from ..core.security import store_tokens

router = APIRouter()

@router.get("/login")
def login_with_google():
    """
    Redirects the user to the Google OAuth consent screen.
    """
    auth_url, _ = google_auth.get_auth_url()
    return RedirectResponse(auth_url)

@router.get("/callback")
def auth_callback(code: str, state: str):
    """
    Handles the callback from Google after user authentication.
    Exchanges the authorization code for an access token.
    """
    credentials = google_auth.get_tokens_from_code(code, state)
    print("Received credentials:", credentials)
    
    # Store credentials securely (using user's email as ID for now)
    # In a real app, you'd use a proper user ID system
    user_id = "current_user"  # For development - in production use actual user ID
    store_tokens(user_id, credentials)
    print(f"Tokens stored for user: {user_id}")
    
    # Redirect to frontend dashboard
    frontend_dashboard_url = f"{settings.FRONTEND_URL}/dashboard"
    return RedirectResponse(url=frontend_dashboard_url) 