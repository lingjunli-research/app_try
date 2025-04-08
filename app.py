import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Neuropeptide Database", layout="wide")
st.title("🧬 Neuropeptide Database")
st.markdown("Search and explore neuropeptides, predicted structures, and CCS values.")

# Load peptide database
@st.cache_data
def load_data():
    return pd.read_csv("peptides.csv")

df = load_data()

# Search bar
search_query = st.text_input("🔍 Search by peptide name:", "")

# Filter results
filtered_df = df[df["Name"].str.contains(search_query, case=False, na=False)]

# Display results
for index, row in filtered_df.iterrows():
    st.markdown(f"### 🔹 {row['Name']}")
    st.write(f"**Sequence:** {row['Sequence']}")
    st.write(f"**Collision Cross Section (CCS):** {row['CCS']} Å²")
    
    # Show structure image if it exists
    if os.path.exists(row["StructureImage"]):
        st.image(row["StructureImage"], width=300, caption="Structure Prediction")
    else:
        st.info("No structure image available.")

    st.markdown("---")
