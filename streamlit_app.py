import streamlit as st
import pandas as pd

st.title("Astrids CSV-Verwurschtler")

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
    df.columns = df.columns.str.strip()  # Clean column names

    # Filter only rows where BS is "AR" or "ST"
    df = df[df["BS"].isin(["AR", "ST"])].copy()

    # Sort by 'ReNr.' (belegnr)
    df = df.sort_values(by="ReNr.").reset_index(drop=True)

    # Convert numeric values
    betrag = pd.to_numeric(df["Brutto"].astype(str).str.replace(",", "."), errors="coerce")
    steuer = -pd.to_numeric(df["Ust."].astype(str).str.replace(",", "."), errors="coerce")

    # Assemble output dataframe
    output = pd.DataFrame({
        "satzart": ["0"] * len(df),
        "konto": ["200000"] * len(df),
        "gkonto": ["4000"] * len(df),
        "belegnr": df["ReNr."],
        "belegdatum": df["Datum"],
        "buchsymbol": df["BS"],
        "buchcode": ["1"] * len(df),
        "prozent": ["20"] * len(df),
        "steuercode": ["1"] * len(df),
        "betrag": betrag,
        "steuer": steuer,
        "text": df["Name"]
    })

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

    # Show group totals by 'buchsymbol'
    st.subheader("Sum of 'betrag' grouped by 'buchsymbol'")
    grouped = transformed_df.groupby("buchsymbol")["betrag"].sum().reset_index()
    grouped["betrag"] = grouped["betrag"].map(
        lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    st.dataframe(grouped)
    
    st.subheader("Transformed Data")
    st.dataframe(transformed_df)

    # Format numbers using comma as decimal separator
    transformed_df["betrag"] = transformed_df["betrag"].map(
        lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if pd.notnull(x) else ""
    )
    transformed_df["steuer"] = transformed_df["steuer"].map(
        lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if pd.notnull(x) else ""
    )

    # Create downloadable CSV with semicolon separator
    csv = transformed_df.to_csv(index=False, sep=';', encoding='utf-8').encode('utf-8')
    st.download_button("Download Transformed CSV", csv, "transformed.csv", "text/csv")
