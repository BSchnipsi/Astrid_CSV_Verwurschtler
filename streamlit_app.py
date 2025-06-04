import streamlit as st
import pandas as pd

st.title("CSV Transformer Tool")

uploaded_file = st.file_uploader("Upload your CSV file (semicolon-separated)", type=["csv"])

# Load the CSV starting from the row where the first cell is 'Kundennummer'
def load_csv_with_kundennummer(file):
    raw_lines = file.getvalue().decode("utf-8").splitlines()

    header_index = None
    for i, line in enumerate(raw_lines):
        if line.strip().startswith("Kundennummer"):
            header_index = i
            break

    if header_index is None:
        raise ValueError("Header row with 'Kundennummer' not found.")

    data_str = "\n".join(raw_lines[header_index:])
    from io import StringIO
    return pd.read_csv(StringIO(data_str), delimiter=';')

# Transform to the desired output format
def transform(df):
df.columns = df.columns.str.strip()  # Clean up column names

output = pd.DataFrame()
output["satzart"] = ["0"] * len(df)
output["konto"] = ["200000"] * len(df)
output["gkonto"] = ["4000"] * len(df)

output["belegnr"] = df["ReNr."]
output["belegdatum"] = df["Datum"]
output["buchsymbol"] = df["BS"]

output["buchcode"] = ["1"] * len(df)
output["prozent"] = ["20"] * len(df)
output["steuercode"] = ["1"] * len(df)

# Handle comma-as-decimal conversion
output["betrag"] = pd.to_numeric(
df["Brutto"].astype(str).str.replace(",", "."), errors="coerce"
)
output["steuer"] = -pd.to_numeric(
df["Ust."].astype(str).str.replace(",", "."), errors="coerce"
)

output["text"] = df["Name"]

return output


if uploaded_file:
    try:
        df = load_csv_with_kundennummer(uploaded_file)
        st.success("CSV loaded successfully from 'Kundennummer' row.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    st.subheader("Original Data")
    st.dataframe(df)

    transformed_df = transform(df)
    st.subheader("Transformed Data")
    st.dataframe(transformed_df)

    csv = transformed_df.to_csv(index=False, sep=';').encode('utf-8')
    st.download_button("Download Transformed CSV", csv, "transformed.csv", "text/csv")
