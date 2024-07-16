import streamlit as st
import csv

# List of all the team members
TEAM = ["Alice", "Bob"]


def main():
    st.title("Commemoratif")

    # Ask user if they want to create a new record
    if st.button("Create new record"):
        create_record()

    # If not we display the existing records
    else:
        display_records()


def create_record():

    # Text inputs
    mise_en_culture_technicien = st.selectbox("Technicien", TEAM)
    mise_en_culture_ts = st.date_input("Date de mise en culture")

    # Slider inputs
    age = st.slider("Age", 0, 100, 25)
    rating = st.slider("Rating", 0.0, 10.0, 5.0)

    # Submit button
    if st.button("Submit"):
        # Create a new row with user inputs
        row = [name, email, age, rating]

        # Append the row to the CSV file
        with open("output.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)

        st.success("Form submitted successfully!")


if __name__ == "__main__":
    main()
