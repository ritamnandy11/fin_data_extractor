import streamlit as st
import pandas as pd
import dataex_2
from io import StringIO

st.set_page_config(page_title="Financial Data", page_icon="💼", layout="wide")

# Initialize session state
if 'saved_records' not in st.session_state:
    st.session_state.saved_records = []
if 'current_data' not in st.session_state:
    st.session_state.current_data = pd.DataFrame({
        "Measure": ["Company", "CEO", "Market Capital", "Quarter", "Stock Name", "Revenue", "Net Income"],
        "Value": ["", "", "", "", "", "", ""]
    })

# Custom styling
st.markdown("""
    <style>
        div[data-testid="column"] {
            padding: 5px;
        }
        .stMarkdown {
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

def convert_horizontal_to_vertical(horizontal_df):
    """Convert horizontal DataFrame to vertical format"""
    return pd.DataFrame({
        "Measure": ["Company", "CEO", "Market Capital", "Quarter", "Stock Name", "Revenue", "Net Income"],
        "Value": [
            horizontal_df.iloc[0]["Company"],
            horizontal_df.iloc[0]["CEO"],
            horizontal_df.iloc[0]["Market Capital"],
            horizontal_df.iloc[0]["Quarter"],
            horizontal_df.iloc[0]["Stock Name"],
            horizontal_df.iloc[0]["Revenue"],
            horizontal_df.iloc[0]["Net income"]
            
        ]
    })

with col1:
    st.title("Financial Data Extractor")
    news_article = st.text_area("Enter the text here", height=300)
    
    col1_btns = st.columns(4)
    with col1_btns[0]:
        if st.button("Extract"):
            if news_article.strip():
                try:
                    # Get horizontal DataFrame from extraction function
                    raw_data = dataex_2.extract_financial_data(news_article)
                    # Convert to vertical format
                    vertical_data = convert_horizontal_to_vertical(raw_data)
                    st.session_state.current_data = vertical_data
                except Exception as e:
                    st.error(f"Extraction failed: {str(e)}")
            else:
                st.warning("Please enter some text first")
    
    with col1_btns[1]:
        if st.button("Save Data"):
            valid_count = st.session_state.current_data['Value'].str.strip().ne('').sum()
            if valid_count >= 3:
                record = st.session_state.current_data.set_index('Measure')['Value'].to_dict()
                st.session_state.saved_records.append(record)
                st.success("Data saved successfully!")
                # Reset current data
                st.session_state.current_data = pd.DataFrame({
                    "Measure": ["Company", "CEO", "Market Capital", "Quarter", "Stock Name", "Revenue", "Net Income"],
                    "Value": ["", "", "", "", "", "", ""]
                })
            else:
                st.warning("Need at least 3 valid fields to save")
    
    with col1_btns[2]:
        if st.session_state.saved_records:
            csv_string = StringIO()
            all_records_df = pd.DataFrame(st.session_state.saved_records)
            all_records_df.to_csv(csv_string, index=False)
            st.download_button(
                label="Download All",
                data=csv_string.getvalue(),
                file_name="all_financial_records.csv",
                mime="text/csv"
            )
        else:
            st.button("Download All", disabled=True)
    
    with col1_btns[3]:
        if st.button("Clear All"):
            st.session_state.saved_records = []
            st.session_state.current_data = pd.DataFrame({
                "Measure": ["Company", "CEO", "Market Capital", "Quarter", "Stock Name", "Revenue", "Net Income"],
                "Value": ["", "", "", "", "", "", ""]
            })
            st.rerun()

with col2:
    st.markdown("### Current Extraction")
    
    # Vertical display with proper formatting
    for _, row in st.session_state.current_data.iterrows():
        col_left, col_right = st.columns([1, 2])
        with col_left:
            st.markdown(f"**{row['Measure']}**")
        with col_right:
            display_value = row['Value'] if row['Value'].strip() else "-"
            st.markdown(display_value)
    
    st.divider()
    
    if st.session_state.saved_records:
        st.markdown("### Saved Records Status")
        st.success(f"Total records saved: {len(st.session_state.saved_records)}")
        st.caption("All data is securely stored. Use the Download All button to export complete records.")
    else:
        st.markdown("### Saved Records Status")
        st.info("No records saved yet")