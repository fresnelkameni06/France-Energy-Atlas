import streamlit as st
from sections.common import heading


def render(ctx):
    st.subheader("01 / The Big Question")
    heading("How did electricity demand and regional generation patterns change in France from 2020 to 2026?")
    st.markdown("""**Our challenge:** identify **when** demand is highest, **where** regional differences emerge, and **how** the generation mix evolves—without confusing correlation with causation.

    **Audience:** energy analysts, citizens, students and decision-makers.

    **Story arc:** Why it matters → historical context → regional contrasts → energy sources → rhythms and relationships → limitations → evidence-based next steps.

    **Research questions:**
    - Which regions report the highest demand, and during which periods?
    - How has the mix of electricity generation evolved?
    - Are hourly, weekly and seasonal patterns stable?
    - What can observations support—and what can they *not* prove?
    """)
    st.success("The charts are built from the 2020–2026 Excel workbook and reproducible prepared datasets. No API calls are made from this dashboard.")
