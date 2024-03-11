
import streamlit as st
from streamlit.logger import get_logger
from streamlit_feedback import streamlit_feedback
from portkey_ai import Portkey

LOGGER = get_logger(__name__)
PORTKEY_API_KEY = st.text_input("Portkey API key")
VIRTUAL_KEY = st.text_input("Virtual Key")
st.link_button("Go to Portkey", "https://www.portkey.ai")

try:
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

except ValueError:
    st.markdown("""💡Ensure you fill above fields before generating a tweet""")


