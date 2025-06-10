import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    url = "https://github.com/kwamearhinPORTFL/supermarket-dashboard/blob/main/supermarket_sales.csv"
    return pd.read_csv(url)

data = load_data()

# Clean column names (just in case)
data.columns = data.columns.str.strip()

# Convert date columns
data['Date'] = pd.to_datetime(data['Date'])
data['Month'] = data['Date'].dt.to_period('M')
data['Hour'] = pd.to_datetime(data['Time']).dt.hour

st.title("🛒 Supermarket Sales Dashboard")

# Filters
# === Sidebar Filters ===
st.sidebar.header("🔍 Filters")

# Branch filter
branch = st.sidebar.multiselect(
    "Select Branch:",
    options=data['Branch'].unique(),
    default=data['Branch'].unique()
)

# Gender filter
gender = st.sidebar.multiselect(
    "Select Gender:",
    options=data['Gender'].unique(),
    default=data['Gender'].unique()
)

# Product Line filter
product_lines = st.sidebar.multiselect(
    "Select Product Line:",
    options=data['Product line'].unique(),
    default=data['Product line'].unique()
)

# Payment Method filter
payment_methods = st.sidebar.multiselect(
    "Select Payment Method:",
    options=data['Payment'].unique(),
    default=data['Payment'].unique()
)

# Apply filters
filtered_data = data[
    (data['Branch'].isin(branch)) &
    (data['Gender'].isin(gender)) &
    (data['Product line'].isin(product_lines)) &
    (data['Payment'].isin(payment_methods))
]

# Filter data
filtered_data = data[(data['Branch'].isin(branch)) & (data['Gender'].isin(gender))]

# KPIs
total_sales = filtered_data['Total'].sum()
avg_rating = filtered_data['Rating'].mean()
gross_income = filtered_data['gross income'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Average Rating", f"{avg_rating:.2f}")
col3.metric("Gross Income", f"${gross_income:,.2f}")

st.markdown("---")

# Sales by product line
st.subheader("Total Sales by Product Line")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.barplot(data=filtered_data, x='Product line', y='Total', estimator=sum, ax=ax1)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
st.pyplot(fig1)

# Sales by hour
st.subheader("Sales by Hour of Day")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(data=filtered_data, x='Hour', y='Total', estimator=sum, ax=ax2)
st.pyplot(fig2)

# Customer loyalty
st.subheader("Customer Loyalty – Average Purchase")
fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.barplot(data=filtered_data, x='Customer type', y='Total', estimator='mean', ax=ax3)
st.pyplot(fig3)
# Customer loyalty
st.subheader("Customer Loyalty – Average Purchase")
# Pie Chart: Payment Method Distribution
st.subheader("💳 Payment Method Distribution")

payment_data = filtered_data['Payment'].value_counts()

fig4, ax4 = plt.subplots()
ax4.pie(payment_data, labels=payment_data.index, autopct='%1.1f%%', startangle=90)
ax4.axis('equal')  # Equal aspect ratio ensures the pie is circular.
st.pyplot(fig4)
# Download Button
st.markdown("---")
st.subheader("⬇️ Download Filtered Data")

csv = filtered_data.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name='filtered_supermarket_data.csv',
    mime='text/csv'
)

