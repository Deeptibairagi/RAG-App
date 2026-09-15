# import uuid

# import streamlit as st

# from app.config import API_URL
# from app.api_client import api_client

# from app.session_state import (
#     initialize_session_state,
#     start_new_chat,
#     load_chat,
#     remove_chat,
# )

# from app.database.connection import (
#     init_database,
#     save_conversation,
#     get_all_conversations,
# )


# # ============================================================
# # Page configuration
# # ============================================================

# st.set_page_config(
#     page_title="ThinkSmarter RAG",
#     page_icon="🧠",
#     layout="centered",
# )


# # ============================================================
# # Custom CSS
# # ============================================================

# st.markdown(
#     """
#     <style>

#     /* Sidebar height */
#     section[data-testid="stSidebar"] > div {
#         height: 100vh;
#     }

#     /* Previous chats scrolling area */
#     .chat-history {
#         max-height: 55vh;
#         overflow-y: auto;
#         padding-right: 5px;
#     }

#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # ============================================================
# # Initialize database
# # ============================================================

# init_database()


# # ============================================================
# # Initialize session state
# # ============================================================

# initialize_session_state()


# # ============================================================
# # Header
# # ============================================================

# st.title("🧠 Think Smarter")

# st.caption(
#     "Ask questions and continue the conversation "
#     "with your RAG system."
# )


# # ============================================================
# # Sidebar
# # ============================================================

# with st.sidebar:

#     st.header("⚙️ Configuration")

#     st.caption(
#         f"API: {API_URL}"
#     )

#     # ========================================================
#     # API Check
#     # ========================================================


#     if st.button(
#         " Check API",
#         use_container_width=True,
#     ):

#         success, status_code, message = (
#             api_client.check_api()
#         )

#         if success:

#             st.success(
#                 "API is running ✅"
#             )

#         else:

#             st.error(
#                 message
#             )

#     # ========================================================
#     # New Chat
#     # ========================================================

#     if st.button(
#         "➕ New Chat",
#         use_container_width=True,
#     ):

#         start_new_chat()

#         st.rerun()

#     st.divider()

#     # ========================================================
#     # Previous chats
#     # ========================================================

#     st.subheader("💬 Previous Chats")

#     conversations = get_all_conversations()

#     # --------------------------------------------------------
#     # Ensure newest first
#     # --------------------------------------------------------

#     conversations = sorted(
#         conversations,
#         key=lambda chat: (
#             chat["updated_at"]
#             if chat["updated_at"]
#             else ""
#         ),
#         reverse=True,
#     )

#     if conversations:

#         st.markdown(
#             '<div class="chat-history">',
#             unsafe_allow_html=True,
#         )

#         for conversation in conversations:

#             conversation_id = conversation["id"]

#             title = conversation["title"]

#             if not title:

#                 title = "New conversation"

#             title = title.strip()

#             if not title:

#                 title = "New conversation"

#             # ------------------------------------------------
#             # Individual chat row
#             # ------------------------------------------------

#             col1, col2 = st.columns(
#                 [6, 1],
#                 gap="small",
#             )

#             # ------------------------------------------------
#             # Open chat
#             # ------------------------------------------------

#             with col1:

#                 if st.button(
#                     f"💬 {title}",
#                     key=f"open_{conversation_id}",
#                     use_container_width=True,
#                 ):

#                     load_chat(
#                         conversation_id
#                     )

#                     st.rerun()

#             # ------------------------------------------------
#             # Delete chat
#             # ------------------------------------------------

#             with col2:

#                 if st.button(
#                     "🗑️",
#                     key=f"delete_{conversation_id}",
#                     help="Delete this chat",
#                 ):

#                     remove_chat(
#                         conversation_id
#                     )

#                     st.rerun()

#         st.markdown(
#             "</div>",
#             unsafe_allow_html=True,
#         )

#     else:

#         st.caption(
#             "No previous chats yet."
#         )


# # ============================================================
# # Current conversation
# # ============================================================

# for message in st.session_state.messages:

#     role = message.get(
#         "role",
#         "assistant",
#     )

#     content = message.get(
#         "content",
#         "",
#     )

#     if not content:
#         continue

#     with st.chat_message(
#         role
#     ):

#         st.markdown(
#             content
#         )


# # ============================================================
# # Chat input
# # ============================================================

# question = st.chat_input(
#     "Ask a follow-up question..."
# )


# # ============================================================
# # Process question
# # ============================================================

# if question:

#     question = question.strip()

#     if not question:

#         st.warning(
#             "Please enter a question."
#         )

#         st.stop()

#     # ========================================================
#     # Create chat ID
#     # ========================================================

#     if (
#         st.session_state.current_chat_id
#         is None
#     ):

#         st.session_state.current_chat_id = (
#             str(uuid.uuid4())
#         )

#     chat_id = (
#         st.session_state.current_chat_id
#     )

#     # ========================================================
#     # Save previous history before adding new question
#     # ========================================================

#     history = list(
#         st.session_state.messages
#     )

#     # ========================================================
#     # Add user message
#     # ========================================================

#     user_message = {
#         "role": "user",
#         "content": question,
#     }

#     st.session_state.messages.append(
#         user_message
#     )

#     # ========================================================
#     # Display user message
#     # ========================================================

#     with st.chat_message("user"):

#         st.markdown(
#             question
#         )

#     # ========================================================
#     # Save user message immediately
#     # ========================================================

#     save_conversation(
#         chat_id,
#         st.session_state.messages,
#     )

#     # ========================================================
#     # Call FastAPI + LangGraph
#     # ========================================================

#     with st.chat_message("assistant"):

#         with st.spinner(
#             "Thinking..."
#         ):

#             result = api_client.ask_question(
#                 question=question,
#                 history=history,
#             )

#         # ====================================================
#         # Successful response
#         # ====================================================

#         if result["success"]:

#             answer = result.get(
#                 "answer",
#                 "",
#             )

#             if not answer:

#                 answer = (
#                     "I could not generate an answer."
#                 )

#             st.markdown(
#                 answer
#             )

#             # ------------------------------------------------
#             # Add assistant message
#             # ------------------------------------------------

#             st.session_state.messages.append(
#                 {
#                     "role": "assistant",
#                     "content": answer,
#                 }
#             )

#             # ------------------------------------------------
#             # Save complete conversation
#             # ------------------------------------------------

#             save_conversation(
#                 chat_id,
#                 st.session_state.messages,
#             )

#         # ====================================================
#         # API error
#         # ====================================================

#         else:

#             error_message = result.get(
#                 "error",
#                 "Something went wrong.",
#             )

#             st.error(
#                 error_message
#             )

#             details = result.get(
#                 "details"
#             )

#             if details:

#                 if isinstance(
#                     details,
#                     dict,
#                 ):

#                     st.json(
#                         details
#                     )

#                 else:

#                     st.write(
#                         details
#                     )

#             # ------------------------------------------------
#             # Backend connection error
#             # ------------------------------------------------

#             if (
#                 result.get(
#                     "status_code"
#                 )
#                 is None
#             ):

#                 st.info(
#                     f"Make sure FastAPI is running at "
#                     f"{API_URL}"
#                 )



















import uuid

import streamlit as st

from app.config import API_URL
from app.api_client import api_client

from app.session_state import initialize_session_state, start_new_chat, load_chat, remove_chat

from app.database.connection import init_database, save_conversation, get_all_conversations


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="ThinkSmarter RAG",
    page_icon="🧠",
    layout="centered",
)



# ============================================================
# Custom CSS
# ============================================================



