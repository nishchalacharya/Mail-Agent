from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

# Load Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Output parser
parser = StrOutputParser()

# Context-aware reply prompt
reply_prompt = ChatPromptTemplate.from_template("""
You are an AI email assistant.

Your job is to write a professional email **reply** to an incoming message based on its content and context.

You will be given:
- The original sender's name (if available).
- The subject and body of the email.
- A `decision` label, which is either `AUTO` or `HITL`.

Respond as follows:

---

If the `decision` is **AUTO**:
- Write a context-aware, relevant, and helpful reply.
- Maintain a polite and professional tone.
- Keep it brief and to the point.
- If the email is a confirmation, acknowledgment, or update, respond accordingly.

If the `decision` is **HITL**:
- Respond with a neutral, friendly acknowledgment.
- Indicate that the message has been received and someone will get back to them soon.
- Do **not** attempt to solve or respond to the actual content.

---

Examples:

🟢 AUTO Case:
Subject: "Meeting Confirmation"  
Body: "Just confirming our meeting this Friday at 3PM."  
Decision: AUTO  
Reply: "Thank you for confirming. Looking forward to our meeting on Friday at 3PM."

🟠 HITL Case:
Subject: "Need help understanding this legal clause"  
Body: "Can you help interpret this section from the NDA?"  
Decision: HITL  
Reply: "Thanks for reaching out. Your message has been received, and someone from our team will get back to you shortly."

---

Now write the reply:
Sender Name: {sender}
Subject: {subject}
Body: {body}
Decision: {decision}
""")

reply_chain = reply_prompt | model | parser

# HITL fallback reply
HITL_GENERIC_RESPONSE = (
    "Thank you for reaching out. Your message has been forwarded to the concerned team. "
    "We’ll get back to you as soon as possible."
)

def generate_email_reply(subject: str, body: str, decision: str, sender: str) -> str:
    """
    Generates a reply email based on decision type.
    If 'AUTO', uses Gemini to generate context-aware response.
    If 'HITL', returns a generic fallback message.
    """
    if decision == "AUTO":
        try:
            return reply_chain.invoke({"subject": subject, "body": body, "sender": sender, "decision": decision}).strip()
        except Exception as e:
            print(f"[ERROR] Gemini auto-reply failed: {e}")
            return HITL_GENERIC_RESPONSE
    else:
        return HITL_GENERIC_RESPONSE
