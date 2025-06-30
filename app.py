import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="🏠 Real Estate Analytics Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling yang lebih menarik
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e1e5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    .plot-container {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    h1 {
        color: #2e4057;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #667eea;
        margin-bottom: 2rem;
    }
    h2, h3 {
        color: #2e4057;
        margin-top: 2rem;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_clean_data():
    """Load dan bersihkan data dengan error handling"""
    try:
        # Load data
        df = pd.read_csv('us_house_Sales_data.csv')
        
        # Bersihkan kolom Price
        df['Price_Clean'] = df['Price'].str.replace('$', '').str.replace(',', '').astype(float)
        
        # Bersihkan kolom Bedrooms dan Bathrooms
        df['Bedrooms_Clean'] = df['Bedrooms'].str.extract('(\d+)').astype(float)
        df['Bathrooms_Clean'] = df['Bathrooms'].str.extract('(\d+)').astype(float)
        
        # Bersihkan kolom Area
        df['Area_Clean'] = df['Area (Sqft)'].str.replace('sqft', '').str.replace(',', '').astype(float)
        
        # Bersihkan kolom Lot Size
        df['Lot_Size_Clean'] = df['Lot Size'].str.replace('sqft', '').str.replace(',', '').astype(float)
        
        # Tambahkan kolom Price per sqft
        df['Price_per_sqft'] = df['Price_Clean'] / df['Area_Clean']
        
        # Kategorikan usia bangunan
        current_year = datetime.now().year
        df['Building_Age'] = current_year - df['Year Built']
        df['Age_Category'] = pd.cut(df['Building_Age'], 
                                   bins=[0, 10, 20, 30, 50, 100], 
                                   labels=['0-10 years', '11-20 years', '21-30 years', '31-50 years', '50+ years'])
        
        # Kategorikan harga
        df['Price_Category'] = pd.cut(df['Price_Clean'], 
                                     bins=[0, 200000, 400000, 600000, 1000000, float('inf')], 
                                     labels=['<$200K', '$200K-$400K', '$400K-$600K', '$600K-$1M', '>$1M'])
        
        # Extract agent name
        df['Agent_Name'] = df['Listing Agent'].str.split(' - ').str[0]
        df['Agent_Company'] = df['Listing Agent'].str.split(' - ').str[1]
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_metric_cards(df):
    """Buat metric cards untuk KPI utama"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_price = df['Price_Clean'].mean()
        st.metric("Rata-rata Harga", f"${avg_price:,.0f}")
    
    with col2:
        avg_days = df['Days on Market'].mean()
        st.metric("Rata-rata Hari di Pasar", f"{avg_days:.0f} hari")
    
    with col3:
        total_properties = len(df)
        st.metric("Total Properti", f"{total_properties:,}")
    
    with col4:
        sold_rate = (df['Status'] == 'Sold').mean() * 100
        st.metric("Tingkat Terjual", f"{sold_rate:.1f}%")

def plot_price_distribution(df):
    """Plot distribusi harga berdasarkan state dan city"""
    st.subheader("📈 1. Analisis Harga Pasar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Harga rata-rata per state
        state_prices = df.groupby('State')['Price_Clean'].agg(['mean', 'count']).reset_index()
        state_prices = state_prices[state_prices['count'] >= 10]  # Filter states dengan data cukup
        
        fig_state = px.bar(state_prices.sort_values('mean', ascending=False), 
                          x='State', y='mean',
                          title='Rata-rata Harga Properti per Negara Bagian',
                          labels={'mean': 'Rata-rata Harga ($)', 'State': 'Negara Bagian'},
                          color='mean',
                          color_continuous_scale='viridis')
        fig_state.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_state, use_container_width=True)
    
    with col2:
        # Top 10 kota termahal
        city_prices = df.groupby(['City', 'State'])['Price_Clean'].agg(['mean', 'count']).reset_index()
        city_prices = city_prices[city_prices['count'] >= 5]
        top_cities = city_prices.nlargest(10, 'mean')
        top_cities['City_State'] = top_cities['City'] + ', ' + top_cities['State']
        
        fig_city = px.bar(top_cities.sort_values('mean'), 
                         x='mean', y='City_State',
                         title='Top 10 Kota Termahal',
                         labels={'mean': 'Rata-rata Harga ($)', 'City_State': 'Kota'},
                         color='mean',
                         color_continuous_scale='plasma',
                         orientation='h')
        fig_city.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_city, use_container_width=True)

def plot_market_efficiency(df):
    """Plot analisis efisiensi pasar"""
    st.subheader("⏱️ 2. Efisiensi Penjualan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Days on market by property type
        market_days = df.groupby('Property Type')['Days on Market'].agg(['mean', 'median', 'count']).reset_index()
        market_days = market_days[market_days['count'] >= 10]
        
        fig_market = go.Figure()
        fig_market.add_trace(go.Bar(x=market_days['Property Type'], y=market_days['mean'],
                                   name='Rata-rata', marker_color='lightblue'))
        fig_market.add_trace(go.Bar(x=market_days['Property Type'], y=market_days['median'],
                                   name='Median', marker_color='darkblue'))
        
        fig_market.update_layout(
            title='Hari di Pasar berdasarkan Tipe Properti',
            xaxis_title='Tipe Properti',
            yaxis_title='Hari di Pasar',
            barmode='group',
            height=400
        )
        st.plotly_chart(fig_market, use_container_width=True)
    
    with col2:
        # Days on market by price category
        price_market = df.groupby('Price_Category')['Days on Market'].mean().reset_index()
        
        fig_price_market = px.box(df, x='Price_Category', y='Days on Market',
                                 title='Distribusi Hari di Pasar berdasarkan Kategori Harga',
                                 labels={'Price_Category': 'Kategori Harga', 'Days on Market': 'Hari di Pasar'},
                                 color='Price_Category')
        fig_price_market.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_price_market, use_container_width=True)

def plot_property_preferences(df):
    """Plot analisis preferensi properti"""
    st.subheader("🏡 3. Preferensi Pasar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Heatmap korelasi antara bedrooms, bathrooms, area, dan price
        correlation_data = df[['Bedrooms_Clean', 'Bathrooms_Clean', 'Area_Clean', 'Price_Clean']].corr()
        
        fig_corr = px.imshow(correlation_data,
                            text_auto=True,
                            aspect="auto",
                            title='Korelasi: Kamar Tidur, Kamar Mandi, Luas & Harga',
                            color_continuous_scale='RdBu_r')
        fig_corr.update_layout(height=400)
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        # Scatter plot area vs price dengan color berdasarkan bedrooms
        fig_scatter = px.scatter(df.sample(n=min(1000, len(df))), 
                               x='Area_Clean', y='Price_Clean',
                               color='Bedrooms_Clean',
                               size='Bathrooms_Clean',
                               title='Hubungan Luas Bangunan vs Harga',
                               labels={'Area_Clean': 'Luas Bangunan (sqft)', 
                                      'Price_Clean': 'Harga ($)',
                                      'Bedrooms_Clean': 'Kamar Tidur'},
                               hover_data=['City', 'State'])
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

def plot_agent_performance(df):
    """Plot analisis performa agen"""
    st.subheader("👥 4. Analisis Performa Agen")
    
    # Hitung statistik agen
    agent_stats = df.groupby('Agent_Name').agg({
        'Price_Clean': ['count', 'mean'],
        'Days on Market': 'mean',
        'Status': lambda x: (x == 'Sold').sum()
    }).reset_index()
    
    agent_stats.columns = ['Agent_Name', 'Total_Properties', 'Avg_Price', 'Avg_Days_Market', 'Sold_Count']
    agent_stats['Sold_Rate'] = (agent_stats['Sold_Count'] / agent_stats['Total_Properties']) * 100
    
    # Filter agen dengan minimal 5 properti
    agent_stats = agent_stats[agent_stats['Total_Properties'] >= 5]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 agen berdasarkan jumlah properti
        top_agents = agent_stats.nlargest(10, 'Total_Properties')
        
        fig_agents = px.bar(top_agents.sort_values('Total_Properties'), 
                           x='Total_Properties', y='Agent_Name',
                           title='Top 10 Agen Berdasarkan Jumlah Properti',
                           labels={'Total_Properties': 'Jumlah Properti', 'Agent_Name': 'Nama Agen'},
                           color='Total_Properties',
                           color_continuous_scale='blues',
                           orientation='h')
        fig_agents.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_agents, use_container_width=True)
    
    with col2:
        # Scatter plot: sold rate vs avg days on market
        fig_perf = px.scatter(agent_stats, 
                            x='Avg_Days_Market', y='Sold_Rate',
                            size='Total_Properties',
                            title='Performa Agen: Tingkat Penjualan vs Rata-rata Hari di Pasar',
                            labels={'Avg_Days_Market': 'Rata-rata Hari di Pasar', 
                                   'Sold_Rate': 'Tingkat Penjualan (%)',
                                   'Total_Properties': 'Jumlah Properti'},
                            hover_data=['Agent_Name'])
        fig_perf.update_layout(height=400)
        st.plotly_chart(fig_perf, use_container_width=True)

def plot_building_age_analysis(df):
    """Plot analisis usia bangunan"""
    st.subheader("🏗️ 5. Tren Pasar Berdasarkan Usia Bangunan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Harga rata-rata berdasarkan kategori usia
        age_price = df.groupby('Age_Category')['Price_Clean'].agg(['mean', 'count']).reset_index()
        
        fig_age = px.bar(age_price, 
                        x='Age_Category', y='mean',
                        title='Rata-rata Harga berdasarkan Usia Bangunan',
                        labels={'Age_Category': 'Kategori Usia', 'mean': 'Rata-rata Harga ($)'},
                        color='mean',
                        color_continuous_scale='viridis')
        fig_age.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        # Days on market berdasarkan usia bangunan
        fig_age_market = px.box(df, x='Age_Category', y='Days on Market',
                               title='Distribusi Hari di Pasar berdasarkan Usia Bangunan',
                               labels={'Age_Category': 'Kategori Usia', 'Days on Market': 'Hari di Pasar'},
                               color='Age_Category')
        fig_age_market.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_age_market, use_container_width=True)

def create_interactive_filters(df):
    """Buat filter interaktif di sidebar"""
    st.sidebar.header("🎛️ Filter Data")
    
    # Filter berdasarkan state
    states = ['All'] + sorted(df['State'].unique().tolist())
    selected_state = st.sidebar.selectbox("Pilih Negara Bagian:", states)
    
    # Filter berdasarkan property type
    prop_types = ['All'] + sorted(df['Property Type'].unique().tolist())
    selected_prop_type = st.sidebar.selectbox("Pilih Tipe Properti:", prop_types)
    
    # Filter berdasarkan price range
    price_min = int(df['Price_Clean'].min())
    price_max = int(df['Price_Clean'].max())
    price_range = st.sidebar.slider("Rentang Harga ($):", price_min, price_max, (price_min, price_max))
    
    # Filter berdasarkan status
    statuses = ['All'] + sorted(df['Status'].unique().tolist())
    selected_status = st.sidebar.selectbox("Pilih Status:", statuses)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_state != 'All':
        filtered_df = filtered_df[filtered_df['State'] == selected_state]
    
    if selected_prop_type != 'All':
        filtered_df = filtered_df[filtered_df['Property Type'] == selected_prop_type]
    
    filtered_df = filtered_df[
        (filtered_df['Price_Clean'] >= price_range[0]) & 
        (filtered_df['Price_Clean'] <= price_range[1])
    ]
    
    if selected_status != 'All':
        filtered_df = filtered_df[filtered_df['Status'] == selected_status]
    
    return filtered_df

def main():
    """Fungsi utama dashboard"""
    st.title("🏠 Real Estate Analytics Dashboard")
    st.markdown("---")
    
    # Load data
    df = load_and_clean_data()
    if df is None:
        st.error("Gagal memuat data. Pastikan file CSV tersedia.")
        return
    
    # Create interactive filters
    filtered_df = create_interactive_filters(df)
    
    # Tampilkan informasi filter
    st.sidebar.markdown("---")
    st.sidebar.write(f"**Data yang ditampilkan:** {len(filtered_df):,} dari {len(df):,} properti")
    
    # Metric cards
    create_metric_cards(filtered_df)
    
    st.markdown("---")
    
    # Plot analisis
    plot_price_distribution(filtered_df)
    st.markdown("---")
    
    plot_market_efficiency(filtered_df)
    st.markdown("---")
    
    plot_property_preferences(filtered_df)
    st.markdown("---")
    
    plot_agent_performance(filtered_df)
    st.markdown("---")
    
    plot_building_age_analysis(filtered_df)
    
    # Tabel detail (optional)
    if st.checkbox("Tampilkan Tabel Detail"):
        st.subheader("📋 Data Detail")
        display_columns = ['Price', 'Address', 'City', 'State', 'Bedrooms', 'Bathrooms', 
                          'Area (Sqft)', 'Year Built', 'Days on Market', 'Property Type', 
                          'Status', 'Listing Agent']
        st.dataframe(filtered_df[display_columns].head(100), use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("*Dashboard dibuat dengan Streamlit dan Plotly*")

if __name__ == "__main__":
    main()