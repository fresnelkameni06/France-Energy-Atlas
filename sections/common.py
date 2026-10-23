"""Narrative UI helpers shared across the pages."""
import streamlit as st


def heading(question, takeaway=None):
    st.markdown(f"#### {question}")
    if takeaway:
        st.caption(takeaway)


def note(text):
    st.info(text, icon="💡")


def limitations(text):
    st.caption(f"**Interpretation caution:** {text}")


def empty(df):
    if df is None or df.empty:
        st.warning("No observations match the current selection. Try another year, date range or region.")
        return True
    return False
