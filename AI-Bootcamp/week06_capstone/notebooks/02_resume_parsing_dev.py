import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import sys
    sys.path.insert(0, "../app")  # import the capstone modules
    return mo, sys


@app.cell
def __(mo):
    mo.md(
        r"""
        # 02. Resume Parsing — Development Notebook

        Develop and test the resume parsing + skill-gap logic that backs the capstone
        (`app/resume_parser.py`). This is the deterministic, offline foundation the LLM layer
        builds on.
        """
    )
    return


@app.cell
def __():
    from resume_parser import extract_skills, skill_gap

    resume = """
    Jane Doe — Data Analyst
    Skills: Python, Pandas, SQL, Excel, Tableau. Built dashboards and ran A/B tests.
    Some exposure to machine learning with scikit-learn.
    """
    skills = extract_skills(resume)
    print("Extracted skills:", skills)
    return extract_skills, resume, skill_gap, skills


@app.cell
def __(skill_gap, skills):
    job = """
    AI Engineer — required: Python, PyTorch, Docker, AWS, RAG, LLM, prompt engineering.
    """
    from resume_parser import extract_skills as _es

    job_skills = _es(job)
    gap = skill_gap(skills, job_skills)
    print("Job skills:", job_skills)
    print("Coverage:", gap["coverage"])
    print("Missing:", gap["missing"])
    print("Matched:", gap["matched"])
    return gap, job, job_skills


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Exercises
        1. Extend `KNOWN_SKILLS` in `app/resume_parser.py` with 10 more skills relevant to your
           target role and re-run extraction.
        2. Add a PDF resume (`extract_text` supports PDFs via pypdf) and confirm skills extract.
        3. Improve `skill_gap` to weight "must-have" vs "nice-to-have" skills differently.

        ## Notes
        - Keyword extraction is fast and explainable but misses synonyms ("ML" vs "machine
          learning"). The LLM layer (`analyze_resume`) covers nuance; the deterministic layer
          gives reliable, testable structure.
        - Keep this layer pure (no network) so `test_app.py` runs offline in CI.
        """
    )
    return


if __name__ == "__main__":
    app.run()
