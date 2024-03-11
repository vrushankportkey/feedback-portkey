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
from streamlit.logger import get_logger
from streamlit_feedback import streamlit_feedback
from portkey_ai import Portkey

LOGGER = get_logger(__name__)
PORTKEY_API_KEY = st.text_input("Portkey API key")
VIRTUAL_KEY = st.text_input("Virtual Key")
st.link_button("Go to Portkey", "https://www.portkey.ai")
st.markdown("""💡Ensure you fill above fields before generating a tweet""")

portkey = Portkey(
    api_key=PORTKEY_API_KEY,
    virtual_key=VIRTUAL_KEY
)

def generate_tweet():
    response = portkey.with_options(
        trace_id="trace_for_feedback"
    ).chat.completions.create(
    messages = [{ "role": 'user', "content": 'Generate a random tweet' }],
    model = 'gpt-3.5-turbo'
)
    tweet = response['choices'][0]['message']['content']
    st.markdown(f'### {tweet}')
    
def send_feedback(no_of_stars=None):
    portkey.feedback.create(
    trace_id="trace_for_feedback",
    value=no_of_stars, 
)


def run():
    st.divider()
    st.header("Tweet generator 👋")
    st.button("Generate", on_click=generate_tweet())
    number = st.slider("Rate the Tweet", 0, 5)
    st.text(f"Rated {number} stars ⭐️")
    st.button("Submit Rating", on_click=send_feedback(no_of_stars=number))
    st.text("Feedback Saved")

if __name__ == "__main__":
    run()
