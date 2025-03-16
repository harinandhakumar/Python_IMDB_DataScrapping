import streamlit as st
import pandas as pd
import plotly.express as px

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


# Streamlit App title
st.title("Top Rated Movies and Most Voted Movies")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    # Display the DataFrame
    st.subheader("Uploaded Data")
    st.dataframe(df)

    # Show summary
    st.subheader("Summary Statistics")
    st.write(df.describe())

    # Check available columns
    st.subheader("Column Names")
    st.write(df.columns.tolist())

    # Convert votes and ratings to numeric if needed
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Voting'] = df['Voting'].apply(convert_votes)
    print(df)

    # Drop rows with missing ratings or votes
    df_clean = df.dropna(subset=['Rating', 'Voting'])
    
    # Top 10 Movies by Votes
    top_voted = df.sort_values(by='Voting', ascending=False).head(10)
    st.subheader("Top 10 Movies by Voting")
    st.dataframe(top_voted[['Title', 'Rating', 'Voting']])

    # Plot - Top 10 Voted
    fig_votes = px.bar(top_voted, x='Title', y='Voting', title="Top 10 Movies by Voting", labels={'Title': 'Title', 'Voting': 'Voting'})
    st.plotly_chart(fig_votes)
    
    # Top 10 Movies by Rating
    top_rated = df.sort_values(by='Rating', ascending=False).head(10)
    # print(top_rated)
    st.subheader("Top 10 Movies by Rating")
    st.dataframe(top_rated[['Title', 'Rating', 'Voting']])

    # Plot - Top 10 Rated
    fig_rating = px.bar(top_rated, x='Title', y='Rating', title="Top 10 Movies by Rating", labels={'Title': 'Title', 'Rating': 'Rating'})
    st.plotly_chart(fig_rating)    
