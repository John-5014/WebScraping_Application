import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import *

st.set_page_config(page_title = "Analytics Dashboard", page_icon = "📊",layout="wide")
st.subheader("📈 Descriptive Analysis")
st.markdown("##")

#fetching data

result = view_all_data()
df = pd.DataFrame(result, columns=["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating","id"])
# st.dataframe(df)
#sidebar
st.sidebar.image("../data/images/logo.png", caption = "Online Analytics")
st.sidebar.header("Please filter")
#instances within the columns
region = st.sidebar.multiselect(
    "Select Region",
    options = df["Region"].unique(),
    default = df["Region"].unique(),
)
location = st.sidebar.multiselect(
    "Select Location",
    options = df["Location"].unique(),
    default = df["Location"].unique(),
)
construction = st.sidebar.multiselect(
    "Select Construction",
    options = df["Construction"].unique(),
    default = df["Construction"].unique(),
)
df_selection = df.query(
    
    "Region==@region & Location==@location & Construction==@construction"
)
# st.dataframe(df_selection)

def Home():
    with st.expander("Tabular"):
        showData= st.multiselect("Filter: ",df_selection.columns,default=[])
        st.write(df_selection[showData])
Home()