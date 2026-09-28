import pandas as pd
import streamlit as st


def format_currency(value):
    """Format a number as Indian Rupees."""
    if pd.isna(value):
        return "₹0.00"

    return f"₹{value:,.2f}"


def format_number(value):
    """Format a number with comma separators."""
    if pd.isna(value):
        return "0"

    return f"{int(value):,}"


def show_dataframe(df):
    """Display a dataframe in Streamlit."""
    if df is not None and not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No data available.")


def show_kpi(label, value):
    """Display a KPI metric."""
    st.metric(
        label=label,
        value=value
    )
