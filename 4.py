import pandas as pd
import streamlit as st
import plotly.express as px

# Title of the app
st.title("Average Voting Count Across Different Genres")

# Define the convert_votes function to clean and convert the voting data
def convert_votes(value):
    if isinstance(value, str):
        value = value.strip().lower().replace(',', '')  # Remove commas and spaces
        value = value.replace('(', '').replace(')', '')  # Remove brackets
        if 'k' in value:
            try:
                return float(value.replace('k', '')) * 1000  # Convert 'k' to 1000
            except:
                return None
        else:
            try:
                return float(value)  # Convert to float if not 'k'
            except:
                return None
    return value

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Apply the convert_votes function to the 'Voting' column to clean and convert values
    df['Voting'] = df['Voting'].apply(convert_votes)
    
    # Display first few rows of the data to check its structure
    st.write(df.head())
    
    # Ensure necessary columns exist in the data
    if 'Genre_Title' in df.columns and 'Voting' in df.columns:
        
        # Drop rows where 'Voting' is NaN after conversion
        df = df.dropna(subset=['Voting'])
        
        # Grouping data by genre and calculating the average voting count
        genre_avg_voting = df.groupby('Genre_Title')['Voting'].mean().reset_index()

        # Sorting the data for better visualization
        genre_avg_voting = genre_avg_voting.sort_values('Voting', ascending=False)

        # Create an interactive bar chart using Plotly Express
        fig = px.bar(genre_avg_voting, 
                     x='Voting', 
                     y='Genre_Title', 
                     orientation='h',
                     title="Average Voting Count by Genre",
                     labels={'Voting': 'Average Voting', 'Genre_Title': 'Genre Title'},
                     color='Voting',
                     color_continuous_scale='Viridis')

        # Show the plot in the Streamlit app
        st.plotly_chart(fig)
    else:
        st.error("The required columns 'Genre_Title' and 'Voting' are not present in the dataset.")
