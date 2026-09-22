"""
KPI metrics card module for CDC Natality 2025 Streamlit Dashboard.
Calculates and presents summary metrics for active data selections.
"""

import pandas as pd
import streamlit as st


def render_kpi_cards(filtered_df: pd.DataFrame, full_df: pd.DataFrame):
    """Calculate and display 5 key performance indicator (KPI) cards."""
    if filtered_df.empty:
        st.warning("⚠️ No data available for the current filter criteria. Please adjust your sidebar selections.")
        return

    # Total births in current selection
    total_selected_births = filtered_df['Births'].sum()
    total_national_births = full_df['Births'].sum()
    pct_national = (total_selected_births / total_national_births) * 100

    # Geography metric
    num_selected_states = filtered_df['State of Residence'].nunique()
    total_states = full_df['State of Residence'].nunique()

    # Average births per selected month
    num_selected_months = filtered_df['Month'].nunique()
    avg_monthly_births = total_selected_births / num_selected_months if num_selected_months > 0 else 0

    # Top geography in selection
    state_totals = filtered_df.groupby('State of Residence', observed=True)['Births'].sum()
    if not state_totals.empty:
        top_state_name = state_totals.idxmax()
        top_state_count = state_totals.max()
        top_state_delta = f"{top_state_count:,} births"
    else:
        top_state_name = "N/A"
        top_state_delta = "0 births"

    # Peak month in selection
    month_totals = filtered_df.groupby('Month', observed=True)['Births'].sum()
    if not month_totals.empty:
        top_month_name = str(month_totals.idxmax())
        top_month_count = month_totals.max()
        top_month_delta = f"{top_month_count:,} births"
    else:
        top_month_name = "N/A"
        top_month_delta = "0 births"

    # Render KPI Cards in a 5-column layout
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Total Birth Count",
            value=f"{total_selected_births:,}",
            delta=f"{pct_national:.1f}% of 2025 Data",
            help="Total live births recorded across the active filter criteria."
        )

    with col2:
        st.metric(
            label="Selected Geographies",
            value=f"{num_selected_states} / {total_states}",
            delta=f"{num_selected_states/total_states:.0%} Coverage",
            help="Number of U.S. states and territories included in current view."
        )

    with col3:
        st.metric(
            label="Avg Births / Month",
            value=f"{int(avg_monthly_births):,}",
            delta=f"Across {num_selected_months} Month(s)",
            help="Average monthly birth volume across selected months."
        )

    with col4:
        st.metric(
            label="Top Geography",
            value=top_state_name,
            delta=top_state_delta,
            help="State or geography with the largest birth count in current selection."
        )

    with col5:
        st.metric(
            label="Peak Month",
            value=top_month_name,
            delta=top_month_delta,
            help="Month with the highest accumulated birth count in current selection."
        )
