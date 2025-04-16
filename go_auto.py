import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Vehicle Popularity Finder", layout="wide")

# Load data
@st.cache_data

def load_data():
    used_df = pd.read_csv("vehicle_df_with_originals (1).csv")
    new_df = pd.read_csv("vehicle_new_df_clustered (1).csv")
    brand_used = pd.read_csv("brand_df_with_originals (1).csv")
    brand_new = pd.read_csv("brand_new_df_clustered (1).csv")
    return used_df, new_df, brand_used, brand_new

# Load all
dfs = load_data()
used_df, new_df, brand_used, brand_new = dfs

# Sidebar Nav
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Dashboard", "🚘 Vehicle Search", "📈 Brand Insights", "🎯 Cluster Profiles", "📌 Insights & Recommendations"])

# === PAGE 1: Dashboard ===
if page == "🏠 Dashboard":
    st.title("🚗 Feature-Based Vehicle Popularity Analysis")
    st.markdown("""
    ### 🔍 Problem Statement
    This dashboard addresses **Problem Statement #7**: _Feature-Based Vehicle Popularity Analysis (Clustering)_.

    **Goal:** Apply clustering techniques to group vehicles based on features that impact popularity:
    - 🚗 Exterior Color
    - 📆 Vehicle Year
    - 📉 Days on Market
    - 🔁 Number of Price Changes
    - ✅ Certified Status

    **Benefits:**
    - Understand what makes a car sell faster
    - Help dealerships identify high-demand segments
    - Use clustering to make data-driven stocking and pricing decisions

    **Features Considered:**
    - Vehicle Year
    - Mileage
    - Price
    - Days on Market
    - Certified/Color/Price Change (preprocessed)
    """)

# === PAGE 2: Vehicle Search ===
elif page == "🚘 Vehicle Search":
    st.title("🔍 Explore Popular Vehicles")

    dataset_choice = st.radio("Select Dataset", ("Used Vehicles", "New Vehicles"))
    df = used_df.copy() if dataset_choice == "Used Vehicles" else new_df.copy()

    st.sidebar.header("Filter Criteria")
    if df.model_year.min() == df.model_year.max():
        year = (int(df.model_year.min()), int(df.model_year.max()) + 1)
    else:
        year = st.sidebar.slider("Model Year", min_value=int(df.model_year.min()), max_value=int(df.model_year.max()), value=(int(df.model_year.min()), int(df.model_year.max())))

    mileage = st.sidebar.slider("Mileage", min_value=int(df.mileage.min()), max_value=int(df.mileage.max()), value=(int(df.mileage.min()), int(df.mileage.max())))
    price = st.sidebar.slider("Price", min_value=int(df.price.min()), max_value=int(df.price.max()), value=(int(df.price.min()), int(df.price.max())))
    dom = st.sidebar.slider("Days on Market", min_value=int(df.days_on_market.min()), max_value=int(df.days_on_market.max()), value=(int(df.days_on_market.min()), int(df.days_on_market.max())))

    filtered = df[
        (df['model_year'].between(*year)) &
        (df['mileage'].between(*mileage)) &
        (df['price'].between(*price)) &
        (df['days_on_market'].between(*dom))
    ]

    st.subheader(f"Matching Vehicles: {len(filtered)}")
    st.dataframe(filtered[['original_make', 'original_model', 'model_year', 'mileage', 'price', 'days_on_market']].sort_values(by='days_on_market'))

# === PAGE 3: Brand-Level Cluster Insights ===
elif page == "📈 Brand Insights":
    st.title("📊 Popular Brand Performance")
    brand_set = st.radio("Select Dataset", ("Used Vehicles", "New Vehicles"))
    brand_df = brand_used.copy() if brand_set == "Used Vehicles" else brand_new.copy()

    dom = st.slider("Days on Market", min_value=int(brand_df.days_on_market.min()), max_value=int(brand_df.days_on_market.max()), value=(int(brand_df.days_on_market.min()), int(brand_df.days_on_market.max())))
    if brand_df.model_year.min() == brand_df.model_year.max():
        year = (int(brand_df.model_year.min()), int(brand_df.model_year.max()) + 1)
    else:
        year = st.slider("Model Year", min_value=int(brand_df.model_year.min()), max_value=int(brand_df.model_year.max()), value=(int(brand_df.model_year.min()), int(brand_df.model_year.max())))

    brand_filtered = brand_df[
        (brand_df['days_on_market'].between(*dom)) &
        (brand_df['model_year'].between(*year))
    ]

    st.write("Brands with fast turnover (lower days_on_market = more popular):")
    st.dataframe(brand_filtered[['original_make', 'days_on_market', 'model_year', 'price', 'mileage', 'brand_cluster']].sort_values(by='days_on_market'))

# === PAGE 4: Cluster PCA Visuals ===
elif page == "🎯 Cluster Profiles":
    st.title("🎯 Cluster Visualizations")
    cluster_tab = st.radio("Choose Cluster Type", ("Vehicle-Level", "Brand-Level"))

    if cluster_tab == "Vehicle-Level":
        df = used_df.copy()
        if 'PCA1' in df.columns and 'PCA2' in df.columns:
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='vehicle_cluster', palette='tab10', s=10, ax=ax)
            plt.title("Vehicle-Level Cluster Visualization (PCA)")
            st.pyplot(fig)
        else:
            st.warning("PCA columns not found in dataset. Please ensure PCA1 and PCA2 exist.")

    else:
        df = brand_used.copy()
        if 'PCA1' in df.columns and 'PCA2' in df.columns:
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='brand_cluster', palette='Set2', s=50, ax=ax)
            plt.title("Brand-Level Cluster Visualization (PCA)")
            st.pyplot(fig)
        else:
            st.warning("PCA columns not found in dataset. Please ensure PCA1 and PCA2 exist.")

# === PAGE 5: Insights ===
elif page == "📌 Insights & Recommendations":
    st.title("📌 Final Insights & Strategy")
    st.markdown("""
    ### 🔑 Key Observations
    - Clusters with low days on market = popular vehicles
    - Certified, newer, low-mileage vehicles dominate high-performing clusters
    - Brands like Toyota, Honda, Tesla appear frequently in fast-selling segments

    ### 📌 Recommendations for Dealerships
    - 🎯 Stock more vehicles with high-performing features
    - 📊 Use cluster insights for pricing & listing prioritization
    - 📉 Avoid overstocking slow segments
    - 🧠 Use certified status & price trends to fine-tune strategies

    ✅ Data-driven clustering helps **Go Auto** make intelligent inventory and pricing decisions.
    """)
