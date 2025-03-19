import pandas as pd
import streamlit as st
import plotly.express as px

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


# Title of the app
st.title("Genres with the Highest Total Voting Counts")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    df['Voting'] = df['Voting'].apply(convert_votes)
    
    # Display first few rows of the data to check its structure
    st.write(df.head())
    
    # Ensure necessary columns 'Genre_Title' and 'Voting' exist in the data
    if 'Genre_Title' in df.columns and 'Voting' in df.columns:
                
        # Drop rows where 'Voting' is NaN after conversion
        df = df.dropna(subset=['Voting'])
        
        # Group by 'Genre_Title' and sum the total voting counts for each genre
        genre_voting_counts = df.groupby('Genre_Title')['Voting'].sum().reset_index()
        
        # Create a pie chart for genres with the highest total voting counts
        pie_fig = px.pie(genre_voting_counts, 
                         names='Genre_Title', 
                         values='Voting', 
                         title="Total Voting Counts by Genre",
                         color='Genre_Title', 
                         color_discrete_sequence=px.colors.qualitative.Set3)
        
        # Show the pie chart in the Streamlit app
        st.plotly_chart(pie_fig)
        
    else:
        st.error("The required columns 'Genre_Title' and 'Voting' are not present in the dataset.")
