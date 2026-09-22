"""
CDC Natality 2025 Streamlit Dashboard Main Entrypoint.
Designed for undergraduate business analytics students to explore provisional U.S. live birth count data.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_data
from src.filters import render_sidebar_filters
from src.kpis import render_kpi_cards
from src.charts import (
    plot_monthly_trend,
    plot_sex_comparison,
    plot_state_ranking,
    plot_choropleth_map,
    plot_state_month_heatmap,
    plot_top_bottom_comparison
)

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="CDC Natality 2025 Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for visual polish and clean typography
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1rem;
    }
    .stAlert {
        border-radius: 8px;
    }
    .metric-card-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def render_header():
    """Render main header, CDC source attribution, and metric notice banners."""
    st.markdown('<div class="main-title">👶 Provisional 2025 CDC Natality Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">An interactive data exploration tool for business analytics students studying U.S. birth patterns.</div>',
        unsafe_allow_html=True
    )

    # Required Banners: CDC attribution, Provisional status, Birth Count Notice
    col_info1, col_info2 = st.columns([3, 2])

    with col_info1:
        st.info(
            "🏛️ **Data Source & Attribution:** Official provisional 2025 natality data published by the "
            "**Centers for Disease Control and Prevention (CDC)** / National Center for Health Statistics (NCHS)."
        )

    with col_info2:
        st.warning(
            "⚠️ **Analytical Notice (Counts vs. Rates):** All figures represent **absolute live birth counts**, "
            "not birth rates. Birth counts reflect population size and total volume rather than per-capita fertility rates."
        )


def main():
    # 1. Load Data with Cached Ingestion & Audit Checks
    try:
        full_df = load_data()
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        st.stop()

    # 2. Render Main Header
    render_header()
    st.divider()

    # 3. Render Sidebar Filters & Obtain Filtered Data Subset
    filtered_df = render_sidebar_filters(full_df)

    # 4. Render Top KPI Metric Cards
    render_kpi_cards(filtered_df, full_df)
    st.divider()

    # 5. Check if Filtered Data is Empty
    if filtered_df.empty:
        st.error("🚫 No data matches your active filter selection. Please use the sidebar to select at least one State and Month.")
        st.stop()

    # 6. Tabbed Dashboard Navigation
    tab_overview, tab_geo, tab_time_sex, tab_table, tab_about = st.tabs([
        "📊 Overview",
        "🗺️ Geographic Analysis",
        "📈 Monthly & Sex Trends",
        "📋 Data Table & Download",
        "ℹ️ About the Data"
    ])

    # --- TAB 1: OVERVIEW ---
    with tab_overview:
        st.markdown("### 📊 Executive Summary & Key Visual Trends")
        st.markdown(
            "This tab provides a high-level overview of live birth counts across 2025. "
            "Use the charts below to analyze national seasonal patterns and infant sex distributions."
        )

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            fig_trend = plot_monthly_trend(filtered_df)
            if fig_trend:
                st.plotly_chart(fig_trend, use_container_width=True)

        with col_chart2:
            fig_sex = plot_sex_comparison(filtered_df)
            if fig_sex:
                st.plotly_chart(fig_sex, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 💡 Student Analytics Insight")
        st.markdown(
            "- **Biological Sex Ratio:** Nationally, male live birth counts consistently exceed female live birth counts by approximately **5%** "
            "(a natural biological sex ratio at birth of ~105 male births per 100 female births).\n"
            "- **Seasonality Pattern:** U.S. live birth counts typically peak during late summer and early autumn (July–September), "
            "reflecting well-documented annual conception trends."
        )

    # --- TAB 2: GEOGRAPHIC ANALYSIS ---
    with tab_geo:
        st.markdown("### 🗺️ Geographic Distribution & State Rankings")
        st.markdown(
            "Explore spatial differences across the 50 U.S. states and District of Columbia. "
            "Notice how total birth counts closely align with state population sizes."
        )

        # Choropleth Map
        fig_map = plot_choropleth_map(filtered_df)
        if fig_map:
            st.plotly_chart(fig_map, use_container_width=True)

        st.divider()

        col_rank, col_disparity = st.columns([3, 2])

        with col_rank:
            num_selected_states = filtered_df['State of Residence'].nunique()
            top_n = st.slider(
                "Number of states to show in ranking chart:",
                min_value=min(5, num_selected_states),
                max_value=max(5, num_selected_states),
                value=min(20, num_selected_states),
                step=1
            )
            fig_rank = plot_state_ranking(filtered_df, top_n=top_n)
            if fig_rank:
                st.plotly_chart(fig_rank, use_container_width=True)

        with col_disparity:
            fig_top_bottom = plot_top_bottom_comparison(filtered_df)
            if fig_top_bottom:
                st.plotly_chart(fig_top_bottom, use_container_width=True)

    # --- TAB 3: MONTHLY & SEX TRENDS ---
    with tab_time_sex:
        st.markdown("### 📈 Detailed Monthly Density & Heatmap Analysis")
        st.markdown(
            "Analyze month-by-month state activity using the density heatmap below. "
            "Darker blue shading represents higher monthly birth volume."
        )

        fig_heatmap = plot_state_month_heatmap(filtered_df)
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)

        st.divider()
        st.markdown("#### 📊 State Monthly Distribution Variance")
        
        # Monthly distribution boxplot
        fig_box = px.box(
            filtered_df,
            x='Month',
            y='Births',
            color='Sex of Infant',
            title="<b>Monthly Birth Count Distribution Across Geographies</b>",
            labels={'Month': 'Month', 'Births': 'Monthly Live Birth Count per State'},
            color_discrete_map={'Female': '#D55E00', 'Male': '#0072B2'}
        )
        fig_box.update_layout(yaxis=dict(rangemode="tozero"))
        st.plotly_chart(fig_box, use_container_width=True)

    # --- TAB 4: DATA TABLE & DOWNLOAD ---
    with tab_table:
        st.markdown("### 📋 Filtered Data Table & CSV Export")
        st.markdown(
            "Review the exact dataset matching your current sidebar filters. "
            "You can sort by any column, search for specific states, or download the data as CSV for further analysis in Excel or Python."
        )

        # Summary metadata for student audit
        st.caption(f"Displaying **{len(filtered_df):,}** observations with total birth count of **{filtered_df['Births'].sum():,}**.")

        # Reorder and format columns for student viewing
        display_df = filtered_df[['State of Residence', 'State Code', 'Year Code', 'Month Code', 'Month', 'Sex of Infant', 'Births']].copy()
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Births": st.column_config.NumberColumn("Live Birth Count", format="%d"),
                "Month Code": st.column_config.NumberColumn("Month Code", format="%d"),
                "Year Code": st.column_config.NumberColumn("Year", format="%d"),
                "State Code": st.column_config.TextColumn("USPS Code")
            }
        )

        # CSV Download Button
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Subset as CSV",
            data=csv_data,
            file_name="cdc_provisional_natality_2025_filtered.csv",
            mime="text/csv",
            type="primary"
        )

    # --- TAB 5: ABOUT THE DATA ---
    with tab_about:
        st.markdown("### ℹ️ About the Provisional 2025 CDC Natality Dataset")
        
        st.markdown(r"""
        #### 1. Data Source & Background
        This dataset contains provisional live birth count data for the calendar year **2025**, compiled by the 
        **National Center for Health Statistics (NCHS)** at the **Centers for Disease Control and Prevention (CDC)**.
        
        #### 2. Key Business Analytics Concepts
        - **Counts vs. Rates:** This dataset reports **absolute birth counts** (\(N\)). It does *not* report crude birth rates or general fertility rates (which require population denominator data).
        - **Factorial Structure:** The dataset comprises exactly \(51 \text{ geographies} \times 12 \text{ months} \times 2 \text{ infant sexes} = 1,224 \text{ observations}\).
        - **Provisional Status:** Provisional data are subject to minor revisions as state vital statistics registries complete final birth record reconciliations.

        #### 3. Data Dictionary
        | Field Name | Type | Description |
        | :--- | :--- | :--- |
        | `State of Residence` | Categorical | U.S. State or District of Columbia where the mother resided |
        | `State Code` | Categorical | 2-letter USPS postal abbreviation |
        | `Year Code` | Discrete Numerical | Reporting year (`2025`) |
        | `Month Code` | Ordinal | Chronological month number (`1` to `12`) |
        | `Month` | Categorical | Full calendar month name |
        | `Sex of Infant` | Categorical | Registered biological sex of infant (`Female`, `Male`) |
        | `Births` | Quantitative | Absolute count of registered live births |

        #### 4. Student Practice & Reflection Questions
        1. *Why do populous states like California, Texas, and Florida dominate total birth counts regardless of month?*
        2. *Calculate the male-to-female sex ratio for your home state. Is it close to the national ratio of ~1.05?*
        3. *Why is it important not to confuse state birth counts with state birth rates when analyzing family planning policies?*
        """)

    # Footer
    st.divider()
    st.caption("CDC Natality 2025 Dashboard | Built for Business Analytics Education | Powered by Streamlit & Plotly")


if __name__ == "__main__":
    main()
