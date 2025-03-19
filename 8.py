import pandas as pd
import streamlit as st
import re

# Title of the app
st.title("Shortest and Longest Movies")

def duration_to_minutes(duration_str):
    if isinstance(duration_str, str):
        hours = 0
        minutes = 0
        match = re.findall(r'(\d+)\s*h', duration_str.lower())
        if match:
            hours = int(match[0])
        match = re.findall(r'(\d+)\s*m', duration_str.lower())
        if match:
            minutes = int(match[0])
        return hours * 60 + minutes
    return None

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display first few rows of the data to check its structure
    st.write(df.head())
    
    # Ensure necessary columns 'Duration' and 'Title' exist in the data
    if 'Duration' in df.columns and 'Title' in df.columns:
        
        df['Duration'] = df['Duration'].apply(duration_to_minutes)
        
        # Drop rows where 'Duration' is NaN after conversion
        df = df.dropna(subset=['Duration'])
        df = df[df['Duration'] > 0]
        
        # Find the shortest and longest movies based on 'Duration'
        shortest_movie = df.loc[df['Duration'].idxmin()]
        longest_movie = df.loc[df['Duration'].idxmax()]
        
        # Display the shortest movie in a card
        st.markdown(
            f"""
            <div style="background-color: lightblue; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                <h3 style="text-align: center;">Shortest Movie</h3>
                <p><strong>Title:</strong> {shortest_movie['Title']}</p>
                <p><strong>Duration:</strong> {shortest_movie['Duration']} minutes</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Display the longest movie in a card
        st.markdown(
            f"""
            <div style="background-color: lightgreen; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                <h3 style="text-align: center;">Longest Movie</h3>
                <p><strong>Title:</strong> {longest_movie['Title']}</p>
                <p><strong>Duration:</strong> {longest_movie['Duration']} minutes</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    else:
        st.error("The required columns 'Duration' and 'Title' are not present in the dataset.")
