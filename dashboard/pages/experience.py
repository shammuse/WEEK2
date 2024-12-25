import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    # Replace this with actual data loading logic
    df = pd.DataFrame({
        'Handset': ['iPhone 13', 'Samsung S21', 'Huawei P40', 'Xiaomi Mi 11', 'Others'],
        'Throughput': [85, 82, 78, 76, 70]
    })
    return df

def show():
    st.title("Experience Analysis")

    df = load_data()

    col1, col2, col3 = st.columns(3)
    col1.metric("Average RTT", "120ms")
    col2.metric("TCP Retransmission Rate", "2.5%")
    col3.metric("Average Throughput", "25 Mbps")

    st.subheader("Throughput by Handset Type")
    fig = px.bar(df, x='Handset', y='Throughput', title="Throughput by Handset Type")
    st.plotly_chart(fig, use_container_width=True)

    # Add more experience analysis visualizations here