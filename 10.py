import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Function to convert voting counts (e.g., "1K" to 1000)
def convert_votes(value):
    if isinstance(value, str):
        value = value.strip().lower().replace(',', '')
        value = value.replace('(', '').replace(')', '')  # Remove brackets
        if 'k' in value:
            try:
                return float(value.replace('k', '')) * 1000
            except:
                return None
        else:
            try:
                return float(value)
            except:
                return None
    return value

# Title of the app
st.title("Ratings vs Voting Counts (Scatter Plot)")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display first few rows of the data to check its structure
    st.write(df.head())
    
    # Ensure necessary columns 'Rating' and 'Voting' exist in the data
    if 'Rating' in df.columns and 'Voting' in df.columns:
        
        # Convert 'Rating' to numeric (handle errors as NaN)
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        
        # Convert 'Voting' to numeric using the custom function
        df['Voting'] = df['Voting'].apply(convert_votes)
        
        # Drop rows where 'Rating' or 'Voting' is NaN
        df = df.dropna(subset=['Rating', 'Voting'])
        
        # Create a scatter plot of 'Rating' vs 'Voting'
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='Voting', y='Rating', color='blue', alpha=0.7)
        
        # Add title and labels
        plt.title("Scatter Plot: Ratings vs Voting Counts")
        plt.xlabel("Voting Counts")
        plt.ylabel("Ratings")
        
        # Show the scatter plot in the Streamlit app
        st.pyplot(plt)
        
    else:
        st.error("The required columns 'Rating' and 'Voting' are not present in the dataset.")
