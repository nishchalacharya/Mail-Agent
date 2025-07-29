from utils.gmail_utils import authenticate_gmail, get_unread_messages, extract_email_content, send_reply
from agent.decider_agent import decide_hitl_or_auto
from agent.mail_agent import generate_email_reply
import time

def main():
    service = authenticate_gmail()

    while True:
        print("Checking for new messages...")
        messages = get_unread_messages(service)

        for msg in messages:
            email_data = extract_email_content(service, msg['id'])
            print(f"Received email from: {email_data['sender']} | Subject: {email_data['subject']}")

            # Use decider agent
            decision = decide_hitl_or_auto(email_data['subject'], email_data['body'])
            print(f"Decision: {decision}")

            # Use mail agent to generate reply based on decision
            reply_text = generate_email_reply(
                email_data['subject'],
                email_data['body'],
                decision,
                email_data['sender']
            )
            print(f"Reply: {reply_text}")

            # Send the reply
            send_reply(service, email_data['message_id'], reply_text)
            print("Replied to the email.\n")

        print("Sleeping for 60 seconds...\n")
        time.sleep(60)

if __name__ == "__main__":
    main()
