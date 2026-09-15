

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from app.config import DATABASE_PATH


# ============================================================
# Database connection
# ============================================================

def get_db_connection():

    database_path = Path(
        DATABASE_PATH
    )

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    conn = sqlite3.connect(
        str(database_path),
        check_same_thread=False,
    )

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# Initialize database
# ============================================================

def init_database():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            messages TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    conn.commit()

    conn.close()


# ============================================================
# Save conversation
# ============================================================

def save_conversation(
    conversation_id,
    messages,
):

    if not conversation_id:
        return

    if not messages:
        return

    # --------------------------------------------------------
    # Only save when there is actual content
    # --------------------------------------------------------

    has_message = any(
        message.get(
            "content",
            "",
        ).strip()
        for message in messages
    )

    if not has_message:
        return

    # --------------------------------------------------------
    # Generate title from first user message
    # --------------------------------------------------------

    title = "New conversation"

    for message in messages:

        if (
            message.get("role") == "user"
            and message.get(
                "content",
                "",
            ).strip()
        ):

            title = message[
                "content"
            ].strip()

            break

    # --------------------------------------------------------
    # Maximum 40 characters
    # --------------------------------------------------------

    title = title[:40]

    now = datetime.now().isoformat()

    serialized_messages = json.dumps(
        messages,
        ensure_ascii=False,
    )

    conn = get_db_connection()

    existing = conn.execute(
        """
        SELECT id
        FROM conversations
        WHERE id = ?
        """,
        (
            conversation_id,
        ),
    ).fetchone()

    # --------------------------------------------------------
    # Update existing conversation
    # --------------------------------------------------------

    if existing:

        conn.execute(
            """
            UPDATE conversations
            SET
                title = ?,
                messages = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                title,
                serialized_messages,
                now,
                conversation_id,
            ),
        )

    # --------------------------------------------------------
    # Insert new conversation
    # --------------------------------------------------------

    else:

        conn.execute(
            """
            INSERT INTO conversations (
                id,
                title,
                messages,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                conversation_id,
                title,
                serialized_messages,
                now,
                now,
            ),
        )

    conn.commit()

    conn.close()


# ============================================================
# Get all conversations
# ============================================================

def get_all_conversations():

    conn = get_db_connection()

    rows = conn.execute(
        """
        SELECT
            id,
            title,
            messages,
            created_at,
            updated_at
        FROM conversations
        ORDER BY updated_at DESC
        """
    ).fetchall()

    conn.close()

    return rows


# ============================================================
# Get one conversation
# ============================================================

def get_conversation(
    conversation_id,
):

    conn = get_db_connection()

    row = conn.execute(
        """
        SELECT
            id,
            title,
            messages,
            created_at,
            updated_at
        FROM conversations
        WHERE id = ?
        """,
        (
            conversation_id,
        ),
    ).fetchone()

    conn.close()

    return row


# ============================================================
# Delete conversation
# ============================================================

def delete_conversation(
    conversation_id,
):

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM conversations
        WHERE id = ?
        """,
        (
            conversation_id,
        ),
    )

    conn.commit()

    conn.close()