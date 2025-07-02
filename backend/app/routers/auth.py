from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from ..services import google_auth
from ..core.config import settings

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
    # For now, just print the credentials. In a real app, you would
    # create a user session, store tokens securely, and redirect to the dashboard.
    print("Received credentials:", credentials)
    
    # Construct the frontend dashboard URL from the redirect URI setting
    frontend_dashboard_url = settings.GOOGLE_REDIRECT_URI.replace("/auth/callback", "/dashboard")
    return RedirectResponse(url=frontend_dashboard_url) 