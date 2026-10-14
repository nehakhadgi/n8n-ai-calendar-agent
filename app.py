import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="AI Calendar Assistant",
    page_icon="📅",
    layout="centered"
)

st.title("📅 AI Calendar Assistant")
st.write(
    "Welcome! I am an intelligent personal scheduling agent powered by "
    "**n8n** and **OpenAI (gpt-4o-mini)**. Ask me to schedule events on my calendar!"
)

# 2. Get the n8n webhook URL from Streamlit secrets (for secure production deployment)
# For local testing, you can fallback to a local string, but secrets are best practice!
N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", "https://your-n8n-instance.com/webhook/schedule-agent")

# 3. Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! What meeting or event can I schedule for you today?"}
    ]

# 4. Display Existing Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Input
if user_prompt := st.chat_input("e.g., Book a sync meeting tomorrow at 3 PM"):
    # Display user's message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🧠 *Thinking and checking calendar...*")

        try:
            # Send payload to n8n backend
            payload = {"message": user_prompt}
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
            
            if response.status_code == 200:
                # n8n output usually parses as a list or a direct JSON response
                response_data = response.json()
                
                # Extract the output message. Adjust the key mapping based on your n8n output schema
                # Usually, n8n AI agent response text is located in 'output' or 'text' keys
                ai_reply = ""
                if isinstance(response_data, list) and len(response_data) > 0:
                    ai_reply = response_data[0].get("output") or response_data[0].get("text") or "Event successfully processed!"
                elif isinstance(response_data, dict):
                    ai_reply = response_data.get("output") or response_data.get("text") or "Event successfully processed!"
                else:
                    ai_reply = "I've successfully scheduled that event on your calendar!"

                message_placeholder.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            else:
                error_msg = f"⚠️ Server communication error (Status Code: {response.status_code}). Please try again."
                message_placeholder.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

        except requests.exceptions.Timeout:
            timeout_msg = "⏱️ The request timed out. My AI agent took a bit too long to configure your event, but check your calendar!"
            message_placeholder.markdown(timeout_msg)
            st.session_state.messages.append({"role": "assistant", "content": timeout_msg})
        except Exception as e:
            general_error = f"❌ An unexpected error occurred: {str(e)}"
            message_placeholder.markdown(general_error)
            st.session_state.messages.append({"role": "assistant", "content": general_error})
