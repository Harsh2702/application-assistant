from app.graph import build_graph
from app.memory import init_db, save_research, load_research, list_all_research
from app.report import save_report

init_db()

print("\nPreviously researched jobs:")
history = list_all_research()
if history:
    for row in history:
        print(f"  - {row[1]} | {row[0][:60]}... | {row[2]}")
else:
    print("  None yet.")

job_url = input("\nPaste job URL: ")

existing = load_research(job_url)
if existing:
    print(f"\n>> Found in memory! Loading saved research for {existing['company_name']}...")
    print("\n========== JOB REPORT (from memory) ==========\n")
    print(f"Company: {existing['company_name']}")
    print(f"\n{existing['report']}")
    save_report(existing["company_name"], existing["report"], job_url)
else:
    app = build_graph()
    result = app.invoke({
        "job_url": job_url,
        "job_content": "",
        "company_name": "",
        "company_info": "",
        "cv_content": "",
        "report": ""
    })

    save_research(
        job_url=job_url,
        company_name=result["company_name"],
        company_info=result["company_info"],
        job_content=result["job_content"],
        report=result["report"]
    )

    save_report(result["company_name"], result["report"], job_url)

    print("\n========== JOB REPORT ==========\n")
    print(f"Company: {result['company_name']}")
    print(f"\n{result['report']}")