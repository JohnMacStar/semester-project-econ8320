# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px

import streamlit as st
from streamlit.hello.utils import show_code

def Page1():
    st.write("# How Important is Education in Relation to Earning a Higher Income")

    data = pd.read_csv("https://github.com/JohnMacStar/semester-project-econ8320/releases/download/Data/ECON8320Final.csv")
    #st.dataframe(data.head())
    sample2024 = data[data['Year'] == 2024]
    sample2024['PEEDUCA'] = sample2024['PEEDUCA'].str.replace('(ged)','')
    sample2024['PEEDUCA'] = sample2024['PEEDUCA'].str.replace('(ex:ba,ab,bs)','')
    sample2024['PEEDUCA'] = sample2024['PEEDUCA'].str.replace("(EX:MA,MS,MEng,MEd,MSW)",'')
    
    test = sample2024.HEFAMINC.str.extract(r'(\d+,?\d+)?([^0-9]*)?(\d+?,\d+)?')
    test[0] = test[0].str.replace(',','')
    test[0] = test[0].fillna("0")
    test[0] = test[0].astype(int)
    ulttest = pd.concat([test,sample2024], axis = 1)
    ulttest = ulttest.rename(columns = {0:"Income"})
    
    kiddata = sample2024[['PEEDUCA', 'PRNMCHLD']]
    kiddata = kiddata.groupby(['PEEDUCA']).mean().reset_index()

    incvchld = ulttest[['Income', 'PRNMCHLD']]
    incvchld = incvchld.groupby(["Income"]).mean().reset_index()

    raceinc = ulttest[['Income', 'PTDTRACE']]
    raceinc = raceinc.groupby(["PTDTRACE"]).mean().reset_index()
    raceinc = raceinc.sort_values('Income', ascending=False)

    educbox = px.box(ulttest, x = "PEEDUCA", y = "Income", color = "PESEX")
    educhist = px.histogram(sample2024, x = "PEEDUCA", barmode = "group", histnorm = "percent")
    kidbar = px.bar(kiddata, x = "PEEDUCA", y = "PRNMCHLD")
    childrenvinc = px.scatter(incvchld, x = "Income", y = "PRNMCHLD")
    racebar = px.bar(raceinc, x = "PTDTRACE", y = "Income")


    ##Eventually edit to make this main data
    fullData =data.HEFAMINC.str.extract(r'(\d+,?\d+)?([^0-9]*)?(\d+?,\d+)?')
    fullData[0] = fullData[0].str.replace(',','')
    fullData[0] = fullData[0].fillna("0")
    fullData[0] = fullData[0].astype(int)
    fullData = pd.concat([fullData,data], axis = 1)
    fullData = fullData.rename(columns = {0:"Income"})

    empl = fullData[['PEEDUCA','PREXPLF']]
    empl = empl.groupby(['PREXPLF','PEEDUCA']).size().reset_index()
    empl = empl.rename(columns = {0:"Count"})
    empl = empl[empl["PREXPLF"] != "In Universe, Met No Conditions To Assign"]
    emplbar = px.histogram(empl, x = "PREXPLF", y = "Count", color = "PEEDUCA", barmode = "group", histnorm = "percent")
    
    fullSample2024 = fullData[(fullData['Year'] == 2024)]
    
    timeInc = fullData[['Income', 'Year','PEEDUCA']]
    timeInc = timeInc.groupby(["Year","PEEDUCA"]).mean().reset_index()
    
    timeoInc = px.line(timeInc, x = "Year", y = "Income", color = "PEEDUCA")

    hoursinc = fullData[["PEERNHRO", "PEEDUCA","Income"]]
    hoursinc = hoursinc[hoursinc["PEERNHRO"] != -1]
    hoursinc = hoursinc.groupby(["PEEDUCA","Income"]).mean().reset_index()
    hourvinc = px.scatter(hoursinc, x = "PEERNHRO", y = "Income", color = "PEEDUCA")
    #End of comment

    
    st.plotly_chart(educbox)
    st.write("""
    Obtaining a higher education not only will increase the amount of knowledge someone has but also increases their abilities and skills within that sector. 
    Academic achievement exemplifies the development and preparedness that one gains from a well rounded education. This is more appealing to compainies and there for
    will typically be offered higher salaries.
    """)
    st.plotly_chart(timeoInc)
    st.write("""
    Salaries over time do increase to match up with inflation and tend to increase at a fairly steady rate regardless of education. Having a higher education will start
    with a larger starting salary but the increases will still be on par with most other positions.
    """)
    st.plotly_chart(hourvinc)
    st.write("""
    The number of hours worked will directly affect income level regardless of education level. However, higher education salaries will tend to surpass lower 
    education salaries even with less working hours per week.
    """)

Page1()
