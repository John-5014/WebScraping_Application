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

df_selection["Investment"] = pd.to_numeric(df_selection["Investment"], errors="coerce")
# st.dataframe(df_selection)

def Home():
    with st.expander("Tabular"):
        showData= st.multiselect("Filter: ",df_selection.columns,default=[])
        st.write(df_selection[showData])
        
    #compute top analytics
    total_investment = df_selection["Investment"].sum()
    investment_mode = df_selection["Investment"].mode()
    investement_mean = df_selection["Investment"].mean()
    investement_median = df_selection["Investment"].median()
    rating = df_selection["Rating"].sum()
    
    #converting to numeric data
    # investment_mode = pd.to_numeric(investment_mode,errors="coerce")
    # total_investment =float(total_investment)
    
    total1,total2,total3,total4,total5 = st.columns(5, gap='large')
    with total1:
        st.info('Total Investment', icon ="📌")
        st.metric(label="sum TZS", value=f"{total_investment: .0f}")
        
    with total2:
        st.info('Most frequent', icon ="📌")
        st.metric(label="mode TZS", value=investment_mode)
    with total3:
        st.info('Average', icon ="📌")
        st.metric(label="average TZS", value=f"{investement_mean: .0f}")
    with total4:
        st.info('Central Earnings', icon ="📌")
        st.metric(label="median TZS", value=f"{investement_median: .0f}")
    with total5:
        st.info('Ratings', icon ="📌")
        st.metric(label="Rating TZS", value= numerize(rating), help=f""" Total Rating: {rating} """)
    st.markdown("---")
# Home()

#graph

def graphs():
    # total_investment = int(df_selection["Investment"]).sum()
    # averageRating = int(round(df_selection["Rating"]).mean(), 2)
    
    #simple bar graph
    investment_by_business_type = (
        df_selection.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
    )
    
    fig_investment = px.bar(
        investment_by_business_type,
        x="Investment",
        y= investment_by_business_type.index,
        orientation="h",
        title = "<b> Investment by Business Type",
        color_discrete_sequence=["#0083b8"]* len(investment_by_business_type),
        template="plotly_white",
    )
    
    fig_investment.update_layout(
        
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = (dict(showgrid=False))
    )
     #simple line graph
    investment_state = df_selection.groupby(by=["State"]).count()[["Investment"]]
    fig_state = px.line(
        investment_state,
        x=investment_state.index,
        y= "Investment",
        orientation="v",
        title = "<b> Investment by State",
        color_discrete_sequence=["#0083b8"]* len(investment_state),
        template="plotly_white",
    )
    fig_state.update_layout(
        xaxis = (dict(tickmode="linear")),
        plot_bgcolor = "rgba(0,0,0,0)",
        yaxis = (dict(showgrid=False))
    )
    
    left,right=st.columns(2)
    left.plotly_chart(fig_state,use_container_width=True)
    right.plotly_chart(fig_investment,use_container_width=True)
Home()
graphs()
