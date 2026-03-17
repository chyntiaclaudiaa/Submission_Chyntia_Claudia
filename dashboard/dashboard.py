import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="E-Commerce Performance Dashboard",
    page_icon="🛍️",
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
    st.markdown("""
        <div style="text-align: center; margin-top: -20px;">
            <h1 style="color: #72BCD4; margin-bottom: 0px;">🛍️ E-Shop</h1>
            <p style="font-size: 0.9em; margin-top: 0px;">Project Analisis Data</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.write("### Filter Analisis")
    min_date = all_df["order_purchase_timestamp"].min()
    max_date = all_df["order_purchase_timestamp"].max()
    
    start_date = st.date_input(
        label='Tanggal Mulai',
        min_value=min_date,
        max_value=max_date,
        value=min_date
    )
    
    end_date = st.date_input(
        label='Tanggal Akhir',
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )
    
    st.markdown("---")
    
    st.caption("Dashboard ini memvisualisasikan insight dari E-Commerce Public Dataset.")

main_df = all_df[(all_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

st.title("E-Commerce Intelligence Dashboard 🚀")
st.info(f"Menampilkan data periode: **{start_date}** hingga **{end_date}**")

tab_growth, tab_product, tab_delivery, tab_customer = st.tabs([
    "📈 Growth & Revenue", "📦 Product & Payments", "🚚 Delivery & Satisfaction", "💎 Customer RFM"
])

color_main = "#72BCD4"
color_sub = "#D3D3D3"
color_alert = "#E38690"

with tab_growth:
    st.subheader("Business Growth Trend")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Unique Orders", f"{main_df.order_id.nunique():,}")
    with m2:
        st.metric("Total Revenue", f"R$ {main_df.payment_value.sum():,.2f}")
    with m3:
        order_count = main_df.order_id.nunique()
        aov = main_df.payment_value.sum() / order_count if order_count > 0 else 0
        st.metric("Avg Order Value", f"R$ {aov:,.2f}")

    monthly_trend = main_df.resample(rule='ME', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    }).reset_index()
    monthly_trend["order_purchase_timestamp"] = monthly_trend["order_purchase_timestamp"].dt.strftime('%b-%Y')

    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(monthly_trend["order_purchase_timestamp"], monthly_trend["payment_value"], marker='o', linewidth=2, color=color_main)
    ax.set_title("Monthly Revenue Trend (BRL)", fontsize=18)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab_product:
    st.subheader("Product & Payment Performance")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### 🏆 Top 5 Categories by Volume")
        top_volume = main_df.groupby("product_category_name_english").order_id.nunique().sort_values(ascending=False).head(5).reset_index()
        fig, ax = plt.subplots()
        sns.barplot(x="order_id", y="product_category_name_english", data=top_volume, 
                    palette=[color_main] + [color_sub]*4, hue="product_category_name_english", legend=False, ax=ax)
        st.pyplot(fig)
        
    with col2:
        st.write("#### 💳 Avg Transaction Value by Payment")
        avg_payment = main_df.groupby("payment_type").payment_value.mean().sort_values(ascending=False).reset_index()
        fig, ax = plt.subplots()
        sns.barplot(x="payment_value", y="payment_type", data=avg_payment, 
                    palette=[color_main] + [color_sub]*4, hue="payment_type", legend=False, ax=ax)
        st.pyplot(fig)

with tab_delivery:
    st.subheader("Delivery Efficiency & Impact on Rating")
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.write("#### 🚚 Delivery Status Distribution")
        delivery_perf = main_df["delivery_performance"].value_counts().reset_index()
        fig, ax = plt.subplots()
        ax.pie(delivery_perf["count"], labels=delivery_perf["delivery_performance"], autopct='%1.1f%%', colors=[color_main, color_alert])
        st.pyplot(fig)
        
    with col_d2:
        st.write("#### ⭐ Avg Rating: On-Time vs Late")
        rating_impact = main_df.groupby("delivery_performance").review_score.mean().sort_values(ascending=False).reset_index()
        fig, ax = plt.subplots()
        sns.barplot(x="review_score", y="delivery_performance", data=rating_impact, palette=[color_main, color_alert], hue="delivery_performance", legend=False, ax=ax)
        ax.set_xlim(0, 5)
        st.pyplot(fig)

with tab_customer:
    st.subheader("Best Customer Based on RFM Parameters")
    
    snapshot_date = main_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    rfm_df = main_df.groupby("customer_unique_id").agg({
        "order_purchase_timestamp": lambda x: (snapshot_date - x.max()).days,
        "order_id": "nunique",
        "payment_value": "sum"
    }).reset_index()
    rfm_df.columns = ["cust_id", "Recency", "Frequency", "Monetary"]
    rfm_df['cust_id_short'] = rfm_df['cust_id'].str[:5]

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 10))
    
    sns.barplot(y="Recency", x="cust_id_short", data=rfm_df.sort_values("Recency").head(5), palette=[color_main] + [color_sub]*4, hue="cust_id_short", legend=False, ax=ax[0])
    ax[0].set_title("By Recency (days)", fontsize=30)
    
    sns.barplot(y="Frequency", x="cust_id_short", data=rfm_df.sort_values("Frequency", ascending=False).head(5), palette=[color_main] + [color_sub]*4, hue="cust_id_short", legend=False, ax=ax[1])
    ax[1].set_title("By Frequency", fontsize=30)

    sns.barplot(y="Monetary", x="cust_id_short", data=rfm_df.sort_values("Monetary", ascending=False).head(5), palette=[color_main] + [color_sub]*4, hue="cust_id_short", legend=False, ax=ax[2])
    ax[2].set_title("By Monetary", fontsize=30)
    
    st.pyplot(fig)

st.markdown("---")
st.caption(f"Copyright © {datetime.now().year} | Chyntia Claudia | Dicoding Student ID: CDCC319D6X2689")