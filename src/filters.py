"""
Sidebar filters module for CDC Natality 2025 Streamlit Dashboard.
Provides interactive controls for state, month, and infant sex selection with session state handling.
"""

import pandas as pd
import streamlit as st
from src.data_loader import MONTH_ORDER, US_STATE_ABBR


def init_filter_state(df: pd.DataFrame):
    """Initialize default filter selections in Streamlit session state."""
    all_states = sorted(df['State of Residence'].unique().tolist())
    all_months = MONTH_ORDER
    
    if 'selected_states' not in st.session_state:
        st.session_state.selected_states = all_states
    if 'selected_months' not in st.session_state:
        st.session_state.selected_months = all_months
    if 'selected_sex' not in st.session_state:
        st.session_state.selected_sex = 'All'


def reset_filters(df: pd.DataFrame):
    """Reset all filters back to full dataset defaults."""
    st.session_state.selected_states = sorted(df['State of Residence'].unique().tolist())
    st.session_state.selected_months = MONTH_ORDER
    st.session_state.selected_sex = 'All'


def render_sidebar_filters(df: pd.DataFrame):
    """Render the sidebar filter UI controls and return the filtered dataframe subset."""
    init_filter_state(df)
    
    all_states = sorted(df['State of Residence'].unique().tolist())
    all_months = MONTH_ORDER
    
    st.sidebar.markdown("### 🎛️ Filter Controls")
    
    # --- Reset Button ---
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True, type="secondary"):
        reset_filters(df)
        st.rerun()

    st.sidebar.divider()

    # --- 1. Geography Filter ---
    st.sidebar.markdown("#### 📍 Geography")
    col_state_btn1, col_state_btn2 = st.sidebar.columns(2)
    if col_state_btn1.button("Select All", key="btn_all_states", use_container_width=True):
        st.session_state.selected_states = all_states
        st.rerun()
    if col_state_btn2.button("Clear All", key="btn_clear_states", use_container_width=True):
        st.session_state.selected_states = []
        st.rerun()

    selected_states = st.sidebar.multiselect(
        "Select States / Geographies:",
        options=all_states,
        default=st.session_state.selected_states,
        key="ms_states",
        help="Choose one or more of the 50 US States + District of Columbia"
    )
    # Sync multiselect return to session state
    st.session_state.selected_states = selected_states

    # --- 2. Month Filter ---
    st.sidebar.markdown("#### 📅 Time Period (Month)")
    col_month_btn1, col_month_btn2 = st.sidebar.columns(2)
    if col_month_btn1.button("Select All", key="btn_all_months", use_container_width=True):
        st.session_state.selected_months = all_months
        st.rerun()
    if col_month_btn2.button("Clear All", key="btn_clear_months", use_container_width=True):
        st.session_state.selected_months = []
        st.rerun()

    selected_months = st.sidebar.multiselect(
        "Select Months:",
        options=all_months,
        default=st.session_state.selected_months,
        key="ms_months",
        help="Select specific months (ordered chronologically January through December)"
    )
    st.session_state.selected_months = selected_months

    # --- 3. Infant Sex Filter ---
    st.sidebar.markdown("#### 👶 Infant Sex")
    selected_sex = st.sidebar.radio(
        "Select Category:",
        options=['All', 'Female', 'Male'],
        index=['All', 'Female', 'Male'].index(st.session_state.selected_sex),
        key="radio_sex",
        horizontal=True,
        help="Filter data by Female, Male, or combined Total"
    )
    st.session_state.selected_sex = selected_sex

    st.sidebar.divider()

    # --- Filter Summary Badge ---
    st.sidebar.markdown("#### 📋 Active Filter Summary")
    num_states = len(st.session_state.selected_states)
    num_months = len(st.session_state.selected_months)
    sex_label = st.session_state.selected_sex

    st.sidebar.info(
        f"• **Geographies:** {num_states} of {len(all_states)} selected\n"
        f"• **Months:** {num_months} of {len(all_months)} selected\n"
        f"• **Infant Sex:** {sex_label}"
    )

    # --- Filter Application Logic ---
    filtered_df = df.copy()

    if selected_states:
        filtered_df = filtered_df[filtered_df['State of Residence'].isin(selected_states)]
    else:
        filtered_df = filtered_df.iloc[0:0]  # Empty dataframe if zero states selected

    if selected_months:
        filtered_df = filtered_df[filtered_df['Month'].isin(selected_months)]
    else:
        filtered_df = filtered_df.iloc[0:0]  # Empty dataframe if zero months selected

    if selected_sex != 'All':
        filtered_df = filtered_df[filtered_df['Sex of Infant'] == selected_sex]

    return filtered_df
