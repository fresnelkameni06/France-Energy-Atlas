
"""Chapter 14 — Student and Project Credits."""

from pathlib import Path
import tomllib
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]


def render(ctx):
    st.header("14 · Student & Project Credits")

    with open(ROOT / "config" / "profile.toml", "rb") as file:
        profile = tomllib.load(file)

    student = profile.get("student", {})
    course = profile.get("course", {})
    project = profile.get("project", {})

    st.image(str(ROOT / "assets" / "efrei.webp"), width=300)

    st.subheader(project.get("title", "France Energy Atlas"))

    st.markdown("### Student Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Full Name:**", student.get("full_name", ""))
        st.write("**Program:**", student.get("program", ""))
        st.write("**Academic Year:**", student.get("year", ""))

    with col2:
        st.write("**Email:**", student.get("email", ""))
        st.write("**LinkedIn:**", student.get("linkedin", ""))
        st.write("**Portfolio:**", student.get("portfolio", ""))
        st.write("**GitHub:**", student.get("github", ""))

    st.divider()

    st.markdown("### Course Information")

    st.write("**Course Name:**", course.get("name", ""))
    st.write(
        "**Project Proposed By:**",
        course.get("project_proposed_by", "")
    )
    st.write(
        "**Professor Contact:**",
        course.get("professor_linkedin_or_email", "")
    )
