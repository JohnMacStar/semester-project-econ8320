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

import time

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit.hello.utils import show_code


def page2():
    st.write("# Population Distribution of Education")
    
    data = pd.read_csv("https://github.com/JohnMacStar/semester-project-econ8320/releases/download/Data/ECON8320Final.csv")
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
    raceinc = raceinc.replace({"AI-Asian":"Other","AI-HP":"Other","American Indian, Alaskan Native Only":"Other","Asian-HP":"Other","Black-AI":"Other","Black-Asian":"Other", "Hawaiian/Pacific Islander Only":"Other", "Other 3 Race Combinations":"Other","Other 4 and 5 Race Combinations":"Other", "W-A-HP":"Other", "W-AI-A":"Other", "W-AI-HP":"Other", "W-B-A":"Other", "W-B-AI-A":"Other", "W-B-AI":"Other", "W-B-HP":"Other", "White-AI":"Other", "White-Asian":"Other", "White-Black":"Other","White-HP":"Other"})
    raceinc = raceinc.groupby(["PTDTRACE"]).mean().reset_index()
    raceinc = raceinc.sort_values('Income', ascending=False)

    educbox = px.box(ulttest, x = "PEEDUCA", y = "Income", color = "PESEX")
    educhist = px.histogram(sample2024, x = "PEEDUCA", barmode = "group", histnorm = "percent")



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


    raceed = ulttest[['PEEDUCA', 'PTDTRACE']]
    raceed = raceed.groupby(["PTDTRACE","PEEDUCA"]).size().reset_index()
    raceed = raceed.rename(columns = ({0:"Count"}))
    raceed = raceed.replace({"AI-Asian":"Other","AI-HP":"Other","American Indian, Alaskan Native Only":"Other","Asian-HP":"Other","Black-AI":"Other","Black-Asian":"Other", "Hawaiian/Pacific Islander Only":"Other", "Other 3 Race Combinations":"Other","Other 4 and 5 Race Combinations":"Other", "W-A-HP":"Other", "W-AI-A":"Other", "W-AI-HP":"Other", "W-B-A":"Other", "W-B-AI-A":"Other", "W-B-AI":"Other", "W-B-HP":"Other", "White-AI":"Other", "White-Asian":"Other", "White-Black":"Other","White-HP":"Other"})
    raceved = px.histogram(raceed, x = "PEEDUCA", y = "Count", color = "PTDTRACE", barmode = "group", histnorm = "percent")
    #End of comment
    
    st.plotly_chart(educhist)
    st.plotly_chart(raceved)
    st.plotly_chart(emplbar)
page2()
