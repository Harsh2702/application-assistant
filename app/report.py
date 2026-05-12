import os
from app.config import REPORTS_DIR
from datetime import datetime

def save_report(company_name: str, report: str, job_url: str):
    """Save report as a txt file."""
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # clean company name for use as filename
    clean_name = company_name.strip().replace(" ", "_").replace("/", "-")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{clean_name}_{timestamp}.txt"
    filepath = os.path.join(REPORTS_DIR, filename)

    content = f"""# Job Research Report
**Company:** {company_name}
**Job URL:** {job_url}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

{report}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f">> Report saved to {filepath}")
    return filepath