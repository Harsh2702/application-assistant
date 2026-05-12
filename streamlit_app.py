import streamlit as st
from app.graph import build_graph
from app.memory import init_db, save_research, load_research, list_all_research
from app.report import save_report

init_db()

st.set_page_config(page_title="Job Research Agent", page_icon="🤖")
st.title("Job Application Research Agent")
st.caption("Paste a job URL and get a full research report instantly.")

# sidebar: past research
with st.sidebar:
    st.header("Previously Researched Jobs")
    history = list_all_research()
    if history:
        for row in history:
            st.markdown(f"**{row[1]}**")
            st.caption(f"{row[2]}")
    else:
        st.info("No research saved yet.")

# main input
job_url = st.text_input("Paste Job URL here")

if st.button("Research this Job"):
    if not job_url.strip():
        st.warning("Please paste a job URL first.")
    else:
        existing = load_research(job_url)

        if existing:
            st.success(f"Found in memory! Loaded saved research for {existing['company_name']}")
            st.markdown(f"## {existing['company_name']}")
            st.markdown(existing["report"])
            save_report(existing["company_name"], existing["report"], job_url)

        else:
            with st.spinner("Researching... this takes about 30 seconds"):
                try:
                    agent = build_graph()
                    result = agent.invoke({
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

                    filepath = save_report(
                        result["company_name"],
                        result["report"],
                        job_url
                    )

                    st.success(f"Done! Research saved for {result['company_name']}")
                    st.markdown(f"## {result['company_name']}")
                    st.markdown(result["report"])

                    # download button
                    with open(filepath, "r", encoding="utf-8") as f:
                        st.download_button(
                            label="Download Report as Markdown",
                            data=f.read(),
                            file_name=f"{result['company_name']}_report.md",
                            mime="text/markdown"
                        )

                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")