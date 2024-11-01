# streamlit_app.py

import streamlit as st
import pandas as pd

def main():
    st.title("CSV File Uploader")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Display the dataframe
        st.write("Dataframe:")
        st.dataframe(df)

if __name__ == "__main__":
    main()
