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

#fig 1

st.subheader(f"1.Closing Price of {selected_company} over Time")

fig1=px.line(comp_df,x="date",y="close",title=selected_company+" Closing Prices Over Time")
st.plotly_chart(fig1,use_container_width=True)


#fig 2
#Moving avg
st.subheader(f"2.Moving Average of {selected_company} over Time")
all_data["Ma20"]=all_data.groupby("Name")["close"].transform(lambda  x: x.rolling(20).mean())
all_data["Ma10"]=all_data.groupby("Name")["close"].transform(lambda  x: x.rolling(10).mean())
all_data["Ma50"]=all_data.groupby("Name")["close"].transform(lambda  x: x.rolling(50).mean())
avg_stock=all_data[all_data["Name"]=="AAPL"]
fig2=px.line(avg_stock, x="date",y=["close","Ma20","Ma50","Ma10"],title=f"{selected_company} Stock Price with Moving Averages",labels={"date":"Date","value":"Price"},color_discrete_map={"close":"blue","Ma20":"orange","ma50":"green","Ma10":"red"})
st.plotly_chart(fig2,use_container_width=True)

#fig3
#Daily return for company
st.subheader(f"3.Daily Returns for {selected_company}")
comp_df["Daily Return in %"]=comp_df["close"].pct_change()*100
fig3=px.line(comp_df,x="date",y="close",title="Daily return in (%)")
st.plotly_chart(fig3,use_container_width=True)

#fig4
#Resampled price for company
st.subheader(f"4.Resampled Price (Monthly / Quarterly / Yearly)for {selected_company}")
comp_df.set_index('date',inplace=True)
genre = st.radio(
    "Select resample frequency",
    ["Monthly", "Quarterly", "Yearly"]
)
if genre=="Monthly":
    resampled=comp_df["close"].resample("ME").mean()

    
elif genre=="Quarterly":
    resampled=comp_df["close"].resample("QE").mean()
    
else:
   resampled=comp_df["close"].resample("YE").mean()
    
fig4=px.line(resampled,title=selected_company + " " +genre +" "+ "Average Closing Price" )
st.plotly_chart(fig4,use_container_width=True)

#fig 5
#co relation between company lounching dashboard
app=pd.read_csv(company_list[0])
goog=pd.read_csv(company_list[1])
amzn=pd.read_csv(company_list[2])
msft=pd.read_csv(company_list[3])
closing_price=pd.DataFrame()
closing_price["APPL_close"]=app["close"].values
closing_price["GOOG_close"]=pd.Series(goog["close"].values)
closing_price["AMZN_close"]=pd.Series(amzn["close"].values)
closing_price["MSFT_close"]=pd.Series(msft["close"].values)

closing_price.corr()
fig5,ax=plt.subplots()
sns.heatmap(closing_price.corr(),annot=True,cmap="coolwarm")
st.pyplot(fig5)

st.markdown("---")


st.markdown("**Note:** This dashboard provides basic technical analysis of major tech stocks")

