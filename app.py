import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Neuropeptide Database", layout="wide")
st.title("🧬 Neuropeptide Database")
st.markdown("Search and explore neuropeptides, predicted structures, and CCS values.")

# Load peptide database
@st.cache_data
def load_data():
    df = pd.read_csv("peptides.csv")
    # Add length column if not present
    if "Length" not in df.columns:
        df["Length"] = df["Sequence"].apply(len)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filters")

# Search bar
search_query = st.sidebar.text_input("Peptide name contains:")

# Peptide length slider
min_len = int(df["Length"].min())
max_len = int(df["Length"].max())
length_range = st.sidebar.slider(
    "Peptide length (aa):",
    min_value=min_len,
    max_value=max_len,
    value=(min_len, max_len),
)

# Apply filters
filtered_df = df[
    df["Name"].str.contains(search_query, case=False, na=False) &
    df["Length"].between(length_range[0], length_range[1])
]

# Display results
st.markdown(f"### Showing {len(filtered_df)} matching peptides")
for index, row in filtered_df.iterrows():
    st.markdown(f"### 🔹 {row['Name']}")
    st.write(f"**Sequence:** {row['Sequence']}  \n**Length:** {row['Length']} aa")
    st.write(f"**Collision Cross Section (CCS):** {row['CCS']} Å²")
    
    # Show structure image if it exists
    if os.path.exists(row["StructureImage"]):
        st.image(row["StructureImage"], width=300, caption="Structure Prediction")
    else:
        st.info("No structure image available.")

    st.markdown("---")
