import streamlit as st
import sqlite3
import vetcownect.db as db
from vetcownect.utils import connect_to_db, check_db_exists
from vetcownect.log_config import get_logger
from vetcownect.CONSTANTS import TEAM

# Logger
logger = get_logger(__name__)


def main():
    st.title("Commemoratifs")

    # First we check that the database exists
    if not check_db_exists():
        db.init_db()

    # Ask user if they want to create a new record
    if st.button("Create new record"):
        create_record()

    # If not we display the existing records
    else:
        display_records()


def create_record():
    """Create a new record in the database based on user inputs."""

    with st.form("create_record_form"):
        st.write("Create a new record")
        # User inputs
        mise_en_culture_technicien = st.selectbox("Technicien", TEAM)
        mise_en_culture_ts = st.date_input("Date de mise en culture")
        numero_vache = st.text_input("Numéro vache")
        rang_lactation = st.number_input("Rang de lactation", min_value=0)
        stade_lactation = st.radio("Stade de lactation", ["Début", "Milieu", "Fin"])
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

        # User needs to select the eleveur: we use a selectbox
        eleveur = st.selectbox("Eleveur", db.get_eleveurs())

        # Submit button
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Create a new row with user inputs
            row = [
                mise_en_culture_technicien,
                mise_en_culture_ts,
                numero_vache,
                rang_lactation,
                stade_lactation,
                quartier,
                chronicite,
                gravite,
            ]

            # Write the row to the commemoratif table on the SQLite db
            try:
                conn = connect_to_db()
                write_commemoratif_row(row, conn)
                st.success("Record created successfully!")
                logger.info(f"Record created: {row}")

            except sqlite3.Error as e:
                st.error(f"Error: {e}")
                logger.error(f"Error: {e}")


def write_commemoratif_row(row: list, conn: sqlite3.Connection) -> None:
    """
    Write a new row to the commemoratifs table.
    """
    cursor = conn.cursor()

    # SQL command to insert a row
    insert_row_command = """
    INSERT INTO commemoratifs (
        mise_en_culture_technicien,
        mise_en_culture_ts,
        numero_vache,
        rang_lactation,
        stade_lactation,
        quartier,
        chronicite,
        gravite
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    # Execute the SQL command
    cursor.execute(insert_row_command, row)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()


def display_records():
    """Display the existing records in the database."""

    # Connect to the SQLite database
    conn = connect_to_db()
    cursor = conn.cursor()

    # SQL command to select all rows from the commemoratif table
    select_rows_command = """
    SELECT * FROM commemoratifs
    """

    # Execute the SQL command
    cursor.execute(select_rows_command)

    # Fetch all rows
    rows = cursor.fetchall()

    # Display the rows
    for row in rows:
        st.write(row)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
