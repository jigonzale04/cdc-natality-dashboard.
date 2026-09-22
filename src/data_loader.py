"""
Data loader module for CDC Natality 2025 Streamlit Dashboard.
Handles cached data ingestion, validation checks, month categorization, and state code mapping.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

# State to 2-letter USPS abbreviation dictionary (50 US States + District of Columbia)
US_STATE_ABBR = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

# Standard chronological month ordering
MONTH_ORDER = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]


def get_default_data_path() -> Path:
    """Return the absolute path to the dataset, supporting local & Streamlit Cloud execution."""
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / "data" / "Provisional_Natality_2025_CDC.xlsx"


@st.cache_data(show_spinner="Loading and validating provisional 2025 CDC natality data...")
def load_data(file_path: str = None) -> pd.DataFrame:
    """
    Load data from the CDC Excel workbook, run data hygiene audits, 
    and format columns for chronological and spatial analysis.
    """
    if file_path is None:
        target_path = get_default_data_path()
    else:
        target_path = Path(file_path)

    if not target_path.exists():
        raise FileNotFoundError(f"Dataset missing at location: {target_path}")

    # Read first sheet of Excel workbook
    df = pd.read_excel(target_path, sheet_name=0)

    # --- Data Hygiene & Audit Validation Checks ---
    expected_rows = 1224
    expected_states = 51
    expected_months = 12
    expected_sexes = 2
    expected_total_births = 3604640

    errors = []
    if len(df) != expected_rows:
        errors.append(f"Row count mismatch: found {len(df)}, expected {expected_rows}")
    if df['State of Residence'].nunique() != expected_states:
        errors.append(f"Geography count mismatch: found {df['State of Residence'].nunique()}, expected {expected_states}")
    if df['Month Code'].nunique() != expected_months:
        errors.append(f"Month count mismatch: found {df['Month Code'].nunique()}, expected {expected_months}")
    if df['Sex of Infant'].nunique() != expected_sexes:
        errors.append(f"Sex category mismatch: found {df['Sex of Infant'].nunique()}, expected {expected_sexes}")
    if df.isnull().sum().sum() > 0:
        errors.append(f"Missing values found: {df.isnull().sum().sum()}")
    if df.duplicated().sum() > 0:
        errors.append(f"Duplicate rows found: {df.duplicated().sum()}")
    if df['Births'].sum() != expected_total_births:
        errors.append(f"Total births sum mismatch: found {df['Births'].sum():,}, expected {expected_total_births:,}")

    if errors:
        error_msg = "; ".join(errors)
        st.error(f"Data Validation Failed: {error_msg}")
        raise ValueError(f"Data audit failure: {error_msg}")

    # Enforce chronological ordering on Month column
    df['Month'] = pd.Categorical(df['Month'], categories=MONTH_ORDER, ordered=True)

    # Add 2-letter state code for geographical map plotting
    df['State Code'] = df['State of Residence'].map(US_STATE_ABBR)

    # Sort dataframe chronologically by Month Code and State
    df = df.sort_values(by=['Month Code', 'State of Residence', 'Sex of Infant']).reset_index(drop=True)

    return df
