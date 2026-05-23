import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/ecommerce_sales_data.csv")

    # Convert date
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

    # Create total sales
    df['Total Sales'] = df['Quantity'] * df['Price']

    # Create month/year columns
    df['Month'] = df['Order Date'].dt.month_name()
    df['Year'] = df['Order Date'].dt.year

    return df

df = load_data()

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("📌 Filters")

city_filter = st.sidebar.multiselect(
    "Select City",
    options=df['City'].unique(),
    default=df['City'].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df['Product Category'].unique(),
    default=df['Product Category'].unique()
)

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

payment_filter = st.sidebar.multiselect(
    "Payment Method",
    options=df['Payment Method'].unique(),
    default=df['Payment Method'].unique()
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = df[
    (df['City'].isin(city_filter)) &
    (df['Product Category'].isin(category_filter)) &
    (df['Gender'].isin(gender_filter)) &
    (df['Payment Method'].isin(payment_filter))
]

# ---------------------------------------------------
# DASHBOARD TITLE
# ---------------------------------------------------

st.title("🛒 E-Commerce Sales Analytics Dashboard")

st.markdown("### Business Insights & Sales Performance")

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

total_sales = filtered_df['Total Sales'].sum()
total_orders = filtered_df['Order ID'].nunique()
avg_rating = filtered_df['Rating'].mean()
avg_order_value = filtered_df['Total Sales'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"₹ {total_sales:,.0f}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("⭐ Avg Rating", round(avg_rating, 2))
col4.metric("🛍 Avg Order Value", f"₹ {avg_order_value:,.0f}")

st.divider()

# ---------------------------------------------------
# SALES BY CATEGORY
# ---------------------------------------------------

category_sales = filtered_df.groupby(
    'Product Category'
)['Total Sales'].sum().reset_index()

fig1 = px.bar(
    category_sales,
    x='Product Category',
    y='Total Sales',
    color='Product Category',
    title="Sales by Product Category",
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# MONTHLY SALES TREND
# ---------------------------------------------------

monthly_sales = filtered_df.groupby(
    'Month'
)['Total Sales'].sum().reset_index()

month_order = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]

monthly_sales['Month'] = pd.Categorical(
    monthly_sales['Month'],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values('Month')

fig2 = px.line(
    monthly_sales,
    x='Month',
    y='Total Sales',
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# CITY-WISE SALES
# ---------------------------------------------------

city_sales = filtered_df.groupby(
    'City'
)['Total Sales'].sum().reset_index()

fig3 = px.pie(
    city_sales,
    names='City',
    values='Total Sales',
    title="City-wise Sales Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# PAYMENT METHOD ANALYSIS
# ---------------------------------------------------

payment_data = filtered_df['Payment Method'].value_counts().reset_index()

payment_data.columns = ['Payment Method', 'Count']

fig4 = px.bar(
    payment_data,
    x='Payment Method',
    y='Count',
    color='Payment Method',
    title="Payment Method Usage",
    text_auto=True
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# TOP SELLING PRODUCTS
# ---------------------------------------------------

top_products = filtered_df.groupby(
    'Product Name'
)['Quantity'].sum().reset_index()

top_products = top_products.sort_values(
    by='Quantity',
    ascending=False
).head(10)

fig5 = px.bar(
    top_products,
    x='Product Name',
    y='Quantity',
    color='Quantity',
    title="Top 10 Best Selling Products",
    text_auto=True
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------

st.subheader("📄 Filtered Dataset")

st.dataframe(filtered_df)

# ---------------------------------------------------
# DOWNLOAD BUTTON
# ---------------------------------------------------

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name='filtered_sales_data.csv',
    mime='text/csv'
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")
st.markdown(
    "Developed using Python, Streamlit, Plotly & Pandas 🚀"
)