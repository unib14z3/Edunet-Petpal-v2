from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from typing import Any

DB_PATH = os.getenv("PETPAL_DB_PATH", "petpal.db")


def get_connection(db_path: str | None = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str | None = None) -> None:
    conn = get_connection(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS knowledge_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            source TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()

    count = conn.execute("SELECT COUNT(*) AS count FROM knowledge_items").fetchone()["count"]
    if count == 0:
        seed_default_knowledge(conn)

    conn.commit()
    conn.close()


def seed_default_knowledge(conn: sqlite3.Connection) -> None:
    now = datetime.now(timezone.utc).isoformat()
    defaults = [
        {
            "title": "Pet care basics",
            "content": "Dogs and cats need fresh water, a regular feeding schedule, exercise, and routine veterinary checkups.",
            "tags": "pet-care,health",
            "source": "seed",
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "Adoption support",
            "content": "Adoption records, vaccination history, and emergency contacts should be stored in a secure knowledge base for staff and volunteers.",
            "tags": "adoption,records",
            "source": "seed",
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "IBM Orchestrate integration",
            "content": "This knowledge service exposes simple JSON endpoints that IBM Orchestrate can call over HTTPS behind a Cloudflare public endpoint.",
            "tags": "ibm,orchestrate,cloudflare",
            "source": "seed",
            "created_at": now,
            "updated_at": now,
        },
    ]
    conn.executemany(
        """
        INSERT INTO knowledge_items (title, content, tags, source, created_at, updated_at)
        VALUES (:title, :content, :tags, :source, :created_at, :updated_at)
        """,
        defaults,
    )


def create_knowledge_item(
    title: str,
    content: str,
    tags: str | None = None,
    source: str | None = None,
    db_path: str | None = None,
) -> dict[str, Any]:
    conn = get_connection(db_path)
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.execute(
        """
        INSERT INTO knowledge_items (title, content, tags, source, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, content, tags or "", source or "manual", now, now),
    )
    conn.commit()
    item_id = cursor.lastrowid
    row = conn.execute(
        "SELECT id, title, content, tags, source, created_at, updated_at FROM knowledge_items WHERE id = ?",
        (item_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else {}


def list_knowledge(limit: int = 10, offset: int = 0, db_path: str | None = None) -> list[dict[str, Any]]:
    conn = get_connection(db_path)
    rows = conn.execute(
        """
        SELECT id, title, content, tags, source, created_at, updated_at
        FROM knowledge_items
        ORDER BY updated_at DESC, id DESC
        LIMIT ? OFFSET ?
        """,
        (limit, offset),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def search_knowledge(query: str, limit: int = 10, db_path: str | None = None) -> list[dict[str, Any]]:
    conn = get_connection(db_path)
    search_term = f"%{query.strip()}%"
    rows = conn.execute(
        """
        SELECT id, title, content, tags, source, created_at, updated_at
        FROM knowledge_items
        WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
        ORDER BY updated_at DESC, id DESC
        LIMIT ?
        """,
        (search_term, search_term, search_term, limit),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_status(db_path: str | None = None) -> dict[str, Any]:
    conn = get_connection(db_path)
    count = conn.execute("SELECT COUNT(*) AS count FROM knowledge_items").fetchone()["count"]
    conn.close()
    return {"database": db_path or DB_PATH, "records": count, "status": "ready"}
