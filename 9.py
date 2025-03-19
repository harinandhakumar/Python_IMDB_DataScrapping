import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Title of the app
st.title("Average Ratings Across Genres (Heatmap)")

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
        
        # Group by 'Genre_Title' and calculate the average rating for each genre
        genre_avg_ratings = df.groupby('Genre_Title')['Rating'].mean().reset_index()
        
        # Pivot the data to have genres as rows and ratings as columns for heatmap comparison
        genre_avg_ratings_pivot = genre_avg_ratings.pivot_table(index='Genre_Title', values='Rating', aggfunc='mean')
        
        # Plot the heatmap
        plt.figure(figsize=(12, 8))
        heatmap = sns.heatmap(genre_avg_ratings_pivot.T, annot=True, cmap="YlGnBu", fmt=".2f", cbar_kws={'label': 'Average Rating'})
        plt.title("Average Ratings Across Genres")
        
        # Show the heatmap in the Streamlit app
        st.pyplot(plt)
        
    else:
        st.error("The required columns 'Genre_Title' and 'Rating' are not present in the dataset.")
