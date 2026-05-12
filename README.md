# Job-Application-Assistant

An AI agent that researches any job posting and matches it against your CV.

## What it does
- Scrapes the job posting from any URL
- Extracts the company name automatically
- Researches the company using web search
- Reads your CV and compares it against the job
- Generates a report with match score, what to highlight, skill gaps and cover letter angle
- Saves all research locally so it never repeats work for the same job

## Tech Stack
- LangGraph for the agent graph
- Groq (llama3-70b) as the LLM
- Tavily for web search
- SQLite for long term memory
- Streamlit for the UI

## Setup
0. Sign up to get your both apis first
Groq API: https://console.groq.com
Tavily API: https://tavily.com

1. Clone the repo
2. Create a virtual env and install dependencies
```bash
    pip install -r requirements.txt
```
3. Create a `.env` file

GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key

4. Add your CV as `cv.pdf` in the root folder

5. Run the app
```bash
    streamlit run streamlit_app.py
```

## Project Structure
    job-application-assistant/
      app/
        config.py
        tools.py
        graph.py
        memory.py
        report.py
      streamlit_app.py
      main.py
      requirements.txt
      .env
