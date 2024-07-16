import sqlite3
from vetcownect.log_config import get_logger
from vetcownect.utils import connect_to_db

# TODO: add the get_eleveurs function

# Logger
logger = get_logger(__name__)

# SQL command to create a table
create_eleveurs_table_command = """
CREATE TABLE IF NOT EXISTS eleveurs (
    eleveur_id integer PRIMARY KEY AUTOINCREMENT,
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
    resultat_id integer PRIMARY KEY AUTOINCREMENT,
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
    commemoratif_id integer PRIMARY KEY AUTOINCREMENT,
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


def init_db(conn: sqlite3.Connection):
    """Create the tables in the database."""

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


if __name__ == "__main__":
    conn = connect_to_db()
    init_db(conn)
