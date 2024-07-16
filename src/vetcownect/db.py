import sqlite3

# Define the database name
database_name = "bacterio_db.db"

# Connect to the SQLite database
conn = sqlite3.connect(database_name)

# Create a cursor object
cursor = conn.cursor()

# SQL command to create a table
create_commemoratif_table_command = """
CREATE TABLE IF NOT EXISTS commemoratif (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appel BOOLEAN NOT NULL,
    mise_en_culture_ts TIMESTAMP NOT NULL,
    mise_en_culture_technicien TEXT NOT NULL,
    FOREIGN KEY (eleveur_id) REFERENCES eleveurs (id),
    numero_vache TEXT,
    rang_lactation INTEGER,
    stade_lactation TEXT,
    quartier TEXT,
    chronocite TEXT,
    gravite TEXT,
    commentaires TEXT
);
"""

create_resultat_table_command = """
CREATE TABLE IF NOT EXISTS resultat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_resultat_ts TIMESTAMP NOT NULL,
    resultat TEXT NOT NULL,
    traitement_imm TEXT,
    traitement_inj TEXT,
    traitement_tar TEXT,
    commentaire TEXT,
    epidemio TEXT,
    prevention TEXT,
    FOREIGN KEY (commemoratif_id) REFERENCES commemoratif (id)
)
"""

create_eleveurs_table_command = """
CREATE TABLE IF NOT EXISTS eleveurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    societe TEXT,
    nom TEXT,
    prenom TEXT,
    adresse TEXT,
    telephone TEXT,
    email TEXT NOT NULL
)
"""


# Execute the SQL command
cursor.execute(create_commemoratif_table_command)

# Commit the changes
conn.commit()

# Close the database connection
conn.close()

print("Database initialized successfully.")
