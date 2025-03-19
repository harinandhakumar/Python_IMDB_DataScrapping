import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Title of the app
st.title("Count of Movies for Each Genre (Bar Chart)")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display first few rows of the data to check its structure
    st.write(df.head())
    
    # Ensure necessary column 'Genre_Title' exists in the data
    if 'Genre_Title' in df.columns:
        
        # Count the number of movies for each genre
        genre_counts = df['Genre_Title'].value_counts().reset_index()
        genre_counts.columns = ['Genre_Title', 'Movie Count']
        
        # Create a bar chart of movie counts for each genre
        plt.figure(figsize=(12, 6))
        sns.barplot(data=genre_counts, x='Genre_Title', y='Movie Count', palette="viridis")
        
        # Add title and labels
        plt.title("Count of Movies for Each Genre")
        plt.xlabel("Genre")
        plt.ylabel("Number of Movies")
        plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
        
        # Add movie count annotations on top of bars
        for index, row in genre_counts.iterrows():
            plt.text(row.name, row['Movie Count'] + 0.2, int(row['Movie Count']), 
                     ha='center', color='black', fontweight='bold')
        
        # Show the bar chart in the Streamlit app
        st.pyplot(plt)
        
        # Display the summary of movie counts by genre
        st.subheader("Summary of Movie Counts by Genre:")
        st.write(genre_counts)
        
    else:
        st.error("The required column 'Genre_Title' is not present in the dataset.")
