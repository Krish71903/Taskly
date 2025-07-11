from fastapi import APIRouter, HTTPException
from ..services.gmail_service import GmailService
from typing import List, Dict, Any

router = APIRouter()

@router.get("/recent")
def get_recent_emails() -> Dict[str, Any]:
    """Fetch recent emails from the authenticated user's Gmail."""
    try:
        # For development - use hardcoded user ID
        # In production, get this from authenticated session
        user_id = "current_user"
        
        gmail_service = GmailService(user_id)
        emails = gmail_service.get_recent_emails(max_results=10)
        
        return {
            "emails": emails,
            "count": len(emails)
        }
    
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching emails: {str(e)}")

@router.get("/email/{email_id}")
def get_email(email_id: str) -> Dict[str, Any]:
    """Get a specific email by ID."""
    try:
        user_id = "current_user"
        
        gmail_service = GmailService(user_id)
        email = gmail_service.get_email_by_id(email_id)
        
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        return {"email": email}
    
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching email: {str(e)}")

@router.post("/summarize")
def summarize_email(email_id: str):
    """Summarize an email using OpenAI (placeholder for now)."""
    try:
        user_id = "current_user"
        
        # Get the email content
        gmail_service = GmailService(user_id)
        email = gmail_service.get_email_by_id(email_id)
        
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        # Placeholder summary for now
        summary = f"Summary of email: {email['subject']} - {email['snippet'][:100]}..."
        
        return {
            "email_id": email_id,
            "summary": summary,
            "subject": email['subject']
        }
    
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing email: {str(e)}")

@router.post("/reply")
def draft_reply(email_id: str, prompt: str):
    """Draft a reply to an email using OpenAI (placeholder for now)."""
    try:
        user_id = "current_user"
        
        # Get the email content
        gmail_service = GmailService(user_id)
        email = gmail_service.get_email_by_id(email_id)
        
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        # Placeholder reply for now
        reply = f"Draft reply to '{email['subject']}' based on prompt: '{prompt}'"
        
        return {
            "email_id": email_id,
            "original_subject": email['subject'],
            "draft_reply": reply,
            "prompt": prompt
        }
    
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error drafting reply: {str(e)}") 