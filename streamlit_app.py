import streamlit as st
import pandas as pd

st.title("CSV Transformer Tool")

uploaded_file = st.file_uploader("Upload your CSV file (semicolon-separated)", type=["csv"])

def transform(df):
    if df.shape[1] >= 2:
        df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.upper()
        df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce') * 2
    return df

def load_csv_with_kundennummer(file):
    # Read all lines first to search for header row
    raw_lines = file.getvalue().decode("utf-8").splitlines()

    header_index = None
    for i, line in enumerate(raw_lines):
        if line.startswith("Kundennummer"):
            header_index = i
            break

    if header_index is None:
        raise ValueError("Header row with 'Kundennummer' not found.")

    # Re-read the file from the header row
    data_str = "\n".join(raw_lines[header_index:])
    from io import StringIO
    return pd.read_csv(StringIO(data_str), delimiter=';')

if uplo
