import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    # Replace this with actual data loading logic
    df = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Score': [85, 82, 88, 86, 89, 87]
    })
    return df

def correlation_analysis():
    # Sample data for demonstration
    np.random.seed(42)
    df = pd.DataFrame({
        'Duration': np.random.randint(1, 120, 1000),
        'Total Data': np.random.randint(1, 1000, 1000),
        'TCP Retransmission': np.random.random(1000),
        'RTT': np.random.randint(10, 200, 1000),
        'Throughput': np.random.randint(1, 100, 1000),
    })
    
    correlation_matrix = df[['Duration', 'Total Data', 'TCP Retransmission', 'RTT', 'Throughput']].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, ax=ax)
    plt.title('Correlation Matrix of Key Metrics')
    
    return fig

def show():
    st.title("Satisfaction Analysis")

    df = load_data()

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Satisfaction Score", "8.5/10")
    col2.metric("Highly Satisfied Users", "65%")
    col3.metric("Satisfaction Trend", "↑ 5%")

    st.subheader("Satisfaction Score Trend")
    fig = px.line(df, x='Month', y='Score', title="Satisfaction Score Trend")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Correlation Analysis")
    corr_fig = correlation_analysis()
    st.pyplot(corr_fig)

    # Add more satisfaction analysis visualizations here

