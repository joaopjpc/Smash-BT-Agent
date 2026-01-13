"""Apply SQL migrations in order."""
from __future__ import annotations

from beachbot import db as beach_db


def main() -> None:
    """Apply pending SQL migrations."""
    connection = beach_db.init_db(beach_db.DEFAULT_DB_PATH)
    connection.close()


if __name__ == "__main__":
    main()
