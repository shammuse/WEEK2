import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    # Replace this with actual data loading logic
    df = pd.DataFrame({
        'Handset Type': ['iPhone', 'Samsung', 'Huawei', 'Xiaomi', 'Other'],
        'Count': [300, 250, 200, 150, 100]
    })
    return df

def show():
    st.title("User Overview")

    df = load_data()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Users", "1,000")
    col2.metric("Active Users", "850")
    col3.metric("Avg Session Duration", "25 min")
    col4.metric("Total Data Usage", "250 TB")

    st.subheader("Handset Manufacturers Distribution")
    fig = px.bar(df, x='Handset Type', y='Count', title="Handset Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Add more visualizations and insights here

