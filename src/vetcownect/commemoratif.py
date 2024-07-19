import streamlit as st
import vetcownect.db as db
import sqlite3
import utils
from vetcownect.log_config import get_logger
import vetcownect.CONSTANTS as CONSTANTS
from datetime import datetime
import os


def main() -> None:
    """
    Main function for the commemoratif module.

    Returns:
        None
    """
    logger.debug("Starting the main function")

    st.title("Commemoratifs")

    # First we check that the database exists
    if not db.check_db_exists():
        logger.info("Database does not exist. Creating a new one.")
        db.init_db()
        conn = db.connect_to_db()
        create_eleveur()
    else:
        conn = db.connect_to_db()

    # Display the existing records by default
    display_records(conn)
    # Maybe we'll want a smarter function here to let user filter records
    # And click on a record to see more details and actions (edit, delete)

    if st.button("Create new record"):
        create_record(conn)


def create_record(conn: sqlite3.Connection) -> None:
    """
    Create a new record in the database based on user inputs.

    Args:
        conn (sqlite3.Connection): SQLite database connection
    Returns:
        None
    """

    # User needs to select the eleveur: we use a selectbox
    eleveurs = db.get_eleveurs(conn)
    if not eleveurs:
        st.warning("No eleveurs found in the database. Please create one.")
        create_eleveur()
        eleveurs = db.get_eleveurs(conn)

    with st.form("create_record_form"):
        st.write("Create a new record")

        # User inputs
        eleveur = st.selectbox(
            "Eleveur", [utils.format_eleveur_for_selectbox(e) for e in eleveurs]
        )
        appel = st.radio("Appel", ["Fait", "Non fait"])
        mise_en_culture_technicien = st.selectbox("Technicien", CONSTANTS.TEAM)
        mise_en_culture_ts = st.date_input("Date de mise en culture")
        numero_vache = st.text_input("Numéro vache")
        rang_lactation = st.number_input("Rang de lactation", min_value=0)
        stade_lactation = st.radio(
            "Stade de lactation",
            ["Début", "Milieu", "Fin"],
        )
        quartier = st.radio(
            "Rang de lactation",
            [
                "Avant-gauche",
                "Avant-droit",
                "Arrière-gauche",
                "Arrière-droit",
                "Multiple",
            ],
        )
        chronicite = st.selectbox("Chronicité", ["Aiguë", "Chronique"])
        gravite = st.selectbox("Gravité", ["Bénigne", "Sévère"])
        commentaires = st.text_area("Commentaires")

        # Submit button
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Create a new row with user inputs
            mise_en_culture_ts = datetime.strptime(
                mise_en_culture_ts, "%Y-%m-%d %H:%M:%S"
            )

            row = [
                True if appel == "Fait" else False,
                mise_en_culture_technicien,
                mise_en_culture_ts,
                numero_vache,
                rang_lactation,
                stade_lactation,
                quartier,
                chronicite,
                gravite,
                commentaires,
                eleveur["eleveur_id"],
            ]

            # Write the row to the commemoratif table on the SQLite db
            db.insert_data(
                conn=conn,
                row=row,
                table="commemoratifs",
            )
            st.success("Record created successfully!")
            logger.info(f"Record created: {row}")


def create_eleveur(conn: sqlite3.Connection) -> None:
    """
    Create a new eleveur in the database based on user inputs.

    Args:
        conn (sqlite3.Connection): SQLite database connection
    Returns:
        None
    """

    with st.form("create_eleveur_form"):
        st.write("Create a new eleveur")
        # User inputs
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        adresse = st.text_input("Adresse")
        telephone = st.text_input("Téléphone")

        # Submit button
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Create a new row with user inputs
            row = [nom, prenom, adresse, telephone]

            # Write the row to the eleveur table on the SQLite db
            db.insert_data(conn=conn, row=row, table="eleveurs")
            st.success("Eleveur created successfully!")
            logger.info(f"Eleveur created: {row}")


def display_records(conn) -> None:
    """
    Display the existing records in the database.

    Args:
        conn (sqlite3.Connection): SQLite database connection
    Returns:
        None
    """

    # SQL command to select all rows from the commemoratif table
    select_rows_command = """
    SELECT * FROM commemoratifs
    """

    # Execute the SQL command
    cursor = conn.cursor()
    cursor.execute(select_rows_command)

    # Fetch all the rows
    rows = cursor.fetchall()

    # Display the rows in a table
    if rows:
        for row in rows:
            st.write(row)
    else:
        st.warning("No records found. Please create one.")


if __name__ == "__main__":

    # initialize logger
    logger = get_logger(__name__)

    logger.debug("Starting the commemoratif module")
    logger.debug(f"Current working directory: {os.getcwd()}")
    logger.debug(f"Database exists: {db.check_db_exists()}")
    logger.debug(f"Database name: {CONSTANTS.DATABASE_NAME}")

    main()

    # FIXME # ! for now each time we run streamlit, no rows are displayed.
    # Logs show that the module is run twice then three times etc...
    # There might be some issue with how we run the module (?)
