import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib as plt

st.set_page_config(page_title="LCFS Statistics Dashboard",
                   page_icon=":chart_with_upwards_trend:",
                   layout="wide"
)

df = pd.read_excel(
    io='lcfs.xlsx',
    engine='openpyxl',
    sheet_name='database',
    skiprows=0,
    usecols='A:L',
    nrows=5145,
)

st.title("📈 LCFS Dashboard")

#----Sidebar_Construction----#

st.sidebar.header("Use the Filters Below")
region = st.sidebar.multiselect(
    "Select the Region:",
    options=df["Government_region"].unique(),
    default=df["Government_region"].unique()
)

#Add a help tag to describe what the Govt. Training means
income = st.sidebar.multiselect(
    "Select Main Source of Income:",
    options=df["Income_source"].unique(),
    #add help tag
    default=df["Income_source"].unique()
)

position = st.sidebar.multiselect(
    "Select Economic Position of Household Reference Person:",
    #add help tag
    options=df["Economic_position"].unique(),
    default=df["Economic_position"].unique()
)

#Add a help tag to describe what the numbers mean
occupation = st.sidebar.multiselect(
    "Select Occupation of Household Reference Person:",
    help="These refer to the NS-SEC 3 Employment and occupation classes",
    options=df["Occupation"].unique(),
    default=df["Occupation"].unique()
)

children = st.sidebar.multiselect(
    "Select Number of Children in Household:",
    options=df["Children"].unique(),
    default=df["Children"].unique()
)

df_selection = df.query(
    "Government_region == @region & Economic_position == @position & Income_source == @income & Occupation == @occupation & Children == @children"
)

#Income by region
income_by_region = (
    df_selection.groupby(by=["Government_region"]).mean()

)
income_fig = px.bar(
    income_by_region,
    x=income_by_region.index,
    y="Weekly_income",
    orientation="v",
    title="<b>Average Weekly Income by Region</b>",
    color_discrete_sequence=["#0083B8"]*len(income_by_region),
    template="plotly_white",
)

st.plotly_chart(income_fig, use_container_width=True)

#Expenditure by region
exp_by_region = (
    df_selection.groupby(by=["Government_region"]).mean()
)

exp_fig = px.bar(
    exp_by_region,
    x=exp_by_region.index,
    y="Weekly_exp",
    orientation="v",
    title="<b>Average Weekly Expenditure by Region</b>",
    color_discrete_sequence=["#0083B8"]*len(exp_by_region),
    template="plotly_white",
)

st.plotly_chart(exp_fig, use_container_width=True)

#Histogram ~ Distribution of Weekly Income

income_dist = (
    df_selection.groupby(by=["Weekly_income"])
)

incomefig =px.histogram(
    income_dist,
    x=0,
    labels={'x':'Weekly Household Income', 'y':'Frequency'},
    title="<b>Distribution of Weekly Income</b>",
    color_discrete_sequence=["#0083B8"]*len(income_dist),
    template="plotly_white",
)

st.plotly_chart(incomefig, use_container_width=True)

#Histogram ~ Distribution of Weekly Expenditure
expenditure_dist = (
    df_selection.groupby(by=["Weekly_exp"])
)

expenditurefig =px.histogram(
    expenditure_dist,
    x=0,
    labels={'x':'Weekly Household Expenditure', 'y':'Frequency'},
    title="<b>Distribution of Weekly Expenditure</b>",
    color_discrete_sequence=["#0083B8"]*len(expenditure_dist),
    template="plotly_white",
)
st.plotly_chart(expenditurefig, use_container_width=True)


