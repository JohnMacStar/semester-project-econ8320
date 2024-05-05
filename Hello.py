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

    #st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        This is an introduction to my streamlit dashboard!
        - I will be covering education and its impacts on a multitude of factors
        - Income and unemployment are the main ones.
        """
    )
    data = pd.read_csv("https://github.com/JohnMacStar/semester-project-econ8320/releases/download/Data/ECON8320Final.csv")
    #st.dataframe(data.head())
    sample2024 = data[data['Year'] == 2024]
    
    test = sample2024.HEFAMINC.str.extract(r'(\d+,?\d+)?([^0-9]*)?(\d+?,\d+)?')
    test[0] = test[0].str.replace(',','')
    test[0] = test[0].fillna("0")
    test[0] = test[0].astype(int)
    ulttest = pd.concat([test,sample2024], axis = 1)
    ulttest = ulttest.rename(columns = {0:"Income"})
    ulttest['PEEDUCA'] = ulttest['PEEDUCA'].str.replace('(ged)','')
    ulttest['PEEDUCA'] = ulttest['PEEDUCA'].str.replace('(ex:ba,ab,bs)','')
    ulttest['PEEDUCA'] = ulttest['PEEDUCA'].str.replace("(EX:MA,MS,MEng,MEd,MSW)",'')
    educbox = px.box(ulttest, x = "PEEDUCA", y = "Income")
    educhist = px.histogram(sample2024, x = "PEEDUCA", barmode = "group")
    
    st.plotly_chart(educbox)
    st.plotly_chart(educhist)
if __name__ == "__main__":
    run()
