import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="BusinessBroker • v1",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; color: #1E3A8A; font-weight: bold;}
    .metric-card {background-color: #F8FAFC; padding: 1rem; border-radius: 10px; border: 1px solid #E2E8F0;}
    .business-card {border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'listings' not in st.session_state:
    st.session_state.listings = pd.DataFrame({
        'ID': ['BB001', 'BB002', 'BB003', 'BB004', 'BB005'],
        'Business Name': [
            'Coastal Coffee Roasters',
            'TechSolutions Consulting',
            'GreenLeaf Landscaping',
            'Urban Fitness Studio',
            'Prime Auto Repair'
        ],
        'Industry': ['Food & Beverage', 'Professional Services', 'Home Services', 'Health & Fitness', 'Automotive'],
        'Location': ['San Diego, CA', 'Austin, TX', 'Denver, CO', 'Chicago, IL', 'Phoenix, AZ'],
        'Asking Price': [450000, 1250000, 285000, 675000, 390000],
        'Revenue': [620000, 1850000, 420000, 980000, 680000],
        'EBITDA': [145000, 420000, 95000, 210000, 135000],
        'Cash Flow': [132000, 385000, 88000, 195000, 118000],
        'Year Established': [2018, 2015, 2020, 2019, 2017],
        'Status': ['For Sale', 'For Sale', 'Under Offer', 'For Sale', 'For Sale']
    })

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/fluency/96/handshake.png", width=80)
st.sidebar.title("BusinessBroker")
st.sidebar.markdown("**v1.0** • Marketplace for Serious Buyers & Sellers")

page = st.sidebar.radio("Navigation", [
    "🏠 Home",
    "📋 Browse Listings",
    "🔢 Valuation Tool",
    "📊 Market Insights",
    "💼 Submit Your Business",
    "📞 Contact Us"
])

# HOME PAGE
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">Welcome to BusinessBroker</h1>', unsafe_allow_html=True)
    st.markdown("### The simplest way to buy or sell a profitable business")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Listings", "248", "↑12 this week")
    with col2:
        st.metric("Businesses Sold", "1,847", "YTD")
    with col3:
        st.metric("Avg. Sale Price", "$682k", "↑4.2%")
    with col4:
        st.metric("Avg. Multiple", "3.8x", "SDE")
    
    st.divider()
    
    st.subheader("Featured Businesses")
    featured = st.session_state.listings.head(3)
    
    cols = st.columns(3)
    for i, row in featured.iterrows():
        with cols[i]:
            st.markdown(f"""
            **{row['Business Name']}**  
            {row['Location']} • {row['Industry']}
            """)
            st.metric("Asking", f"${row['Asking Price']:,.0f}", delta=None)
            st.button("View Details", key=f"feat_{i}")

# BROWSE LISTINGS
elif page == "📋 Browse Listings":
    st.title("Browse Businesses For Sale")
    
    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        industry_filter = st.multiselect(
            "Industry", 
            options=st.session_state.listings['Industry'].unique(),
            default=None
        )
    with col2:
        location_filter = st.multiselect(
            "Location", 
            options=st.session_state.listings['Location'].unique(),
            default=None
        )
    with col3:
        price_max = st.slider(
            "Max Asking Price ($)", 
            min_value=100000, 
            max_value=2000000, 
            value=1500000,
            step=50000
        )
    
    # Apply filters
    df = st.session_state.listings.copy()
    if industry_filter:
        df = df[df['Industry'].isin(industry_filter)]
    if location_filter:
        df = df[df['Location'].isin(location_filter)]
    df = df[df['Asking Price'] <= price_max]
    
    # Display listings
    st.markdown(f"**Showing {len(df)} businesses**")
    
    for idx, row in df.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="business-card">
                <h4>{row['Business Name']}</h4>
                <p><b>{row['Industry']}</b> • {row['Location']} • Est. {row['Year Established']}</p>
                <div style="display: flex; gap: 2rem;">
                    <div><b>Asking:</b> ${row['Asking Price']:,.0f}</div>
                    <div><b>Revenue:</b> ${row['Revenue']:,.0f}</div>
                    <div><b>Cash Flow:</b> ${row['Cash Flow']:,.0f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns([1, 1, 3])
            with c1:
                if st.button("💼 View Details", key=f"view_{row['ID']}"):
                    st.success(f"Opening details for {row['Business Name']} (demo)")
            with c2:
                if row['ID'] in st.session_state.favorites:
                    if st.button("❤️", key=f"fav_{row['ID']}"):
                        st.session_state.favorites.remove(row['ID'])
                else:
                    if st.button("♡", key=f"fav_{row['ID']}"):
                        st.session_state.favorites.append(row['ID'])
                        st.toast("Added to favorites ❤️")
            st.divider()

# VALUATION TOOL
elif page == "🔢 Valuation Tool":
    st.title("Business Valuation Estimator")
    st.markdown("Get a quick estimate of what your business could be worth")
    
    st.subheader("Enter Your Business Details")
    
    col1, col2 = st.columns(2)
    with col1:
        revenue = st.number_input("Annual Revenue ($)", min_value=50000, value=500000, step=10000)
        ebitda = st.number_input("EBITDA ($)", min_value=10000, value=120000, step=5000)
        industry = st.selectbox("Industry", [
            "Food & Beverage", "Professional Services", "Retail", 
            "Health & Fitness", "Automotive", "Technology", "Other"
        ])
    
    with col2:
        cash_flow = st.number_input("Seller's Discretionary Earnings (SDE) ($)", min_value=30000, value=150000, step=5000)
        years = st.slider("Years in Operation", 1, 30, 8)
        growth = st.slider("Annual Growth Rate (%)", 0, 50, 12)
    
    if st.button("Calculate Valuation", type="primary"):
        # Simple valuation model
        sde_multiple = 3.2
        if industry in ["Technology", "Professional Services"]:
            sde_multiple = 4.5
        elif industry in ["Food & Beverage", "Retail"]:
            sde_multiple = 2.8
        
        base_value = cash_flow * sde_multiple
        growth_adjust = base_value * (growth / 100) * 0.5
        tenure_bonus = base_value * (min(years, 15) / 20)
        
        estimated_value = base_value + growth_adjust + tenure_bonus
        low = int(estimated_value * 0.85)
        high = int(estimated_value * 1.15)
        
        st.success("### Valuation Range")
        st.metric("Estimated Business Value", f"${estimated_value:,.0f}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Low Estimate", f"${low:,.0f}")
        with col_b:
            st.metric("High Estimate", f"${high:,.0f}")
        
        st.info(f"""
        **Valuation Notes**  
        • Multiple used: **{sde_multiple:.1f}x SDE** (industry adjusted)  
        • Based on {years} years of operation and {growth}% growth  
        • Actual offers will depend on financials, location, and buyer fit
        """)

# MARKET INSIGHTS
elif page == "📊 Market Insights":
    st.title("Market Insights")
    
    st.subheader("Industry Multiples (2026)")
    multiples = pd.DataFrame({
        "Industry": ["Tech & Software", "Healthcare", "Food Service", "Auto Repair", "Fitness", "Landscaping"],
        "Avg Multiple (SDE)": [4.8, 4.2, 2.9, 3.1, 3.4, 2.7],
        "Avg Sale Time (days)": [68, 82, 95, 71, 88, 104]
    })
    st.dataframe(multiples, use_container_width=True, hide_index=True)
    
    st.subheader("Recent Sales Trends")
    chart_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Avg Price": [620000, 645000, 680000, 710000, 695000, 682000],
        "Listings": [42, 51, 48, 55, 63, 58]
    })
    st.line_chart(chart_data.set_index("Month"))

# SUBMIT BUSINESS
elif page == "💼 Submit Your Business":
    st.title("List Your Business For Sale")
    
    with st.form("listing_form"):
        st.text_input("Business Name")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Industry", ["Food & Beverage", "Retail", "Services", "Manufacturing", "Other"])
            st.number_input("Asking Price ($)", min_value=50000)
        with col2:
            st.text_input("City, State")
            st.number_input("Annual Revenue ($)")
        
        st.text_area("Brief Description (max 500 chars)", height=150)
        st.file_uploader("Upload Financial Summary (PDF/Excel)", type=["pdf", "xlsx", "csv"])
        
        submitted = st.form_submit_button("Submit for Review", type="primary")
        if submitted:
            st.success("✅ Thank you! Your listing has been submitted. Our team will review within 48 hours.")

# CONTACT
elif page == "📞 Contact Us":
    st.title("Get In Touch")
    st.markdown("Ready to buy or sell? Let's talk.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input("Your Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        message = st.text_area("How can we help you?", height=200)
        
        if st.button("Send Message", type="primary"):
            st.success("Message sent! We'll get back to you within 24 hours.")
    
    with col2:
        st.markdown("### Broker Team")
        st.markdown("**Michael Torres**  \nSenior Business Broker  \nmichael@businessbroker.com")
        st.markdown("**Sarah Chen**  \nValuations & Listings  \nsarah@businessbroker.com")
        
        st.divider()
        st.info("📍 Serving the United States  \n💼 15+ years helping entrepreneurs")

st.sidebar.markdown("---")
st.sidebar.caption("BusinessBroker v1.0 • Demo App  \nBuilt with Streamlit")
