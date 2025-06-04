import streamlit as st
import pandas as pd

st.title("CSV Transformer Tool")

# Step 1: Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Step 2: Define your transformation function
def transform(df):
    # Example transformation:
    # - Capitalize first column (assumed to be string)
    # - Double the values of second column (assumed numeric)
    if df.shape[1] >= 2:
        df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.upper()
        df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce') * 2
    return df

# Step 3: Process and show download button
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Original Data")
    st.dataframe(df)

    transformed_df = transform(df)

    st.subheader("Transformed Data")
    st.dataframe(transformed_df)

    # Convert to CSV and offer download
    csv = transformed_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Transformed CSV", csv, "transformed.csv", "text/csv")
