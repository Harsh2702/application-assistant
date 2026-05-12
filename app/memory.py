import sqlite3
import json
import os

DB_PATH = "job_agent.db"

def init_db():
    """Create the database and table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_research (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_url TEXT UNIQUE,
            company_name TEXT,
            company_info TEXT,
            job_content TEXT,
            report TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_research(job_url: str, company_name: str, company_info: str,
                  job_content: str, report: str):
    """Save a completed research result to DB."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO job_research 
        (job_url, company_name, company_info, job_content, report)
        VALUES (?, ?, ?, ?, ?)
    """, (job_url, company_name, company_info, job_content, report))
    conn.commit()
    conn.close()
    print(">> Research saved to memory.")


def load_research(job_url: str) -> dict | None:
    """Check if this job URL was already researched."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT company_name, company_info, job_content, report
        FROM job_research WHERE job_url = ?
    """, (job_url,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "company_name": row[0],
            "company_info": row[1],
            "job_content": row[2],
            "report": row[3]
        }
    return None


def list_all_research() -> list:
    """Return all saved jobs for review."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT job_url, company_name, created_at FROM job_research
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows