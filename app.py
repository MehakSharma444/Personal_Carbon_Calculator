from db_handler import create_database, save_user_data, get_recent_data
create_database()  # Ensures DB/table exists


import streamlit as st
import matplotlib.pyplot as plt

# Set wide layout and page name
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

# Define emission factors
# transportation in kgCO2/km
# electricity in kgCO2/KwH
# diet in kgCO2/meal or 2.5 KgCO2/kg
# waste in kgCO2/kg
EMISSION_FACTORS = {
    "India": {"Transportation": 0.14, "Electricity": 0.82, "Diet": 1.25, "Waste": 0.10},
    "United States": {"Transportation": 0.25, "Electricity": 0.45, "Diet": 2.50, "Waste": 0.18},
    "United Kingdom": {"Transportation": 0.19, "Electricity": 0.23, "Diet": 1.90, "Waste": 0.15},
    "Germany": {"Transportation": 0.21, "Electricity": 0.38, "Diet": 2.20, "Waste": 0.16},
    "China": {"Transportation": 0.17, "Electricity": 0.65, "Diet": 2.00, "Waste": 0.12},
    "Canada": {"Transportation": 0.23, "Electricity": 0.12, "Diet": 2.30, "Waste": 0.20},
    "Australia": {"Transportation": 0.22, "Electricity": 0.70, "Diet": 2.40, "Waste": 0.18},
    "France": {"Transportation": 0.18, "Electricity": 0.10, "Diet": 2.00, "Waste": 0.14},
    "Brazil": {"Transportation": 0.20, "Electricity": 0.15, "Diet": 2.10, "Waste": 0.13},
    "Japan": {"Transportation": 0.16, "Electricity": 0.47, "Diet": 2.10, "Waste": 0.17},
    "South Korea": {"Transportation": 0.17, "Electricity": 0.58, "Diet": 2.00, "Waste": 0.15},
    "Russia": {"Transportation": 0.20, "Electricity": 0.50, "Diet": 2.30, "Waste": 0.16},
    "Italy": {"Transportation": 0.18, "Electricity": 0.30, "Diet": 2.00, "Waste": 0.14},
    "Mexico": {"Transportation": 0.19, "Electricity": 0.42, "Diet": 2.10, "Waste": 0.13},
    "South Africa": {"Transportation": 0.22, "Electricity": 0.93, "Diet": 2.20, "Waste": 0.18},
    "Indonesia": {"Transportation": 0.15, "Electricity": 0.75, "Diet": 1.90, "Waste": 0.11},
    "Saudi Arabia": {"Transportation": 0.23, "Electricity": 0.70, "Diet": 2.50, "Waste": 0.19},
    "Argentina": {"Transportation": 0.18, "Electricity": 0.40, "Diet": 2.20, "Waste": 0.15},
    "Spain": {"Transportation": 0.17, "Electricity": 0.27, "Diet": 2.00, "Waste": 0.14},
    "Turkey": {"Transportation": 0.20, "Electricity": 0.50, "Diet": 2.10, "Waste": 0.16},

    # Additional 30 countries:
    "Sweden": {"Transportation": 0.16, "Electricity": 0.04, "Diet": 1.80, "Waste": 0.12},
    "Norway": {"Transportation": 0.15, "Electricity": 0.02, "Diet": 1.70, "Waste": 0.11},
    "Finland": {"Transportation": 0.17, "Electricity": 0.05, "Diet": 1.85, "Waste": 0.12},
    "Denmark": {"Transportation": 0.17, "Electricity": 0.15, "Diet": 1.90, "Waste": 0.13},
    "Switzerland": {"Transportation": 0.16, "Electricity": 0.02, "Diet": 1.80, "Waste": 0.12},
    "Netherlands": {"Transportation": 0.19, "Electricity": 0.38, "Diet": 2.00, "Waste": 0.14},
    "Belgium": {"Transportation": 0.20, "Electricity": 0.23, "Diet": 2.10, "Waste": 0.14},
    "Austria": {"Transportation": 0.18, "Electricity": 0.15, "Diet": 1.95, "Waste": 0.13},
    "Poland": {"Transportation": 0.20, "Electricity": 0.73, "Diet": 2.10, "Waste": 0.15},
    "Ukraine": {"Transportation": 0.19, "Electricity": 0.60, "Diet": 2.00, "Waste": 0.14},
    "Nigeria": {"Transportation": 0.12, "Electricity": 0.55, "Diet": 1.80, "Waste": 0.10},
    "Kenya": {"Transportation": 0.11, "Electricity": 0.30, "Diet": 1.70, "Waste": 0.09},
    "Egypt": {"Transportation": 0.15, "Electricity": 0.60, "Diet": 1.90, "Waste": 0.11},
    "Morocco": {"Transportation": 0.14, "Electricity": 0.60, "Diet": 1.85, "Waste": 0.10},
    "Pakistan": {"Transportation": 0.13, "Electricity": 0.56, "Diet": 1.80, "Waste": 0.10},
    "Bangladesh": {"Transportation": 0.12, "Electricity": 0.51, "Diet": 1.75, "Waste": 0.10},
    "Vietnam": {"Transportation": 0.14, "Electricity": 0.70, "Diet": 1.90, "Waste": 0.11},
    "Philippines": {"Transportation": 0.15, "Electricity": 0.60, "Diet": 1.85, "Waste": 0.12},
    "Thailand": {"Transportation": 0.16, "Electricity": 0.65, "Diet": 2.00, "Waste": 0.13},
    "Malaysia": {"Transportation": 0.17, "Electricity": 0.68, "Diet": 2.10, "Waste": 0.13},
    "Singapore": {"Transportation": 0.18, "Electricity": 0.42, "Diet": 2.20, "Waste": 0.14},
    "UAE": {"Transportation": 0.22, "Electricity": 0.75, "Diet": 2.40, "Waste": 0.18},
    "Qatar": {"Transportation": 0.24, "Electricity": 0.90, "Diet": 2.60, "Waste": 0.20},
    "Israel": {"Transportation": 0.20, "Electricity": 0.60, "Diet": 2.10, "Waste": 0.15},
    "Iran": {"Transportation": 0.19, "Electricity": 0.70, "Diet": 2.00, "Waste": 0.15},
    "Iraq": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.95, "Waste": 0.14},
    "Kazakhstan": {"Transportation": 0.20, "Electricity": 0.80, "Diet": 2.10, "Waste": 0.16},
    "Greece": {"Transportation": 0.18, "Electricity": 0.40, "Diet": 2.00, "Waste": 0.14},
    "Portugal": {"Transportation": 0.17, "Electricity": 0.35, "Diet": 1.95, "Waste": 0.13},
    "New Zealand": {"Transportation": 0.21, "Electricity": 0.10, "Diet": 2.30, "Waste": 0.15},
    "Chile": {"Transportation": 0.18, "Electricity": 0.40, "Diet": 2.10, "Waste": 0.13}
}

