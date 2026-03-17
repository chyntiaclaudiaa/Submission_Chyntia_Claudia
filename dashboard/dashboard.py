import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="E-Commerce Performance Insights",
    page_icon="📊",
    layout="wide"
)

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

all_df = load_data()

with st.sidebar:
    st.title("📊 Business Analytics")
    st.markdown("This dashboard analyzes the performance of the E-Commerce Public Dataset.")
    
    min_date = all_df["order_purchase_timestamp"].min()
    max_date = all_df["order_purchase_timestamp"].max()
    
    start_date, end_date = st.date_input(
        "Select Date Range:",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

st.title("E-Commerce Intelligence Dashboard 🚀")
st.info(f"Analyzing data from **{start_date}** to **{end_date}**")

tab_overview, tab_product, tab_rfm = st.tabs(["📈 Business Overview", "📦 Product Analytics", "💎 Customer RFM"])

with tab_overview:
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Orders", f"{main_df.order_id.nunique():,}")
    with m2:
        st.metric("Total Revenue", f"R$ {main_df.payment_value.sum():,.0f}")
    with m3:
        order_count = main_df.order_id.nunique()
        aov = main_df.payment_value.sum() / order_count if order_count > 0 else 0
        st.metric("Avg Order Value", f"R$ {aov:,.2f}")
    with m4:
        st.metric("Unique Customers", f"{main_df.customer_unique_id.nunique():,}")

    st.subheader("Revenue Trend Over Time")
    daily_revenue = main_df.resample(rule='D', on='order_purchase_timestamp').agg({"payment_value": "sum"}).reset_index()
    
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(daily_revenue["order_purchase_timestamp"], daily_revenue["payment_value"], color="#1f77b4", linewidth=1.5)
    ax.fill_between(daily_revenue["order_purchase_timestamp"], daily_revenue["payment_value"], color="#1f77b4", alpha=0.1)
    ax.set_ylabel("Revenue (R$)")
    st.pyplot(fig)

with tab_product:
    st.subheader("Product Performance Analysis")
    
    product_sales = main_df.groupby("product_category_name").order_id.nunique().sort_values(ascending=False).reset_index()
    product_revenue = main_df.groupby("product_category_name").payment_value.sum().sort_values(ascending=False).reset_index()
    
    blue_palette = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("#### 🏆 Top 5 Categories by Sales Volume")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="order_id", y="product_category_name", data=product_sales.head(5), palette=blue_palette, ax=ax)
        ax.set_xlabel("Number of Sales")
        ax.set_ylabel(None)
        st.pyplot(fig)

    with col2:
        st.write("#### 🔻 Bottom 5 Categories by Sales Volume")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="order_id", y="product_category_name", data=product_sales.tail(5), palette=blue_palette, ax=ax)
        ax.set_xlabel("Number of Sales")
        ax.set_ylabel(None)
        ax.invert_xaxis()
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        st.pyplot(fig)

    st.write("---")
    
    st.write("#### 💰 Top 5 Categories by Total Revenue")
    fig_rev, ax_rev = plt.subplots(figsize=(16, 6))
    sns.barplot(x="payment_value", y="product_category_name", data=product_revenue.head(5), palette=blue_palette, ax=ax_rev)
    ax_rev.set_xlabel("Total Revenue (R$)")
    ax_rev.set_ylabel(None)
    st.pyplot(fig_rev)

with tab_rfm:
    st.subheader("Best Customer Based on RFM Parameters")
    
    ref_date = main_df['order_purchase_timestamp'].max() + pd.DateOffset(days=1)
    rfm = main_df.groupby("customer_unique_id").agg({
        "order_purchase_timestamp": lambda x: (ref_date - x.max()).days,
        "order_id": "nunique",
        "payment_value": "sum"
    }).reset_index()
    rfm.columns = ["cust_id", "Recency", "Frequency", "Monetary"]
    rfm['cust_id_short'] = rfm['cust_id'].str[:5]

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Avg Recency", f"{rfm.Recency.mean():.1f} Days")
    col_b.metric("Avg Frequency", f"{rfm.Frequency.mean():.2f} Orders")
    col_c.metric("Avg Monetary", f"R$ {rfm.Monetary.mean():,.2f}")

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
    colors_rfm = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

    sns.barplot(y="Recency", x="cust_id_short", data=rfm.sort_values(by="Recency", ascending=True).head(5), palette=colors_rfm, ax=ax[0])
    ax[0].set_title("By Recency (days)", fontsize=50)
    ax[0].tick_params(axis='y', labelsize=30)
    ax[0].tick_params(axis='x', labelsize=35)

    sns.barplot(y="Frequency", x="cust_id_short", data=rfm.sort_values(by="Frequency", ascending=False).head(5), palette=colors_rfm, ax=ax[1])
    ax[1].set_title("By Frequency", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=30)
    ax[1].tick_params(axis='x', labelsize=35)

    sns.barplot(y="Monetary", x="cust_id_short", data=rfm.sort_values(by="Monetary", ascending=False).head(5), palette=colors_rfm, ax=ax[2])
    ax[2].set_title("By Monetary", fontsize=50)
    ax[2].tick_params(axis='y', labelsize=30)
    ax[2].tick_params(axis='x', labelsize=35)
    st.pyplot(fig)

    st.write("---")

    st.write("#### Customer Segmentation & Data Details")
    col_table, col_pie = st.columns([1.5, 1])
    
    with col_table:
        st.write("**Top 10 Customers by Revenue**")
        st.dataframe(rfm.sort_values("Monetary", ascending=False).head(10), use_container_width=True, hide_index=True)

    with col_pie:
        st.write("**Customer Value Share**")
        rfm['Segment'] = pd.cut(rfm['Monetary'], 
                                bins=[0, 150, 600, float('inf')], 
                                labels=['Silver', 'Gold', 'Platinum'])
        seg_counts = rfm['Segment'].value_counts().sort_index()
        
        fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
        colors_pie = ['#CD7F32','#FFD700','#E5E4E2'] 
        
        wedges, texts, autotexts = ax_pie.pie(
            seg_counts, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colors_pie,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'width': 0.4},
            textprops={'fontsize': 10, 'fontweight': 'bold'}
        )
        
        ax_pie.legend(wedges, seg_counts.index, title="Segments", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        st.pyplot(fig_pie)

st.markdown("---")
st.caption(f"Copyright © {datetime.now().year} | Data Analysis Project - Chyntia Claudia | Dicoding Student ID: CDCC319D6X2689")