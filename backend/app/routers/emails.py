from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/recent")
def get_recent_emails():
    # Placeholder for fetching recent emails from Gmail
    return {"message": "List of recent emails"}

@router.post("/summarize")
def summarize_email(email_id: str):
    # Placeholder for summarizing an email using OpenAI
    return {"message": f"Summary of email {email_id}"}

@router.post("/reply")
def draft_reply(email_id: str, prompt: str):
    # Placeholder for drafting a reply using OpenAI
    return {"message": f"Draft reply for email {email_id} with prompt: {prompt}"} 