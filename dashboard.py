import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Business Sales Dashboard", layout="wide")

st.title("Business Sales Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Sample - Superstore.csv", encoding='latin1')
    # Convert Order Date to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    # Create Year and Month column
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month_name()
    # Check duplicates
    df.drop_duplicates(inplace=True)
    return df

df = load_data()

# Calculations for KPIs
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100

# Top level KPIs
st.header("Key Performance Indicators")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales", f"${total_sales:,.2f}")
with col2:
    st.metric("Total Profit", f"${total_profit:,.2f}")
with col3:
    st.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# Row 1: Sales Trend & Monthly Sales
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales Trend Over Time")
    fig, ax = plt.subplots(figsize=(8, 4))
    df.groupby('Year')['Sales'].sum().plot(kind='line', ax=ax, marker='o')
    ax.set_ylabel("Total Sales")
    ax.grid(True)
    st.pyplot(fig)

with col2:
    st.subheader("Monthly Sales")
    fig, ax = plt.subplots(figsize=(8, 4))
    df.groupby('Month')['Sales'].sum().plot(kind='bar', ax=ax, color='skyblue')
    ax.set_ylabel("Total Sales")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.divider()

# Row 2: Top Products by Sales & Profit
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Products by Sales")
    top_products_sales = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    top_products_sales.plot(kind='bar', ax=ax, color='lightgreen')
    ax.set_ylabel("Total Sales")
    plt.xticks(rotation=75)
    st.pyplot(fig)

with col2:
    st.subheader("Top 10 Products by Profit")
    top_products_profit = df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    top_products_profit.plot(kind='bar', ax=ax, color='orange')
    ax.set_ylabel("Total Profit")
    plt.xticks(rotation=75)
    st.pyplot(fig)

st.divider()

# Row 3: Profit by Segment & Ship Mode
col1, col2 = st.columns(2)

with col1:
    st.subheader("Profit by Customer Segment")
    fig, ax = plt.subplots(figsize=(8, 4))
    df.groupby('Segment')['Profit'].sum().plot(kind='bar', ax=ax, color='cornflowerblue')
    ax.set_ylabel("Total Profit")
    plt.xticks(rotation=0)
    st.pyplot(fig)

with col2:
    st.subheader("Profit by Shipping Mode")
    fig, ax = plt.subplots(figsize=(8, 4))
    df.groupby('Ship Mode')['Profit'].sum().plot(kind='bar', ax=ax, color='salmon')
    ax.set_ylabel("Total Profit")
    plt.xticks(rotation=0)
    st.pyplot(fig)

st.divider()

# Row 4: Discount vs Profit & Correlation Matrix
col1, col2 = st.columns(2)

with col1:
    st.subheader("Discount vs Profit")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(df['Discount'], df['Profit'], alpha=0.5, color='purple')
    ax.set_xlabel("Discount")
    ax.set_ylabel("Profit")
    ax.grid(True)
    st.pyplot(fig)

with col2:
    st.subheader("Correlation Matrix")
    fig, ax = plt.subplots(figsize=(8, 4))
    corr = df[['Sales','Profit','Discount','Quantity']].corr()
    sns.heatmap(corr, annot=True, ax=ax, cmap='coolwarm')
    st.pyplot(fig)

st.divider()

# Data Tables
st.header("Data Breakdown")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Region Sales & Profit")
    region_data = df.groupby('Region').agg({'Sales':'sum','Profit':'sum'})
    region_data['Profit Margin (%)'] = (region_data['Profit']/region_data['Sales'])*100
    st.dataframe(region_data.style.format("{:.2f}"))

with col2:
    st.subheader("Category Sales & Profit")
    cat_data = df.groupby('Category').agg({'Sales':'sum','Profit':'sum'})
    cat_data['Profit Margin (%)'] = (cat_data['Profit']/cat_data['Sales'])*100
    st.dataframe(cat_data.style.format("{:.2f}"))

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Yearly Sales Growth")
    year_sales = df.groupby('Year')['Sales'].sum()
    growth = year_sales.pct_change() * 100
    growth_df = pd.DataFrame({'Sales': year_sales, 'Growth (%)': growth}).fillna(0)
    st.dataframe(growth_df.style.format("{:.2f}"))

with col2:
    st.subheader("Bottom 10 Products by Profit")
    bottom_products = df.groupby('Product Name')['Profit'].sum().sort_values().head(10).reset_index()
    st.dataframe(bottom_products.style.format({'Profit': "{:.2f}"}))

st.divider()

st.header("Key Business Questions & Insights")

# 1. Which products generate the most revenue?
st.subheader("1. Which products generate the most revenue?")
top_revenue_product = df.groupby('Product Name')['Sales'].sum().idxmax()
top_revenue_amount = df.groupby('Product Name')['Sales'].sum().max()
st.write(f"The product that generates the most revenue is **{top_revenue_product}** with total sales of **${top_revenue_amount:,.2f}**.")
st.write("Other top revenue-generating products include:")
st.dataframe(df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5).reset_index().style.format({'Sales': "${:,.2f}"}))

# 2. Which regions are most profitable?
st.subheader("2. Which regions are most profitable?")
top_region = region_data['Profit'].idxmax()
top_region_profit = region_data['Profit'].max()
st.write(f"The **{top_region}** region is the most profitable, generating **${top_region_profit:,.2f}** in total profit.")

# 3. How do sales change over time?
st.subheader("3. How do sales change over time?")
st.write("Sales have shown an overall positive trend over the years from 2014 to 2017. There was a slight dip in 2015, but sales rebounded strongly in 2016 and peaked in 2017. Looking at the monthly data, sales tend to peak heavily towards the end of the year (November and December) and have a secondary peak in September, indicating strong seasonality.")

# 4. Which categories perform best in terms of profit margin?
st.subheader("4. Which categories perform best in terms of profit margin?")
top_margin_category = cat_data['Profit Margin (%)'].idxmax()
top_margin = cat_data['Profit Margin (%)'].max()
st.write(f"The **{top_margin_category}** category performs best in terms of profit margin at **{top_margin:.2f}%**.")

# 5. Where should the business focus to achieve faster growth?
st.subheader("5. Where should the business focus to achieve faster growth?")
st.markdown("""
Based on the data, the business should focus on the following strategies for faster growth:
*   **Double down on Technology:** Technology products yield the highest profit margins (17.40%), making them highly lucrative. Promoting these items heavily should accelerate profit growth.
*   **Optimize or Discontinue Unprofitable Products:** A significant chunk of profit is lost to underperforming products like *Cubify CubeX 3D Printers*. Identifying the root cause (e.g., high discounts, low margins, or high shipping costs) and either fixing it or discontinuing the products will immediately improve the bottom line.
*   **Investigate Discount Strategies:** The "Discount vs Profit" chart clearly shows that high discounts often lead to negative profits. The business should re-evaluate its discounting strategy to find the sweet spot that drives volume without eroding profit.
*   **Leverage Seasonality:** Sales spike in Q4 (especially November and December). Focusing marketing efforts and ensuring sufficient inventory ahead of these peak months can maximize revenue.
*   **Expand in the East and West Regions:** These regions currently bring in the most profit. Analyzing what works well there and replicating those strategies in the Central and South regions (or focusing expansion budgets on the top regions) can drive growth.
""")