# Page management
if "page" not in st.session_state:
    st.session_state.page = 1

# Page navigation buttons
col_nav1, col_nav2, col_nav3 = st.columns(3)
with col_nav1:
    if st.button("1️⃣ Personal Info"):
        st.session_state.page = 1
with col_nav2:
    if st.session_state.get("personal_complete", False):
        if st.button("2️⃣ Input Data"):
            st.session_state.page = 2
with col_nav3:
    if st.session_state.get("input_complete", False):
        if st.button("3️⃣ Results"):
            st.session_state.page = 3

# Page 1: Personal Info
# Page 1: Personal Info
if st.session_state.page == 1:
    st.title("👤 Personal Information")

    with st.form("personal_form"):
        name = st.text_input("Your Name")
        country = st.selectbox("🌐 Select your country", sorted(EMISSION_FACTORS.keys()))
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        gender = st.radio("Gender", ["Male", "Female", "Other"])

        cols = st.columns([5, 1])
        with cols[1]:
            submit1 = st.form_submit_button("Next ➡️")

        if submit1:
            if name.strip() == "":
                st.error("Please enter your name.")
            else:
                # Store all values into session state
                st.session_state.name = name
                st.session_state.country = country
                st.session_state.age = age
                st.session_state.gender = gender
                st.session_state.personal_complete = True
                st.session_state.page = 2


