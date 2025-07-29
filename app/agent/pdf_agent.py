

# -------------------------------------

import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from app.tools.pdf_tool import parse_pdf as extract_pdf_text

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def parse_pdf(file_path: str) -> str:
    text = extract_pdf_text(file_path)
    print(f"\n[DEBUG] Extracted text from PDF ({file_path}):\n{text[:1000]}")  # log first 1000 chars
    text = text.strip()
    if len(text) > 2000:
        print("[DEBUG] Extracted text is too long, truncating to 2000 characters.")
        text = text[:2000] + "... [truncated]"
    return text

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7
)

tools = [Tool.from_function(parse_pdf,
        name="parse_pdf",
        description="Parse the text content from a PDF file")]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

def run_pdf_tool_agent(email_text: str, file_path: str):
    input_prompt = f"""
You received the following email: "{email_text}"
There is a PDF attached: {file_path}.
Please extract the full content from the PDF using the 'parse_pdf' tool,
and then provide a concise summary of the PDF contents to help respond to the email.
"""
    print("=== Input Prompt ===")
    print(input_prompt)
    print("=== File Path ===")
    print(file_path)
    print("=== Running agent.invoke() ===")

    # Invoke the agent
    result = agent.invoke({"input": input_prompt})

    print("=== Agent Result ===")
    print(result)

    # If the agent returns an 'output' key, also print that:
    if isinstance(result, dict) and 'output' in result:
        print("\n=== Agent Output Text ===")
        print(result['output'])

    return result
