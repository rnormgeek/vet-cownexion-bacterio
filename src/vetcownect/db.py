import sqlite3
import vetcownect.CONSTANTS as CONSTANTS
from vetcownect.log_config import get_logger

# Initialize the logger
logger = get_logger(__name__)


# SQL command to create a table
create_eleveurs_table_command = """
CREATE TABLE IF NOT EXISTS eleveurs (
    eleveur_id integer PRIMARY KEY,
    societe text,
    nom text,
    prenom text,
    adresse text,
    telephone text,
    email text NOT NULL
)
"""

create_resultat_table_command = """
CREATE TABLE IF NOT EXISTS resultats (
    resultat_id integer PRIMARY KEY,
    date_resultat_ts timestamp NOT NULL,
    resultat text NOT NULL,
    traitement_imm text,
    traitement_inj text,
    traitement_tar text,
    commentaire text,
    epidemio text,
    prevention text,
    commemoratif_id integer,
    FOREIGN KEY (commemoratif_id)
        REFERENCES commemoratifs (commemoratif_id)
)
"""

create_commemoratif_table_command = """
CREATE TABLE IF NOT EXISTS commemoratifs (
    commemoratif_id integer PRIMARY KEY,
    appel boolean NOT NULL,
    mise_en_culture_ts timestamp NOT NULL,
    mise_en_culture_technicien text NOT NULL,
    numero_vache text,
    rang_lactation integer,
    stade_lactation text,
    quartier text,
    chronicite text,
    gravite text,
    commentaires text,
    eleveur_id integer NOT NULL,
    FOREIGN KEY (eleveur_id)
        REFERENCES eleveurs (eleveur_id)
);
"""


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


def init_db(conn: sqlite3.Connection):
    """
    Create the tables in the database.

    Args:
        conn (sqlite3.Connection): SQLite database connection

    Returns:
        None
    """

    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")
    conn.commit()

    # Create the eleveurs table
    print("Creating eleveurs table...")
    conn.execute(create_eleveurs_table_command)
    conn.commit()

    # Create the commemoratif table
    print("Creating commemoratif table...")
    conn.execute(create_commemoratif_table_command)
    conn.commit()

    # Create the resultat table
    print("Creating resultat table...")
    conn.execute(create_resultat_table_command)
    conn.commit()

    # Close the connection
    conn.close()

    logger.info("Tables created successfully.")


def insert_data(conn: sqlite3.Connection, row: tuple, table: str) -> None:
    """
    Create a new row in the target table.

    Args:
        conn (sqlite3.Connection): SQLite database connection
        row (tuple): Data to insert
        table (str): Target table

    Returns:
        None
    """
    cursor = conn.cursor()

    # First we check the table exists
    try:
        info = cursor.execute(f"PRAGMA table_info({table});")
        info.fetchall()

    except sqlite3.OperationalError:
        logger.error(f"Table {table} does not exist.")
        return

    # info is a list
    columns = [column[1] for column in info]

    # SQL command to insert a row
    insert_row_command = f"""
    INSERT INTO {table} ({", ".join(columns[1:])})
    VALUES ({", ".join(["?" for _ in range(len(columns[1:]))])})
    """

    # Execute the SQL command
    cursor.execute(insert_row_command, row)

    # Commit the changes
    conn.commit()


def get_eleveur(conn: sqlite3.Connection, eleveur_id: int) -> tuple:
    """
    Get the eleveur with the given ID.

    Args:
        conn (sqlite3.Connection): SQLite database connection
        eleveur_id (int): Eleveur ID

    Returns:
        dict: Eleveur data
    """
    cursor = conn.cursor()

    # SQL command to select the eleveur with the given ID
    select_eleveur_command = """
    SELECT * FROM eleveurs
    WHERE eleveur_id = ?
    """

    # Execute the SQL command
    cursor.execute(select_eleveur_command, (eleveur_id,))

    # Fetch the row
    eleveur = cursor.fetchone()

    # convert the tuple to a dictionary
    # we use the column names as key
    colnames = cursor.execute("PRAGMA table_info(eleveurs);")
    colnames = [col[1] for col in colnames]

    eleveur = dict(zip(colnames, eleveur))

    return eleveur


def get_eleveurs(conn: sqlite3.Connection) -> list:
    """
    Get all the eleveurs in the database.

    Args:
        conn (sqlite3.Connection): SQLite database connection

    Returns:
        list: List of eleveurs
    """
    cursor = conn.cursor()

    # SQL command to select all rows from the eleveurs table
    select_eleveurs_command = """
    SELECT * FROM eleveurs
    """

    # Execute the SQL command
    cursor.execute(select_eleveurs_command)

    # Fetch all rows
    eleveurs = cursor.fetchall()

    # Convert the list of tuples to a list of dictionaries
    colnames = cursor.execute("PRAGMA table_info(eleveurs);")
    colnames = [col[1] for col in colnames]

    eleveurs = [dict(zip(colnames, eleveur)) for eleveur in eleveurs]

    return eleveurs


if __name__ == "__main__":
    conn = connect_to_db()
    init_db(conn)
