
import streamlit as st
from portkey_ai import Portkey

st.title('Portkey Feedback API')
st.markdown("""
    > The application will produce tweets randomly and give users the option to rate them on a scale of 0 to 5 stars. Each rating will be recorded using Portkey's feedback API, which will capture quality metrics through logs and charts that you can choose for your LLM. Give it a try!. 
""")
with st.popover('Prerequisites'):
    st.markdown("""
    - Get [Portkey API Key](https://portkey.ai/docs/api-reference/authentication#obtaining-your-api-key) and add your OpenAI (or any provider's) API key as a [virtual key](https://portkey.ai/docs/product/ai-gateway-streamline-llm-integrations/virtual-keys).
    - Once feedback is submitted, search the logs by `Trace Id` filter with value `trace_for_feedback`
    - See the Charts on the dashboard. (`Analytics > Feedback`)
""")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("Go to Portkey", "https://www.portkey.ai")
    with col2:
        st.link_button("Read the Docs", "https://portkey.ai/docs")


PORTKEY_API_KEY = st.text_input("Portkey API key")
VIRTUAL_KEY = st.text_input("Virtual Key")

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
        print(f'Rating submitted: {no_of_stars} stars')
        portkey.feedback.create(
        trace_id="trace_for_feedback",
        value=int(no_of_stars), 
    )



    def run():
        st.divider()
        st.header("Tweet generator 👋")
        st.button("Generate", on_click=generate_tweet())
        # number = st.slider("Rate the Tweet", 0, 5)
        col1, col2 = st.columns(2)
        with col1:
            stars = st.radio("Rate the app", ["⭐️", "⭐️⭐️", "⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️⭐️"], index=1)
            score = len(stars)/2
            st.text(f"Selected {score} stars ⭐️")
            st.button("Submit Rating", on_click=send_feedback(no_of_stars=score))
        

    if __name__ == "__main__":
        run()

except ValueError:
    st.markdown("""💡Ensure you fill above fields before generating a tweet""")


