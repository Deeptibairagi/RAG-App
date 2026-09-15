import json

import streamlit as st

from app.database.connection import save_conversation, get_conversation, delete_conversation


# ============================================================
# Initialize session state
# ============================================================

def initialize_session_state():

    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None

    if "messages" not in st.session_state:
        st.session_state.messages = []


# ============================================================
# Start new chat
# ============================================================

def start_new_chat():

    current_chat_id = (
        st.session_state.current_chat_id
    )

    messages = (
        st.session_state.messages
    )

    # --------------------------------------------------------
    # Save current chat before starting new one
    # --------------------------------------------------------

    if current_chat_id and messages:

        save_conversation(
            current_chat_id,
            messages,
        )

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    st.session_state.current_chat_id = None
    st.session_state.messages = []


# ============================================================
# Load existing chat
# ============================================================

def load_chat(
    conversation_id,
):

    conversation = get_conversation(
        conversation_id
    )

    if conversation is None:
        return

    try:

        messages = json.loads(
            conversation["messages"]
        )

    except (
        json.JSONDecodeError,
        TypeError,
    ):

        messages = []

    st.session_state.current_chat_id = (
        conversation_id
    )

    st.session_state.messages = messages


# ============================================================
# Delete chat
# ============================================================

def remove_chat(
    conversation_id,
):

    delete_conversation(
        conversation_id
    )

    # --------------------------------------------------------
    # If deleting active chat
    # --------------------------------------------------------

    if (
        conversation_id
        == st.session_state.current_chat_id
    ):

        st.session_state.current_chat_id = None
        st.session_state.messages = []