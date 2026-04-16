import os
import psycopg2
from psycopg2.extras import RealDictCursor, Json
import uuid


def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS extractions (
                    id UUID PRIMARY KEY,
                    filename TEXT,
                    document_type TEXT,
                    result JSONB,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS api_keys (
                    key TEXT PRIMARY KEY,
                    name TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
        conn.commit()


def save_extraction(filename: str, result: dict, document_type: str) -> str:
    extraction_id = str(uuid.uuid4())
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO extractions (id, filename, document_type, result) VALUES (%s, %s, %s, %s)",
                (extraction_id, filename, document_type, Json(result))
            )
        conn.commit()
    return extraction_id


def get_extraction(extraction_id: str) -> dict | None:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, filename, document_type, result, created_at FROM extractions WHERE id = %s",
                (extraction_id,)
            )
            row = cur.fetchone()
    if not row:
        return None
    return {
        "id": str(row["id"]),
        "filename": row["filename"],
        "document_type": row["document_type"],
        "result": row["result"],
        "created_at": row["created_at"].isoformat(),
    }


def is_valid_api_key(key: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM api_keys WHERE key = %s", (key,))
            return cur.fetchone() is not None
