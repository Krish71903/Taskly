from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from typing import Optional, List, Dict, Any
import base64
import email
import re
from email.mime.text import MIMEText
from ..core.security import get_tokens

class GmailService:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Gmail service with user credentials."""
        tokens = get_tokens(self.user_id)
        if not tokens:
            raise ValueError(f"No credentials found for user {self.user_id}")
        
        credentials = Credentials(
            token=tokens['token'],
            refresh_token=tokens['refresh_token'],
            token_uri=tokens['token_uri'],
            client_id=tokens['client_id'],
            client_secret=tokens['client_secret'],
            scopes=tokens['scopes']
        )
        
        self.service = build('gmail', 'v1', credentials=credentials)
    
    def get_recent_emails(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Fetch recent emails from Gmail."""
        try:
            # Get list of messages
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q='in:inbox'  # Only inbox emails
            ).execute()
            
            messages = results.get('messages', [])
            
            email_list = []
            for message in messages:
                # Get full message details
                msg = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                # Extract email data
                email_data = self._extract_email_data(msg)
                email_list.append(email_data)
            
            return email_list
        
        except Exception as e:
            print(f"Error fetching emails: {str(e)}")
            return []
    
    def get_email_by_id(self, email_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific email by ID."""
        try:
            msg = self.service.users().messages().get(
                userId='me',
                id=email_id,
                format='full'
            ).execute()
            
            return self._extract_email_data(msg)
        
        except Exception as e:
            print(f"Error fetching email {email_id}: {str(e)}")
            return None
    
    def _extract_email_data(self, msg: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant data from Gmail message."""
        headers = msg['payload'].get('headers', [])
        
        # Extract header information
        subject = self._get_header_value(headers, 'Subject')
        sender = self._get_header_value(headers, 'From')
        date = self._get_header_value(headers, 'Date')
        to = self._get_header_value(headers, 'To')
        
        # Extract body (returns dict with html, text, content)
        body_data = self._extract_body(msg['payload'])
        
        return {
            'id': msg['id'],
            'thread_id': msg['threadId'],
            'subject': subject,
            'sender': sender,
            'date': date,
            'to': to,
            'body': body_data['content'],  # For backward compatibility
            'body_html': body_data['html'],
            'body_text': body_data['text'],
            'snippet': msg.get('snippet', ''),
            'label_ids': msg.get('labelIds', [])
        }
    
    def _get_header_value(self, headers: List[Dict], name: str) -> str:
        """Get header value by name."""
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ''
    
    def _extract_body(self, payload: Dict[str, Any]) -> Dict[str, str]:
        """Extract email body from payload, returning both HTML and plain text."""
        html_body = ""
        text_body = ""
        
        if 'parts' in payload:
            # Multi-part message - extract both HTML and plain text
            for part in payload['parts']:
                if part['mimeType'] == 'text/html':
                    data = part['body'].get('data')
                    if data:
                        html_body = base64.urlsafe_b64decode(data).decode('utf-8')
                elif part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        text_body = base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            # Simple message
            if payload['mimeType'] == 'text/html':
                data = payload['body'].get('data')
                if data:
                    html_body = base64.urlsafe_b64decode(data).decode('utf-8')
            elif payload['mimeType'] == 'text/plain':
                data = payload['body'].get('data')
                if data:
                    text_body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        # Return HTML if available, otherwise plain text
        return {
            'html': html_body.strip() if html_body else '',
            'text': text_body.strip() if text_body else '',
            'content': html_body.strip() if html_body else text_body.strip()
        }
    
    def _clean_html(self, html_content: str) -> str:
        """Convert HTML content to clean plain text."""
        # Remove style tags and their contents
        clean = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove script tags and their contents
        clean = re.sub(r'<script[^>]*>.*?</script>', '', clean, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove head tags and their contents
        clean = re.sub(r'<head[^>]*>.*?</head>', '', clean, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove CSS media queries and other CSS blocks that might be outside style tags
        clean = re.sub(r'@media[^{]*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', '', clean, flags=re.DOTALL)
        clean = re.sub(r'@font-face[^{]*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', '', clean, flags=re.DOTALL)
        
        # Remove remaining CSS-like content (anything that looks like CSS rules)
        clean = re.sub(r'\{[^{}]*(?::[^{}]*;[^{}]*)*\}', '', clean)
        
        # Remove HTML comments
        clean = re.sub(r'<!--.*?-->', '', clean, flags=re.DOTALL)
        
        # Remove all HTML tags
        clean = re.sub(r'<[^>]+>', '', clean)
        
        # Decode common HTML entities
        html_entities = {
            '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>',
            '&quot;': '"', '&#39;': "'", '&apos;': "'", '&cent;': '¢',
            '&pound;': '£', '&yen;': '¥', '&euro;': '€', '&copy;': '©',
            '&reg;': '®', '&trade;': '™', '&ldquo;': '"', '&rdquo;': '"',
            '&lsquo;': "'", '&rsquo;': "'", '&ndash;': '–', '&mdash;': '—'
        }
        
        for entity, replacement in html_entities.items():
            clean = clean.replace(entity, replacement)
        
        # Clean up whitespace
        clean = re.sub(r'\n\s*\n\s*\n+', '\n\n', clean)  # Multiple newlines to double newlines
        clean = re.sub(r'[ \t]+', ' ', clean)  # Multiple spaces/tabs to single space
        clean = re.sub(r'\n ', '\n', clean)  # Remove spaces at start of lines
        clean = re.sub(r' \n', '\n', clean)  # Remove spaces at end of lines
        
        # Remove any remaining CSS-like patterns
        clean = re.sub(r'[a-zA-Z-]+\s*:\s*[^;]+;', '', clean)
        clean = re.sub(r'font-[a-zA-Z-]+\s*:', '', clean)
        clean = re.sub(r'mso-[a-zA-Z-]+\s*:', '', clean)
        
        return clean.strip()
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email."""
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            send_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return True
        
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False 