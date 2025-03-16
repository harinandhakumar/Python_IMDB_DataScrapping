import streamlit as st
import pandas as pd
import plotly.express as px
import re

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


st.title("Duration Insights Across Genres")

uploaded_file = st.file_uploader("Upload 2024 Movies CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head(10))

    st.subheader("Available Columns")
    st.write(df.columns.tolist())

    # Rename columns if needed
    genre_col = 'Genre_Title'    # Adjust if different
    duration_col = 'Duration'  # Adjust if different

    # Drop rows with missing genre or duration
    df_clean = df.dropna(subset=[genre_col, duration_col])

    # Convert duration to numeric
    df['Duration'] = df[duration_col].apply(duration_to_minutes)

    # Drop any rows with NaN duration after conversion
    df_clean = df_clean.dropna(subset=[duration_col])

    # Split multiple genres and explode into rows
    df_genre_expanded = df.assign(
        Genre=df[genre_col].str.split(',')).explode('Genre_Title')
    df_genre_expanded['Genre_Title'] = df_genre_expanded['Genre_Title'].str.strip()
    print(df_genre_expanded)

    # Group by Genre and compute average duration
    genre_duration = df_genre_expanded.groupby('Genre_Title')[duration_col].mean().reset_index()
    genre_duration.columns = ['Genre_Title', 'Average Duration (min)']
    genre_duration = genre_duration.sort_values(by='Average Duration (min)', ascending=False)

    st.subheader("Average Duration by Genre")
    st.dataframe(genre_duration)

    # Plot bar chart
    fig_duration = px.bar(genre_duration, x='Genre_Title', y='Average Duration (min)',
                          title="Average Movie Duration per Genre_Title",
                          text='Average Duration (min)',
                          labels={'Average Duration (min)': 'Avg Duration (min)'})
    st.plotly_chart(fig_duration)
