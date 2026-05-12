import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
CV_PATH = "D:/Job doc/DS/HarshJoshi_DS_Resume.pdf"
REPORTS_DIR = "reports"
