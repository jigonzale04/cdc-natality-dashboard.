"""
Plotly visualizations module for CDC Natality 2025 Streamlit Dashboard.
Includes accessible, publication-ready interactive charts for analytics students.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Accessible, high-contrast color palette
COLOR_MALE = "#0072B2"      # Accessible Deep Blue
COLOR_FEMALE = "#D55E00"    # Accessible Vermillion / Orange
COLOR_PRIMARY = "#2B5C8F"   # Primary Navy
COLOR_SECONDARY = "#009E73" # Accessible Green


def plot_monthly_trend(df: pd.DataFrame) -> go.Figure:
    """Line chart showing monthly birth count trends chronologically (Jan - Dec)."""
    if df.empty:
        return None

    # Group by Month and Sex of Infant
    trend_data = (
        df.groupby(['Month', 'Sex of Infant'], observed=True)['Births']
        .sum()
        .reset_index()
    )

    fig = px.line(
        trend_data,
        x='Month',
        y='Births',
        color='Sex of Infant',
        markers=True,
        title="<b>Monthly Live Birth Count Trend (2025)</b>",
        labels={'Month': 'Month', 'Births': 'Live Birth Count', 'Sex of Infant': 'Infant Sex'},
        color_discrete_map={'Female': COLOR_FEMALE, 'Male': COLOR_MALE}
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Infant Sex: %{fullData.name}<br>Births: <b>%{y:,}</b><extra></extra>",
        line=dict(width=3),
        marker=dict(size=8)
    )

    fig.update_layout(
        xaxis=dict(type='category', title="Month (Chronological)"),
        yaxis=dict(title="Live Birth Count", rangemode="tozero"),
        legend_title_text="Infant Sex",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig


def plot_sex_comparison(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart comparing total live births by infant sex per month."""
    if df.empty:
        return None

    sex_data = (
        df.groupby(['Month', 'Sex of Infant'], observed=True)['Births']
        .sum()
        .reset_index()
    )

    fig = px.bar(
        sex_data,
        x='Month',
        y='Births',
        color='Sex of Infant',
        barmode='group',
        title="<b>Infant Sex Comparison by Month</b>",
        labels={'Month': 'Month', 'Births': 'Live Birth Count', 'Sex of Infant': 'Infant Sex'},
        color_discrete_map={'Female': COLOR_FEMALE, 'Male': COLOR_MALE}
    )

    # Calculate max y value for non-truncated axis
    max_births = sex_data['Births'].max() if not sex_data.empty else 1000

    fig.update_traces(
        hovertemplate="<b>%{x}</b> (%{fullData.name})<br>Births: <b>%{y:,}</b><extra></extra>"
    )

    fig.update_layout(
        yaxis=dict(title="Live Birth Count", range=[0, max_births * 1.15]),
        xaxis=dict(type='category'),
        legend_title_text="Infant Sex",
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig


def plot_state_ranking(df: pd.DataFrame, top_n: int = 51) -> go.Figure:
    """Horizontal bar chart ranking selected geographies by total birth count."""
    if df.empty:
        return None

    state_totals = (
        df.groupby(['State of Residence', 'State Code'], observed=True)['Births']
        .sum()
        .reset_index()
        .sort_values(by='Births', ascending=True)
    )

    if top_n < len(state_totals):
        state_totals = state_totals.tail(top_n)

    fig = px.bar(
        state_totals,
        x='Births',
        y='State of Residence',
        orientation='h',
        title=f"<b>Geographic Live Birth Ranking (Top {len(state_totals)} Selected)</b>",
        labels={'State of Residence': 'Geography', 'Births': 'Total Live Births'},
        color='Births',
        color_continuous_scale='Blues'
    )

    max_val = state_totals['Births'].max() if not state_totals.empty else 1000

    fig.update_traces(
        hovertemplate="<b>%{y}</b> (%{customdata[0]})<br>Total Births: <b>%{x:,}</b><extra></extra>",
        customdata=state_totals[['State Code']]
    )

    fig.update_layout(
        xaxis=dict(title="Total Live Births", range=[0, max_val * 1.12]),
        yaxis=dict(title="", categoryorder='total ascending'),
        coloraxis_showscale=False,
        height=max(400, len(state_totals) * 22),
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig


def plot_choropleth_map(df: pd.DataFrame) -> go.Figure:
    """Interactive Plotly US Choropleth map of birth counts by state."""
    if df.empty:
        return None

    map_data = (
        df.groupby(['State of Residence', 'State Code'], observed=True)['Births']
        .sum()
        .reset_index()
    )

    fig = px.choropleth(
        map_data,
        locations='State Code',
        locationmode="USA-states",
        color='Births',
        scope="usa",
        color_continuous_scale="Viridis",
        title="<b>U.S. Geographic Live Birth Volume Distribution (2025)</b>",
        hover_name='State of Residence',
        hover_data={'State Code': False, 'Births': ':,d'}
    )

    fig.update_layout(
        geo=dict(
            lakecolor='rgb(255, 255, 255)',
            showlakes=True,
            projection_type='albers usa'
        ),
        margin=dict(l=10, r=10, t=50, b=10),
        coloraxis_colorbar=dict(
            title="Total Births",
            tickformat=",d"
        )
    )

    return fig


def plot_state_month_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap showing state-by-month birth count density."""
    if df.empty:
        return None

    # Pivot dataset: States as rows, Months as columns
    pivot_df = df.pivot_table(
        index='State of Residence',
        columns='Month',
        values='Births',
        aggfunc='sum',
        observed=True
    ).fillna(0)

    fig = px.imshow(
        pivot_df,
        labels=dict(x="Month", y="Geography", color="Births"),
        x=pivot_df.columns.tolist(),
        y=pivot_df.index.tolist(),
        color_continuous_scale="Blues",
        aspect="auto",
        title="<b>State-by-Month Live Birth Density Heatmap</b>"
    )

    fig.update_traces(
        hovertemplate="State: <b>%{y}</b><br>Month: <b>%{x}</b><br>Births: <b>%{z:,}</b><extra></extra>"
    )

    fig.update_layout(
        xaxis=dict(side="top"),
        height=max(500, len(pivot_df) * 18),
        margin=dict(l=40, r=40, t=80, b=40)
    )

    return fig


def plot_top_bottom_comparison(df: pd.DataFrame) -> go.Figure:
    """Side-by-side comparison chart of Top 5 vs. Bottom 5 geographies by birth count."""
    if df.empty:
        return None

    state_totals = (
        df.groupby('State of Residence', observed=True)['Births']
        .sum()
        .reset_index()
        .sort_values(by='Births', ascending=False)
    )

    if len(state_totals) < 10:
        # If fewer than 10 states selected, show simple bar chart
        top_bottom_df = state_totals.copy()
        top_bottom_df['Group'] = 'Selected Geographies'
    else:
        top_5 = state_totals.head(5).copy()
        top_5['Group'] = 'Top 5 Highest Volume'
        bottom_5 = state_totals.tail(5).copy()
        bottom_5['Group'] = 'Bottom 5 Lowest Volume'
        top_bottom_df = pd.concat([top_5, bottom_5])

    fig = px.bar(
        top_bottom_df,
        x='State of Residence',
        y='Births',
        color='Group',
        title="<b>Volume Disparity: Top 5 vs. Bottom 5 Geographies</b>",
        labels={'State of Residence': 'Geography', 'Births': 'Total Live Births'},
        color_discrete_map={
            'Top 5 Highest Volume': COLOR_PRIMARY,
            'Bottom 5 Lowest Volume': COLOR_FEMALE,
            'Selected Geographies': COLOR_SECONDARY
        },
        text_auto=',d'
    )

    max_val = top_bottom_df['Births'].max() if not top_bottom_df.empty else 1000

    fig.update_traces(
        textposition='outside',
        hovertemplate="Geography: <b>%{x}</b><br>Births: <b>%{y:,}</b><extra></extra>"
    )

    fig.update_layout(
        yaxis=dict(title="Total Live Births", range=[0, max_val * 1.18]),
        xaxis=dict(title="Geography"),
        legend_title_text="Volume Group",
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig
