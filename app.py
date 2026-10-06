"""
CSC-128 Assignment 7: Agent with Tools
Michelle Salgado

Streamlit interface for the room reservation agent.
"""

import streamlit as st
from groq import Groq

from agent import run_agent
from tools import dispatch_tool


st.set_page_config(
    page_title="Room Reservation Agent",
    page_icon="🏫"
)

st.title("🏫 Room Reservation Agent")

st.write(
    "Ask me about available rooms, building hours, "
    "or ask me to reserve a room."
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if "tool_log" not in st.session_state:
    st.session_state.tool_log = []

if "pending_booking" not in st.session_state:
    st.session_state.pending_booking = None

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

question = st.text_input(
    "Ask a question:",
    placeholder="Example: What rooms are available on Monday?"
)

if question and question != st.session_state.last_question:
    st.session_state.last_question = question
    st.session_state.pending_booking = Non

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

def parse_tool_arguments(argument_string):
    """Safely parse tool arguments from a JSON string."""
    try:
        return json.loads(argument_string)
    except json.JSONDecodeError as error:
        return f"Invalid tool arguments: {error}"

    result = run_agent(
        client,
        messages,
        tool_log=st.session_state.tool_log
    )

    if isinstance(result, dict) and result.get("confirmation_required"):
        st.session_state.pending_booking = result["arguments"]
        st.warning(result["message"])

    else:
        st.subheader("Answer")
        st.write(result)

# Confirmation step for the state-changing booking tool
if st.session_state.pending_booking:
    booking = st.session_state.pending_booking

    st.write(
        f"Pending reservation: Room {booking['room']} on "
        f"{booking['day']} for {booking['name']}."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Confirm Booking"):
            tool_result = dispatch_tool("book_room", booking)

            st.session_state.tool_log.append(
                {
                    "tool": "book_room",
                    "arguments": booking.copy(),
                    "result": tool_result
                }
            )

            st.success(tool_result)
            st.session_state.pending_booking = None
            st.rerun()

    with col2:
        if st.button("Cancel"):
            st.info("Booking canceled. No changes were made.")
            st.session_state.pending_booking = None
            st.rerun()

st.divider()
st.subheader("Tool Log")

if st.session_state.tool_log:
    for entry in st.session_state.tool_log:
        st.write(f"**Tool:** {entry['tool']}")
        st.write(f"**Arguments:** {entry['arguments']}")
        st.write(f"**Result:** {entry['result']}")
        st.divider()
else:
    st.write("No tools have been called yet.")