from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()  # loads your GEMINI_API_KEY from .env

# Load Gemini model via LangChain
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Simple output parser
output_parser = StrOutputParser()

# Define prompt
decision_prompt = ChatPromptTemplate.from_template("""
You are an intelligent email assistant. Given the subject and body of an email,
decide whether the email can be automatically answered or should be escalated to a human.
Only respond with one of the following exact options:

- "HITL" (if a human should respond)
- "AUTO" (if you can respond on your own)

Subject: {subject}
Body: {body}
""")

# Create chain
decision_chain = decision_prompt | model | output_parser

def decide_hitl_or_auto(subject: str, body: str) -> str:
    """
    Decide if the email needs human-in-the-loop or can be auto-replied.
    Returns "HITL" or "AUTO"
    """
    try:
        result = decision_chain.invoke({"subject": subject, "body": body})
        return result.strip()
    except Exception as e:
        print(f"[ERROR] Decision engine failed: {e}")
        return "HITL"