# Page 2: Input Data
elif st.session_state.page == 2:
    st.title("🌱 Your Carbon Activity Data")
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            distance = st.slider("🚗 Daily commute (km)", 0.0, 100.0, key="distance")
            electricity = st.slider("💡 Monthly electricity use (kWh)", 0.0, 1000.0, key="electricity")
        with col2:
            meals = st.number_input("🍽️ Meals per day", 0, 10, key="meals")
            waste = st.slider("🗑️ Weekly waste (kg)", 0.0, 100.0, key="waste")

        col = st.columns([5,1])
        with col[1]:
            submit2 = st.form_submit_button("Next ➡️")
        if submit2:
            if meals == 0:
                st.error("Meals per day must be greater than 0.")
            if distance == 0:
                st.error("Distance should be greater than 0.")
            if electricity == 0:
                st.error("Electricity should be greater than 0.")
            if waste ==0:
                st.error("Waste should be greater than 0.")
            else:
                st.session_state.input_complete = True
                st.session_state.page = 3

# Page 3: Results
# Page 3: Results
elif st.session_state.page == 3:
    st.title("📊 Carbon Emission Results Dashboard")

    # Validate required session state variables
    required_keys = ["name", "country", "age", "gender", "distance", "electricity", "meals", "waste"]
    missing_keys = [key for key in required_keys if key not in st.session_state]

    if missing_keys:
        st.error(f"🚨 Missing input(s): {', '.join(missing_keys)}. Please return to previous steps and complete the form.")
        st.stop()

    # Fetch user inputs
    name = st.session_state["name"]
    country = st.session_state["country"]
    age = st.session_state["age"]
    gender = st.session_state["gender"]
    distance = st.session_state["distance"]      # km/day
    electricity = st.session_state["electricity"]  # kWh/month
    meals = st.session_state["meals"]            # meals/day
    waste = st.session_state["waste"]            # kg/week

    if country not in EMISSION_FACTORS:
        st.error(f"🌍 Emission data for **{country}** is not available.")
        st.stop()

    factors = EMISSION_FACTORS[country]

    # Estimate diet type from meals per day
    if meals <= 2:
        diet_type = "Low-impact"
    elif meals <= 4:
        diet_type = "Average"
    else:
        diet_type = "High-impact"

    DIET_MULTIPLIERS = {
        "Low-impact": 0.8,
        "Average": 1.0,
        "High-impact": 1.2
    }

    # Monthly calculations
    km_per_month = distance * 30
    kg_waste_per_month = waste * 4.3  # avg weeks/month

    transport_emission = km_per_month * factors["Transportation"]
    electricity_emission = electricity * factors["Electricity"]
    diet_emission = factors["Diet"] * DIET_MULTIPLIERS[diet_type]
    waste_emission = kg_waste_per_month * factors["Waste"]
    total_monthly_emission = transport_emission + electricity_emission + diet_emission + waste_emission

    # Show results
    st.subheader("📉 Monthly Emission Breakdown (kg CO₂e)")
    st.markdown(f"""
    - 🚗 **Transportation**: `{transport_emission:.2f}`
    - 💡 **Electricity**: `{electricity_emission:.2f}`
    - 🍽️ **Diet** ({diet_type}): `{diet_emission:.2f}`
    - 🗑️ **Waste**: `{waste_emission:.2f}`
    """)
    st.success(f"🌍 **Total Monthly Emissions**: `{total_monthly_emission:.2f}` kg CO₂e")

    # Annual breakdown
    transport_annual = transport_emission * 12 / 1000
    electricity_annual = electricity_emission * 12 / 1000
    diet_annual = diet_emission * 12 / 1000
    waste_annual = waste_emission * 12 / 1000
    total_annual = total_monthly_emission * 12 / 1000

    st.subheader("📆 Annual Carbon Footprint (tons of CO₂)")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"🚗 **Transport**: {transport_annual:.2f} tCO₂/year")
        st.info(f"💡 **Electricity**: {electricity_annual:.2f} tCO₂/year")
    with col2:
        st.info(f"🍽️ **Diet**: {diet_annual:.2f} tCO₂/year")
        st.info(f"🗑️ **Waste**: {waste_annual:.2f} tCO₂/year")
    st.success(f"🌎 **Total Annual Carbon Footprint**: `{total_annual:.2f}` tCO₂/year")

    # Comparison to country average
    country_averages = {
        "India": 1.9, "United States": 15.2, "United Kingdom": 5.2, "Germany": 8.0,
        "China": 7.6, "Canada": 14.2, "Australia": 17.1, "France": 4.7, "Brazil": 2.2,
        "Japan": 8.7, "South Korea": 11.5, "Russia": 11.4, "Italy": 5.7, "Mexico": 3.7,
        "South Africa": 7.5, "Indonesia": 2.3, "Saudi Arabia": 18.0, "Argentina": 4.6,
        "Spain": 5.2, "Turkey": 5.4, "Sweden": 3.7, "Norway": 6.8, "Finland": 7.5,
        "Denmark": 5.6, "Switzerland": 4.1, "Netherlands": 8.5, "Belgium": 7.6,
        "Austria": 6.8, "Poland": 7.9, "Ukraine": 4.0, "Nigeria": 0.6, "Kenya": 0.3,
        "Egypt": 2.5, "Morocco": 1.9, "Pakistan": 1.1, "Bangladesh": 0.5, "Vietnam": 2.9,
        "Philippines": 1.2, "Thailand": 4.3, "Malaysia": 7.7, "Singapore": 9.6,
        "UAE": 22.2, "Qatar": 32.7, "Israel": 8.1, "Iran": 8.5, "Iraq": 4.4,
        "Kazakhstan": 13.7, "Greece": 6.1, "Portugal": 4.7, "New Zealand": 6.7,
        "Chile": 4.6
    }

    if country in country_averages:
        avg = country_averages[country]
        if total_annual > avg:
            st.warning(f"⚠️ Your footprint is above the **{country}** average of `{avg} tCO₂/year`.")
        else:
            st.success(f"✅ Your footprint is below the **{country}** average of `{avg} tCO₂/year`.")

    # Pie chart
    st.subheader("📊 Emission Source Distribution")
    import matplotlib.pyplot as plt
    labels = ["Transport", "Electricity", "Diet", "Waste"]
    values = [transport_emission, electricity_emission, diet_emission, waste_emission]
    if sum(values) > 0:
        fig, ax = plt.subplots(figsize=(3,3))
        ax.pie(values, labels=labels, autopct='%0.1f%%', startangle=30)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.warning("⚠️ Not enough data to show pie chart.")

    # Recommendations
    st.subheader("💡 Recommendations to Reduce Emissions")
    highest_source = max(zip(labels, values), key=lambda x: x[1])[0]
    reduction_tips = {
        "Transport": "🚴 Use public transport, cycle, or carpool more often.",
        "Electricity": "💡 Switch to energy-efficient appliances and renewable energy sources.",
        "Diet": "🌱 Reduce red meat and dairy consumption, prefer plant-based options.",
        "Waste": "♻️ Reduce, reuse, recycle. Start composting biodegradable waste."
    }
    st.markdown(f"🔍 **Major Contributor**: `{highest_source}`")
    st.info(f"📌 Tip: {reduction_tips[highest_source]}")

    # Compare to national average assumptions
    country_baselines = EMISSION_FACTORS[country]
    above_avg_sources = []
    if transport_emission > country_baselines["Transportation"] * 1000:
        above_avg_sources.append("Transport")
    if electricity_emission > country_baselines["Electricity"] * 200:
        above_avg_sources.append("Electricity")
    if diet_emission > country_baselines["Diet"]:
        above_avg_sources.append("Diet")
    if waste_emission > country_baselines["Waste"] * 20:
        above_avg_sources.append("Waste")

    if above_avg_sources:
        st.subheader("📌 Other Areas Exceeding National Average:")
        for src in above_avg_sources:
            st.warning(f"⚠️ **{src}** is above average. Tip: {reduction_tips[src]}")

    # Save to DB
    from db_handler import save_user_data
    save_user_data(
        name=name,
        country=country,
        age=age,
        gender=gender,
        transport=transport_emission,
        electricity=electricity_emission,
        diet=diet_emission,
        waste=waste_emission,
        total=total_monthly_emission
    )

