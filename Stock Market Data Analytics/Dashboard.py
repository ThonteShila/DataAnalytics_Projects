# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 18:01:13 2026

@author: santo
"""

import streamlit as st
st.set_page_config(page_title="Stock Analysis Dashboard",layout="wide")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

company_list=['C:\\Shila Data\\DataAnalytics_Projects\\Stock Market Data Analytics\\S&P_resources\\individual_stocks_5yr\\GOOG_data.csv', 'C:\\Shila Data\\DataAnalytics_Projects\\Stock Market Data Analytics\\S&P_resources\\individual_stocks_5yr\\AAPL_data.csv',
 'C:\\Shila Data\\DataAnalytics_Projects\\Stock Market Data Analytics\\S&P_resources\\individual_stocks_5yr\\AMZN_data.csv', 'C:\\Shila Data\\DataAnalytics_Projects\\Stock Market Data Analytics\\S&P_resources\\individual_stocks_5yr\\MSFT_data.csv']
all_data=pd.DataFrame()
for comp in company_list:
    df=pd.read_csv(comp)
    all_data=pd.concat([all_data,df],ignore_index=True)  

all_data["date"]=pd.to_datetime(all_data["date"])

tech_list=all_data["Name"].unique()

st.title("Tech Stock Analysis")

selected_company=st.sidebar.selectbox("Select Stosk",tech_list)

comp_df=all_data[all_data["Name"]==selected_company]

comp_df.sort_values("date",inplace=True)

st.subheader(f"1.Closing Price of {selected_company} over Time")

