import pandas as pd
import streamlit as st
import plotly.express as px

# Title of the app
st.title("Movie Ratings Distribution")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display first few rows of the data to check its structure
    st.write(df.head())
    
    # Ensure necessary column 'Rating' exists in the data
    if 'Rating' in df.columns:
        
        # Convert 'Rating' column to numeric, forcing errors to NaN
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        
        # Drop rows where 'Rating' is NaN after conversion
        df = df.dropna(subset=['Rating'])
        
        # Create a histogram for movie ratings
        hist_fig = px.histogram(df, 
                                 x='Rating', 
                                 title="Distribution of Movie Ratings",
                                 labels={'Rating': 'Movie Rating'},
                                 nbins=20)  # Number of bins for the histogram

        # Show the histogram in the Streamlit app
        st.plotly_chart(hist_fig)

        # Optionally, create a boxplot for movie ratings
        box_fig = px.box(df, 
                         y='Rating', 
                         title="Boxplot of Movie Ratings",
                         labels={'Rating': 'Movie Rating'})

        # Show the boxplot in the Streamlit app
        st.plotly_chart(box_fig)
        
    else:
        st.error("The required column 'Rating' is not present in the dataset.")
