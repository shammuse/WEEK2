import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Set page config - must be the first Streamlit command
st.set_page_config(page_title="Telecom Analytics Dashboard", layout="wide")

# Load data (replace this with your actual data loading logic)
@st.cache_data  # Using the new caching command
def load_data():
    # Simulating data for demonstration
    np.random.seed(42)
    data = {
        'MSISDN': range(1000),
        'Handset Type': np.random.choice(['iPhone', 'Samsung', 'Huawei', 'Xiaomi', 'Other'], 1000),
        'Handset Manufacturer': np.random.choice(['Apple', 'Samsung', 'Huawei', 'Xiaomi', 'Other'], 1000),
        'Session ID': np.random.randint(1, 100, 1000),
        'Duration': np.random.randint(1, 120, 1000),
        'Total DL': np.random.randint(1, 1000, 1000),
        'Total UL': np.random.randint(1, 500, 1000),
        'TCP Retransmission': np.random.random(1000),
        'RTT': np.random.randint(10, 200, 1000),
        'Throughput': np.random.randint(1, 100, 1000),
    }
    df = pd.DataFrame(data)
    df['Total DL + UL'] = df['Total DL'] + df['Total UL']
    return df

df = load_data()

# Title
st.title("Telecom Analytics Dashboard")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["User Overview", "User Engagement", "Experience Analysis", "Satisfaction Analysis"])

if page == "User Overview":
    st.header("User Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Users", f"{len(df['MSISDN'].unique()):,}")
    col2.metric("Active Users", f"{len(df[df['Session ID'] > 0]['MSISDN'].unique()):,}")
    col3.metric("Average Session Duration", f"{df['Duration'].mean():.2f} min")
    col4.metric("Total Data Usage", f"{(df['Total DL'] + df['Total UL']).sum() / 1e6:.2f} TB")
    
    # Top 10 Handsets
    top_handsets = df['Handset Type'].value_counts().head(10)
    fig = px.bar(x=top_handsets.index, y=top_handsets.values, labels={'x': 'Handset', 'y': 'Count'})
    fig.update_layout(title="Top 10 Handsets")
    st.plotly_chart(fig, use_container_width=True)
    
    # Top 3 Manufacturers
    top_manufacturers = df['Handset Manufacturer'].value_counts().head(3)
    fig = px.pie(values=top_manufacturers.values, names=top_manufacturers.index, title="Top 3 Manufacturers")
    st.plotly_chart(fig, use_container_width=True)
    
    # Top 5 Handsets per Top 3 Manufacturer
    col1, col2, col3 = st.columns(3)
    for i, manufacturer in enumerate(top_manufacturers.index):
        top_handsets = df[df['Handset Manufacturer'] == manufacturer]['Handset Type'].value_counts().head(5)
        fig = px.bar(x=top_handsets.index, y=top_handsets.values, title=f"Top 5 Handsets - {manufacturer}")
        [col1, col2, col3][i].plotly_chart(fig, use_container_width=True)

elif page == "User Engagement":
    st.header("User Engagement")
    
    # Engagement Metrics
    engagement_metrics = df.groupby('MSISDN').agg({
        'Session ID': 'count',
        'Duration': 'sum',
        'Total DL + UL': 'sum'
    }).reset_index()
    
    # Normalize engagement metrics
    scaler = StandardScaler()
    engagement_normalized = scaler.fit_transform(engagement_metrics[['Session ID', 'Duration', 'Total DL + UL']])
    
    # K-means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    engagement_metrics['Cluster'] = kmeans.fit_predict(engagement_normalized)
    
    # Visualize clusters
    fig = px.scatter_3d(engagement_metrics, x='Session ID', y='Duration', z='Total DL + UL', color='Cluster',
                        title="User Engagement Clusters")
    st.plotly_chart(fig, use_container_width=True)
    
    # Top 10 engaged users
    st.subheader("Top 10 Engaged Users")
    top_engaged = engagement_metrics.sort_values('Total DL + UL', ascending=False).head(10)
    st.dataframe(top_engaged)
    
    # Top 3 most used applications (simulated)
    st.subheader("Top 3 Most Used Applications")
    app_usage = pd.DataFrame({
        'Application': ['Social Media', 'YouTube', 'Gaming'],
        'Usage': [45, 30, 25]
    })
    fig = px.pie(app_usage, values='Usage', names='Application', title="Application Usage")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Experience Analysis":
    st.header("Experience Analysis")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Average TCP Retransmission", f"{df['TCP Retransmission'].mean():.2%}")
    col2.metric("Average RTT", f"{df['RTT'].mean():.2f} ms")
    col3.metric("Average Throughput", f"{df['Throughput'].mean():.2f} Mbps")
    
    # TCP Retransmission Distribution
    fig = px.histogram(df, x='TCP Retransmission', title="TCP Retransmission Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    # RTT Distribution
    fig = px.histogram(df, x='RTT', title="Round Trip Time (RTT) Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    # Throughput by Handset Type
    throughput_by_handset = df.groupby('Handset Type')['Throughput'].mean().sort_values(ascending=False)
    fig = px.bar(x=throughput_by_handset.index, y=throughput_by_handset.values, 
                 labels={'x': 'Handset Type', 'y': 'Average Throughput (Mbps)'})
    fig.update_layout(title="Throughput by Handset Type")
    st.plotly_chart(fig, use_container_width=True)
    
    # Experience Clustering
    experience_metrics = df[['TCP Retransmission', 'RTT', 'Throughput']]
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Experience Cluster'] = kmeans.fit_predict(experience_metrics)
    
    fig = px.scatter_3d(df, x='TCP Retransmission', y='RTT', z='Throughput', color='Experience Cluster',
                        title="User Experience Clusters")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Satisfaction Analysis":
    st.header("Satisfaction Analysis")
    
    # Simulate satisfaction scores based on engagement and experience
    df['Engagement Score'] = (df['Duration'] + df['Total DL + UL']) / 2
    df['Experience Score'] = (100 - df['TCP Retransmission']*100 + (100 - df['RTT']) + df['Throughput']) / 3
    df['Satisfaction Score'] = (df['Engagement Score'] + df['Experience Score']) / 2
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Satisfaction Score", f"{df['Satisfaction Score'].mean():.2f}")
    col2.metric("Highly Satisfied Users", f"{(df['Satisfaction Score'] >= 75).mean():.1%}")
    col3.metric("Satisfaction Trend", "↑ 5%")
    
    # Satisfaction Distribution
    fig = px.histogram(df, x='Satisfaction Score', title="Satisfaction Score Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation between Engagement and Experience
    fig = px.scatter(df, x='Engagement Score', y='Experience Score', color='Satisfaction Score',
                     title="Engagement vs Experience")
    st.plotly_chart(fig, use_container_width=True)
    
    # Top 10 Satisfied Customers
    st.subheader("Top 10 Satisfied Customers")
    top_satisfied = df.nlargest(10, 'Satisfaction Score')[['MSISDN', 'Satisfaction Score', 'Engagement Score', 'Experience Score']]
    st.dataframe(top_satisfied)
    
    # Satisfaction Prediction (placeholder for actual model)
    st.subheader("Satisfaction Prediction")
    st.write("Here you would integrate your actual regression model to predict satisfaction scores.")
