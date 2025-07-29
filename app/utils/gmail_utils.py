from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from base64 import urlsafe_b64decode
import re
import base64  # Added missing import

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
TARGET_SENDER = "mlintern.aakashlabs@gmail.com"

def authenticate_gmail():
    """Connect to Gmail API"""
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def get_unread_messages(service):
    """More reliable unread message fetcher"""
    try:
        # First try strict query
        query = f'is:unread from:{TARGET_SENDER}'
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=5
        ).execute()
        
        # Fallback to less strict search if no results
        if not results.get('messages'):
            query = f'from:{TARGET_SENDER}'
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=5
            ).execute()
            
        return results.get('messages', [])
    
    except Exception as e:
        print(f"Gmail API error: {e}")
        return []

def extract_email_content(service, message_id):
    """Extract subject and clean body text"""
    msg = service.users().messages().get(
        userId='me',
        id=message_id,
        format='full'
    ).execute()
    
    # Get headers
    headers = {h['name'].lower(): h['value'] for h in msg['payload']['headers']}
    subject = headers.get('subject', 'No Subject')
    sender = headers.get('from', '')
    
    # Extract and clean body
    body = ""
    if 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                body_data = part['body'].get('data', '')
                if body_data:
                    body = _clean_text(urlsafe_b64decode(body_data).decode('utf-8'))
    else:
        body_data = msg['payload']['body'].get('data', '')
        if body_data:
            body = _clean_text(urlsafe_b64decode(body_data).decode('utf-8'))
    
    return {
        'subject': subject,
        'body': body,
        'sender': sender,
        'message_id': message_id
    }

def _clean_text(text):
    """Remove quoted text and signatures"""
    text = re.sub(r'>.*\n?', '', text)  # Remove quoted lines
    text = re.sub(r'\s+', ' ', text)    # Normalize whitespace
    return text.strip()

def send_reply(service, original_msg_id, response_text):
    """Send reply to the original thread"""
    message = {
        'raw': base64.urlsafe_b64encode(
            f"From: me\nTo: {TARGET_SENDER}\nSubject: Re: Your email\n\n{response_text}"
            .encode('utf-8')
        ).decode('utf-8')
    }
    service.users().messages().send(
        userId='me',
        body=message
    ).execute()