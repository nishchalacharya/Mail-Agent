# from app.agent.decider_agent import decide_hitl_or_auto
# from app.agent.mail_agent import generate_email_reply
# from dotenv import load_dotenv
# import os

# load_dotenv()  # Load GEMINI_API_KEY

# # Dummy email samples
# test_emails = [
#     {
#         "sender": "employee@example.com",
#         "subject": "Request for Leave Tomorrow",
#         "body": "Hi, I won't be able to attend work tomorrow due to personal reasons. Please approve my leave. Thanks!"
#     },
#     {
#         "sender": "customer@example.com",
#         "subject": "Issue with Product Purchase",
#         "body": "Hey, I ordered your product last week and it arrived damaged. What can be done to resolve this issue?"
#     },
#     {
#         "sender": "newsletter@techupdates.com",
#         "subject": "Weekly Newsletter",
#         "body": "Welcome to our weekly roundup of tech news and product updates. No action is required from your side."
#     },
#     {
#         "sender": "colleague@example.com",
#         "subject": "Meeting Confirmation",
#         "body": "Just confirming the meeting scheduled for Friday at 3PM. Let me know if it needs to be rescheduled."
#     },
#     {
#         "sender": "researcher@example.com",
#         "subject": "Can you explain this paper?",
#         "body": "Hey, can you summarize the key contributions of the attention-is-all-you-need paper?"
#     }
# ]

# print("🔍 Testing Email Decider & Response Generator:\n")

# for i, email in enumerate(test_emails, 1):
#     decision = decide_hitl_or_auto(email['subject'], email['body'])
#     response = generate_email_reply(email['subject'], email['body'], decision, email['sender'])
    
#     print(f"--- Test Email {i} ---")
#     print(f"Subject : {email['subject']}")
#     print(f"Sender  : {email['sender']}")
#     print(f"Decision: {decision}")
#     print(f"Reply   : {response}\n")
    
    
    
    
 # -------------------------------------------------
 
 
 
 # test_pdf_agent.py

import os
from app.agent.pdf_agent import run_pdf_tool_agent

def test_pdf_agent():
    # Simulated email content
    subject = "Monthly Report"
    body = "Hi, I've attached the monthly sales report. Please review it."

    # Path to a test PDF file (ensure this exists)
    pdf_path = "app/test_file.pdf"

    if not os.path.exists(pdf_path):
        print(f"[ERROR] PDF file not found at {pdf_path}.")
        return

    # Combine subject and body for full context
    email_text = f"Subject: {subject}\nBody: {body}"

    print("=== Running PDF Tool Agent ===")
    output = run_pdf_tool_agent(email_text, pdf_path)

    print("\n=== Agent Output ===")
    print(output)

if __name__ == "__main__":
    test_pdf_agent()
