import streamlit as st
import csv


def main():
    st.title("Form App")

    # Text inputs
    name = st.text_input("Name")
    email = st.text_input("Email")

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
