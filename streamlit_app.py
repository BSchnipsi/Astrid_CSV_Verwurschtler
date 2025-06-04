import streamlit as st
import pandas as pd

st.title("CSV Transformer Tool")

uploaded_file = st.file_uploader("Upload your CSV file (semicolon-separated)", type=["csv"])

def transform(df):
    if df.shape[1] >= 2:
        df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.upper()
        df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce') * 2
    return df

if uploaded_file:
    try:
        # Try to read with semicolon delimiter first
        df = pd.read_csv(uploaded_file, delimiter=';')
        st.success("CSV loaded successfully with semicolon delimiter.")
    except Exception as e:
        st.error(f"Failed to parse CSV: {e}")
        st.stop()

    st.subheader("Original Data")
    st.dataframe(df)

    transformed_df = transform(df)
    st.subheader("Transformed Data")
    st.dataframe(transformed_df)

    csv = transformed_df.to_csv(index=False, sep=';').encode('utf-8')
    st.download_button("Download Transformed CSV", csv, "transformed.csv", "text/csv")
