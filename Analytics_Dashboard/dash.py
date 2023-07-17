import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import *
import time
import pickle
import numpy as np
from app import predict_laptop_price

# import the model
# pipe = pickle.load(open('./pipe.pkl','rb'))
# data = pickle.load(open('./data.pkl','rb'))

st.set_page_config(page_title = "Analytics Dashboard", page_icon = "📊",layout="wide")
st.subheader("📈 Descriptive Analysis")
st.markdown("##")

#fetching data

result = view_all_data()

data = pd.DataFrame(result, columns=["ID","Company","TypeName","Inches","ScreenResolution","Cpu","Ram","Memory","Gpu","OpSys","Weight","Price"])
# st.dataframe(df)
#sidebar
st.sidebar.image("../data/images/logo.png", caption = "Online Analytics")
st.sidebar.header("Please filter")
#instances within the columns
company_brand = st.sidebar.multiselect(
    "Select Laptop Brand",
    options = data["Company"].unique(),
    default = data["Company"].unique(),
)
laptop_type = st.sidebar.multiselect(
    "Select Type",
    options = data["TypeName"].unique(),
    default = data["TypeName"].unique(),
)
operating_system = st.sidebar.multiselect(
    "Select Os",
    options = data["OpSys"].unique(),
    default = data["OpSys"].unique(),
)
df_selection = data.query(
    
    "Company==@company_brand & TypeName==@laptop_type & OpSys==@operating_system"
)

df_selection["Price"] = pd.to_numeric(df_selection["Price"], errors="coerce")
# st.dataframe(df_selection)

def Home():
    with st.expander("Tabular"):
        showData= st.multiselect("Filter: ",df_selection.columns,default=[])
        st.write(df_selection[showData])
        
    #compute top analytics
    # total_investment = df_selection["Price"].sum()
    # investment_mode = df_selection["Price"].mode()
    # investement_mean = df_selection["Price"].mean()
    # investement_median = df_selection["Price"].median()
    # rating = df_selection["Price"].sum()
    
    #converting to numeric data
    # investment_mode = pd.to_numeric(investment_mode,errors="coerce")
    # total_investment =float(total_investment)
    
    # total1,total2,total3,total4,total5 = st.columns(5, gap='large')
    # with total1:
    #     st.info('Total Prices:', icon ="📌")
    #     st.metric(label="sum in KSH", value=f"{total_investment: .0f}")
        
    # with total2:
    #     st.info('Most frequent', icon ="📌")
    #     st.metric(label="mode KSH", value=investment_mode)
    # with total3:
    #     st.info('Average', icon ="📌")
    #     st.metric(label="average KSH", value=f"{investement_mean: .0f}")
    # with total4:
    #     st.info('Central Earnings', icon ="📌")
    #     st.metric(label="median KSH", value=f"{investement_median: .0f}")
    # with total5:
    #     st.info('Ratings', icon ="📌")
    #     st.metric(label="Rating KSH", value= numerize(rating), help=f""" Total Amount: {rating} """)
    # st.markdown("---")
# Home()

#graph

def graphs():
    # total_investment = int(df_selection["Investment"]).sum()
    # averageRating = int(round(df_selection["Rating"]).mean(), 2)
    
    #simple bar graph
    investment_by_business_type = (
        df_selection.groupby(by=["Company"]).count()[["Price"]].sort_values(by="Price")
    )
    
    fig_investment = px.bar(
        investment_by_business_type,
        x="Price",
        y= investment_by_business_type.index,
        orientation="h",
        title = "<b> Price by Company",
        color_discrete_sequence=["#0083b8"]* len(investment_by_business_type),
        template="plotly_white",
    )
    
    fig_investment.update_layout(
        
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = (dict(showgrid=False))
    )
     #simple line graph
    investment_state = df_selection.groupby(by=["OpSys"]).count()[["Price"]]
    fig_state = px.line(
        investment_state,
        x=investment_state.index,
        y= "Price",
        orientation="v",
        title = "<b> Investment by Operating System",
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
# Home()
# graphs()

def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #99ff99, #FFFF00)} </style>""",unsafe_allow_html=True)
    target = 60000000
    current = df_selection["Price"].sum()
    percent=round((current/target * 100))
    my_bar = st.progress(0)
    
    if percent > 100:
        st.subheader("Target done!")
    else:
        st.write("You have: ", percent, "%", "of", (format(target,"d")), "KSH")
        for percent_complete in range(percent):
            time.sleep(0.1)
            my_bar.progress(percent_complete+1,text="Target Percentage")
            
            

    
def sideBar():
    
    
    with st.sidebar:
        selected = option_menu(
            menu_title= "Main Menu",
            options= ["Home","Progress","Predictions"],
            icons=["house","eye",":crystal_ball:"],
            menu_icon="cast",
            default_index=0
        )
    if selected== "Home":
        st.subheader(f"Page: {selected}")
        Home()
        graphs()
        
    if selected== "Progress":
        st.subheader(f"Page: {selected}")
        Progressbar()
        graphs()
        
    if selected== "Predictions":
        st.subheader(f"Welcome to {selected} page")
        predict_laptop_price()
sideBar()
#theme

hide_st_style = """
<style> 
#MainMenu {visibility:hidden;}
#footer {visibility:hidden;}
#header {visibility:hidden;}

</style>

"""