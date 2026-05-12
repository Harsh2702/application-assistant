from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from typing import TypedDict
from app.tools import scrape_job_posting, search_company_info, read_cv
from app.config import GROQ_API_KEY, GROQ_MODEL, CV_PATH
import os

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

llm = ChatGroq(model=GROQ_MODEL)

# full state that gets passed between nodes
class AgentState(TypedDict):
    job_url: str
    job_content: str
    company_name: str
    company_info: str
    cv_content: str
    report: str


def scrape_job_node(state: AgentState) -> AgentState:
    print(">> Scraping job posting...")
    result = scrape_job_posting(state["job_url"])
    return {"job_content": result["content"]}


def extract_company_node(state: AgentState) -> AgentState:
    print(">> Extracting company name...")
    prompt = f"""
    From this job posting text, extract only the company name.
    Return just the company name, nothing else.

    Job posting:
    {state["job_content"][:2000]}
    """
    response = llm.invoke(prompt)
    return {"company_name": response.content.strip()}


def research_company_node(state: AgentState) -> AgentState:
    print(f">> Researching {state['company_name']}...")
    info = search_company_info(state["company_name"])
    return {"company_info": info}


def read_cv_node(state: AgentState) -> AgentState:
    print(">> Reading CV...")
    cv = read_cv(CV_PATH)
    return {"cv_content": cv}


def analyze_match_node(state: AgentState) -> AgentState:
    print(">> Analyzing CV vs Job...")
    prompt = f"""
    You are a career coach. Analyze the fit between this CV and job posting.

    CV:
    {state["cv_content"][:3000]}

    Job Posting:
    {state["job_content"][:2000]}

    Company Info:
    {state["company_info"][:1000]}

    Write a report with these sections:
    1. Match Score (out of 10)
    2. What to Highlight in your application
    3. Skill Gaps to address
    4. Suggested Cover Letter angle
    5. One interesting fact about the company to mention in interview
    """
    response = llm.invoke(prompt)
    return {"report": response.content}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("scrape_job", scrape_job_node)
    graph.add_node("extract_company", extract_company_node)
    graph.add_node("research_company", research_company_node)
    graph.add_node("read_cv", read_cv_node)
    graph.add_node("analyze_match", analyze_match_node)

    graph.set_entry_point("scrape_job")
    graph.add_edge("scrape_job", "extract_company")
    graph.add_edge("extract_company", "research_company")
    graph.add_edge("research_company", "read_cv")
    graph.add_edge("read_cv", "analyze_match")
    graph.add_edge("analyze_match", END)

    return graph.compile()