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

from urllib.error import URLError

import pandas as pd
import pydeck as pdk
import plotly.express as px
import streamlit as st
from streamlit.hello.utils import show_code


def page3():
    st.write("Income And Education Affect the Number of Children Families Have")
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
    
    kidbar = px.bar(kiddata, x = "PEEDUCA", y = "PRNMCHLD")
    childrenvinc = px.scatter(incvchld, x = "Income", y = "PRNMCHLD")
    racebar = px.bar(raceinc, x = "PTDTRACE", y = "Income")
    
    st.plotly_chart(childrenvinc)
    st.plotly_chart(kidbar)
    st.plotly_chart(racebar)

page3()
