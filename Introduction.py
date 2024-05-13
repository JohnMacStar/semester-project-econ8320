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
    #reading in the data
    data = pd.read_csv("https://github.com/JohnMacStar/semester-project-econ8320/releases/download/Data/ECON8320Final.csv")

    #making more adjustments to the data to have income as a value
    fullData =data.HEFAMINC.str.extract(r'(\d+,?\d+)?([^0-9]*)?(\d+?,\d+)?')
    fullData[0] = fullData[0].str.replace(',','')
    fullData[0] = fullData[0].fillna("0")
    fullData[0] = fullData[0].astype(int)
    fullData = pd.concat([fullData,data], axis = 1)
    fullData = fullData.rename(columns = {0:"Income"})
    fullData['Income'] = fullData['Income'].astype(int)
    fullData = fullData[['Income','STATE']]
    fullData = fullData.groupby("STATE").mean().reset_index()

    #Working to get a count of those with a Master's degree in order to plot this
    data = data[["STATE","PEEDUCA"]]
    data = data.groupby(["STATE","PEEDUCA"]).size().reset_index()
    data = data.rename(columns={0:"Count"})
    data['Count'] = data["Count"].astype(int)
    test = data.groupby(['STATE']).Count.sum().reset_index()
    data = pd.merge(data,test, on="STATE")
    data = data[data['PEEDUCA'] == "MASTER'S DEGREE(EX:MA,MS,MEng,MEd,MSW)"]
    data['total'] = (data['Count_x'] / data['Count_y'])*100

    st.write("""
    Furthering education is a large decision to make in order to take your carreer to the next level. 
    One of the motivating factors for continuing school is to make a higher salary.
    However, it is never certain that just because someone has a higher education means that they will recieve a higher salary.
    """)
    st.write("""
    Looking at U.S. census data we can take a look at real situations to discover if higher education is actually associated with a higher salary. 
    We can also look at other factors that relate to education and income. This analysis will be based only on the census data which represents close to 1% of the population 
    to give a general idea of the bigger picture. Also, salary trending data will be based upon the lower fence of salary in order to remove extreme outliers.
    """)
    mapdata = px.choropleth(locationmode = "USA-states", locations = data['STATE'], color = data['total'], scope = "usa", range_color=(10,23), color_continuous_scale='plasma', labels={'color':"Percent Population <br> with Master's Degree"}, title = "Distribution of Population with a Master's Degree")
    mapdata = mapdata.update_layout(plot_bgcolor = 'rgba(0,0,0,0)', title_x=0.25)
    incmap = px.choropleth(locationmode = "USA-states", locations = fullData['STATE'], color = fullData['Income'], scope = "usa",color_continuous_scale='plasma',labels={'color':'Income'}, title = "Average Income by State")
    incmap = incmap.update_layout(plot_bgcolor = 'rgba(0,0,0,0)', title_x=0.25)
        
    st.plotly_chart(mapdata)
    st.write("""This map shows the percentage of population that has obtained a Master's degree. This gives an idea of the distribution of education accross the U.S. 
    The north-east tends to have more education as education is more valued due to the historical universities that were sprung up in the north-east such as Harvard University.
    """)
    st.plotly_chart(incmap)
    st.write("""Using this income map we can look at the similarities and differences between this one and the previous education map. It is clear that there is a relation 
    between the amount of higher education and higher salary. Colorado stands out as one of the most educated states and highest salary states. 
    Colorado does not have a super large college or Master's degree graduation rate but Colorado has had a large number of college and Master's educated residents moving to the state.
    """)

if __name__ == "__main__":
    run()
