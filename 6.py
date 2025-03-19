import pandas as pd
import streamlit as st

# Title of the app
st.title("Top-Rated Movie for Each Genre")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display first few rows of the data to check its structure
    st.write(df.head())
    
    # Ensure necessary columns 'Genre_Title' and 'Rating' exist in the data
    if 'Genre_Title' in df.columns and 'Rating' in df.columns:
        
        # Convert 'Rating' column to numeric, forcing errors to NaN
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        
        # Drop rows where 'Rating' is NaN after conversion
        df = df.dropna(subset=['Rating'])
        
        # Group by 'Genre_Title' and get the movie with the highest rating in each genre
        top_rated_movies = df.loc[df.groupby('Genre_Title')['Rating'].idxmax()]
        
        # Display the top-rated movies in a table, highlighting the highest-rated movie
        st.write("### Top-Rated Movie for Each Genre")
        
        # Highlighting the top-rated movie in the table with cyan color
        def highlight_top_rated(row, genre_max_ratings):
            genre = row['Genre_Title']
            genre_max_rating = genre_max_ratings.get(genre, None)
            return ['background-color: cyan' if row['Rating'] == genre_max_rating else '' for _ in row]

        # Get max ratings for each genre
        genre_max_ratings = top_rated_movies.groupby('Genre_Title')['Rating'].max().to_dict()

        # Apply styling
        top_rated_movies_style = top_rated_movies.style.apply(highlight_top_rated, axis=1, genre_max_ratings=genre_max_ratings)
        
        # Show the styled DataFrame in the Streamlit app
        st.write(top_rated_movies_style)
    else:
        st.error("The required columns 'Genre_Title' and 'Rating' are not present in the dataset.")
