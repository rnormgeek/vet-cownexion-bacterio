import sqlite3
import vetcownect.CONSTANTS as CONSTANTS


def check_db_exists() -> bool:
    """
    Check if the database exists.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(CONSTANTS.DATABASE_NAME)

        # Close the connection
        conn.close()

        return True
    except sqlite3.OperationalError:
        return False


def connect_to_db() -> sqlite3.Connection:
    """
    Connect to the SQLite database.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(CONSTANTS.DATABASE_NAME)

    return conn
