"""SQLite persistence for conversations, trials, and handoff tickets."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable


SCHEMA = (
    "CREATE TABLE IF NOT EXISTS conversations ("
    "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "  role TEXT NOT NULL,"
    "  content TEXT NOT NULL,"
    "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ");",
    "CREATE TABLE IF NOT EXISTS trial_requests ("
    "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "  name TEXT NOT NULL,"
    "  phone TEXT NOT NULL,"
    "  preferred_time TEXT NOT NULL,"
    "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ");",
    "CREATE TABLE IF NOT EXISTS handoff_tickets ("
    "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "  topic TEXT NOT NULL,"
    "  details TEXT NOT NULL,"
    "  status TEXT NOT NULL DEFAULT 'open',"
    "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ");",
)


def init_db(path: Path) -> sqlite3.Connection:
    """Create the SQLite database file and required tables."""
    connection = sqlite3.connect(path)
    for statement in SCHEMA:
        connection.execute(statement)
    connection.commit()
    return connection


def log_message(connection: sqlite3.Connection, role: str, content: str) -> None:
    """Store a message in the conversation history."""
    connection.execute(
        "INSERT INTO conversations (role, content) VALUES (?, ?)",
        (role, content),
    )
    connection.commit()


def record_trial_request(
    connection: sqlite3.Connection,
    name: str,
    phone: str,
    preferred_time: str,
) -> None:
    """Persist a trial lesson request."""
    connection.execute(
        "INSERT INTO trial_requests (name, phone, preferred_time) VALUES (?, ?, ?)",
        (name, phone, preferred_time),
    )
    connection.commit()


def create_handoff_ticket(
    connection: sqlite3.Connection,
    topic: str,
    details: str,
) -> None:
    """Open a ticket for a human follow-up."""
    connection.execute(
        "INSERT INTO handoff_tickets (topic, details) VALUES (?, ?)",
        (topic, details),
    )
    connection.commit()
