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

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.logger import get_logger


LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Introduction",
        page_icon=":spiral_note_pad:",
    )
    st.write("# Introduction")

data = pd.read_csv("https://github.com/JohnMacStar/semester-project-econ8320/releases/download/Data/ECON8320Final.csv")

fullData =data.HEFAMINC.str.extract(r'(\d+,?\d+)?([^0-9]*)?(\d+?,\d+)?')
fullData[0] = fullData[0].str.replace(',','')
fullData[0] = fullData[0].fillna("0")
fullData[0] = fullData[0].astype(int)
fullData = pd.concat([fullData,data], axis = 1)
fullData = fullData.rename(columns = {0:"Income"})
fullData['Income'] = fullData['Income'].astype(int)
fullData = fullData[['Income','STATE']]
fullData = fullData.groupby("STATE").mean().reset_index()

data = data[["STATE","PEEDUCA"]]
data = data.groupby(["STATE","PEEDUCA"]).size().reset_index()
data = data.rename(columns={0:"Count"})


data['Count'] = data["Count"].astype(int)
test = data.groupby(['STATE']).Count.sum().reset_index()
data = pd.merge(data,test, on="STATE")
data = data[data['PEEDUCA'] == "MASTER'S DEGREE(EX:MA,MS,MEng,MEd,MSW)"]
data['total'] = (data['Count_x'] / data['Count_y'])*100

mapdata = px.choropleth(locationmode = "USA-states", locations = data['STATE'], color = data['total'], scope = "usa", range_color=(10,23))
incmap = px.choropleth(locationmode = "USA-states", locations = fullData['STATE'], color = fullData['Income'], scope = "usa")
    
    
    st.plotly_chart(mapdata)
    st.plotly_chart(incmap)
if __name__ == "__main__":
    run()