st.markdown(
    """
    <style>

    section[data-testid="stSidebar"] > div {
        height: 100vh;
    }

    .chat-history {
        max-height: 55vh;
        overflow-y: auto;
        padding-right: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Initialize database
# ============================================================

init_database()


# ============================================================
# Initialize session state
# ============================================================

initialize_session_state()


# ============================================================
# Header
# ============================================================

st.title("🧠 Think Smarter")

st.caption(
    "Ask questions and continue the conversation "
    "with your RAG system."
)


# ============================================================
# Check API connection automatically
# ============================================================

api_connected, api_status_code, api_message = (
    api_client.check_api()
)


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("⚙️ Configuration")

    st.caption(
        f"API: {API_URL}"
    )

    # ========================================================
    # API Status
    # ========================================================

    if api_connected:

        st.success(
            "API Connected",
            icon="🟢",
        )

    else:

        st.error(
            "API Offline",
            icon="🔴",
        )

    # ========================================================
    # New Chat
    # ========================================================

    if st.button(
        "➕ New Chat",
        use_container_width=True,
    ):

        start_new_chat()

        st.rerun()

    st.divider()

    # ========================================================
    # Previous chats
    # ========================================================

    st.subheader("💬 Previous Chats")

    conversations = get_all_conversations()

    # --------------------------------------------------------
    # Ensure newest first
    # --------------------------------------------------------

    conversations = sorted(
        conversations,
        key=lambda chat: (
            chat["updated_at"]
            if chat["updated_at"]
            else ""
        ),
        reverse=True,
    )

    if conversations:

        st.markdown(
            '<div class="chat-history">',
            unsafe_allow_html=True,
        )

        for conversation in conversations:

            conversation_id = conversation["id"]

            title = conversation["title"]

            if not title:
                title = "New conversation"

            title = title.strip()

            if not title:
                title = "New conversation"

            # ------------------------------------------------
            # Individual chat row
            # ------------------------------------------------

            col1, col2 = st.columns(
                [6, 1],
                gap="small",
            )

            # ------------------------------------------------
            # Open chat
            # ------------------------------------------------

            with col1:

                if st.button(
                    f"💬 {title}",
                    key=f"open_{conversation_id}",
                    use_container_width=True,
                ):

                    load_chat(
                        conversation_id
                    )

                    st.rerun()

            # ------------------------------------------------
            # Delete chat
            # ------------------------------------------------

            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{conversation_id}",
                    help="Delete this chat",
                ):

                    remove_chat(
                        conversation_id
                    )

                    st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    else:

        st.caption(
            "No previous chats yet."
        )


# ============================================================
# Current conversation
# ============================================================

for message in st.session_state.messages:

    role = message.get(
        "role",
        "assistant",
    )

    content = message.get(
        "content",
        "",
    )

    if not content:
        continue

    with st.chat_message(role):

        st.markdown(content)


# ============================================================
# Chat input
# ============================================================

question = st.chat_input(
    "Ask a follow-up question..."
)


# ============================================================
# Process question
# ============================================================

if question:

    question = question.strip()

    if not question:

        st.warning(
            "Please enter a question."
        )

        st.stop()

    # ========================================================
    # Check API before sending question
    # ========================================================

    if not api_connected:

        st.error(
            "API Offline. Please start FastAPI before asking a question.",
            icon="🔴",
        )

        st.stop()

    # ========================================================
    # Create chat ID
    # ========================================================

    if st.session_state.current_chat_id is None:

        st.session_state.current_chat_id = (
            str(uuid.uuid4())
        )

    chat_id = (
        st.session_state.current_chat_id
    )

    # ========================================================
    # Save previous history before adding new question
    # ========================================================

    history = list(
        st.session_state.messages
    )

    # ========================================================
    # Add user message
    # ========================================================

    user_message = {
        "role": "user",
        "content": question,
    }

    st.session_state.messages.append(
        user_message
    )

    # ========================================================
    # Display user message
    # ========================================================

    with st.chat_message("user"):

        st.markdown(
            question
        )

    # ========================================================
    # Save user message immediately
    # ========================================================

    save_conversation(
        chat_id,
        st.session_state.messages,
    )

    # ========================================================
    # Call FastAPI + LangGraph
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            result = api_client.ask_question(
                question=question,
                history=history,
            )

        # ====================================================
        # Successful response
        # ====================================================

        if result["success"]:

            answer = result.get(
                "answer",
                "",
            )

            if not answer:

                answer = (
                    "I could not generate an answer."
                )

            st.markdown(
                answer
            )

            # ------------------------------------------------
            # Add assistant message
            # ------------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            # ------------------------------------------------
            # Save complete conversation
            # ------------------------------------------------

            save_conversation(
                chat_id,
                st.session_state.messages,
            )

        # ====================================================
        # API error
        # ====================================================

        else:

            error_message = result.get(
                "error",
                "Something went wrong.",
            )

            st.error(
                error_message
            )

            details = result.get(
                "details"
            )

            if details:

                if isinstance(
                    details,
                    dict,
                ):

                    st.json(
                        details
                    )

                else:

                    st.write(
                        details
                    )

            # ------------------------------------------------
            # Backend connection error
            # ------------------------------------------------

            if (
                result.get("status_code")
                is None
            ):

                st.info(
                    f"Make sure FastAPI is running at "
                    f"{API_URL}"
                )











