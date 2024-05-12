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

import altair as alt
import pandas as pd

import streamlit as st
from streamlit.hello.utils import show_code


def page4():
    st.write("# Conclusion")
    st.write("""After analyzing education attainment and income level we have been able to explore several factors.
    - First, we have determined that the level of education attained by individuals directly affects the amount of income they will earn on average.
    - Second, higher education is much more rare than lower levels of education as higher education can be extremely expensive and require a large comitment.
    - Third, after exploring some other factors we discovered that the amount of income and level of education both have a positive correlation with the number of children had per household.
    """)
page4()

