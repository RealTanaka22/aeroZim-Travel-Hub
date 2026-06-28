import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import os

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AeroZim Travel Hub",
    page_icon="✈️",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0c1a29; color: #dde8f0; }
    [data-testid="stSidebar"] { background-color: #102035; }

    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #0a2235 0%, #102035 100%);
        border: 1px solid #1a4a6e;
        border-radius: 12px;
        padding: 14px;
    }
    [data-testid="metric-container"] label { color: #4da6d9 !important; font-size: 12px !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 24px !important; }

    .section-header {
        background: linear-gradient(90deg, #054d7a 0%, #023552 100%);
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        margin: 20px 0 14px 0;
    }

    .airport-card {
        background: #0a2235;
        border: 1px solid #1a4a6e;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
    }
    .airport-card h4 { color: #4da6d9; margin: 0 0 6px 0; font-size: 15px; }
    .airport-card p  { color: #a0c4d9; margin: 2px 0; font-size: 13px; }

    .hotel-card {
        background: #0a2235;
        border: 1px solid #1a4a6e;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 8px;
    }
    .hotel-card h5 { color: #4da6d9; margin: 0 0 4px 0; font-size: 14px; }
    .hotel-card p  { color: #a0c4d9; margin: 2px 0; font-size: 12px; }

    .risk-low    { color: #22c55e; font-weight: 700; }
    .risk-medium { color: #f59e0b; font-weight: 700; }
    .risk-high   { color: #ef4444; font-weight: 700; }

    .route-row {
        background: #0a2235;
        border: 1px solid #1a4a6e;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 13px;
    }

    h1 { color: #ffffff !important; font-weight: 800 !important; }
    h2, h3 { color: #4da6d9 !important; }
    .stTabs [data-baseweb="tab"] { color: #4da6d9 !important; }
    .stTabs [aria-selected="true"] { border-bottom-color: #4da6d9 !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
def set_plot_style():
    plt.rcParams.update({
        "figure.facecolor": "#0c1a29",
        "axes.facecolor":   "#102035",
        "axes.edgecolor":   "#1a4a6e",
        "axes.labelcolor":  "#4da6d9",
        "xtick.color":      "#4da6d9",
        "ytick.color":      "#4da6d9",
        "text.color":       "#dde8f0",
        "grid.color":       "#1a3a52",
        "grid.linestyle":   "--",
        "grid.alpha":       0.5,
    })


STAR_ICONS = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"}
RISK_COLORS = {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"}
TYPE_COLORS = {"International": "#1e90ff", "Domestic": "#22c55e",
               "Regional": "#f59e0b", "Private/GA": "#a78bfa"}


@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    airports = pd.read_csv(os.path.join(base, "airports.csv"))
    hotels   = pd.read_csv(os.path.join(base, "hotels.csv"))
    routes   = pd.read_csv(os.path.join(base, "routes.csv"))
    return airports, hotels, routes


airports_df, hotels_df, routes_df = load_data()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✈️ Filters")
    st.markdown("---")

    airport_types = st.multiselect(
        "Airport Type",
        options=airports_df["type"].unique().tolist(),
        default=airports_df["type"].unique().tolist()
    )

    max_hotel_price = st.slider("Max Hotel Price ($/night)", 40, 700, 300)

    min_stars = st.slider("Minimum Hotel Stars", 1, 5, 2)

    delay_risks = st.multiselect(
        "Delay Risk Level",
        options=["Low", "Medium", "High"],
        default=["Low", "Medium", "High"]
    )

    st.markdown("---")
    st.markdown("**Data Source:** Zimbabwe Civil Aviation Authority")
    st.markdown("**Last Updated:** 2024")


# ── Apply filters ──────────────────────────────────────────────────────────────
filtered_airports = airports_df[airports_df["type"].isin(airport_types)]
filtered_hotels   = hotels_df[
    (hotels_df["price_per_night_usd"] <= max_hotel_price) &
    (hotels_df["stars"] >= min_stars)
]
filtered_routes = routes_df[routes_df["delay_risk"].isin(delay_risks)]


# ── Title ──────────────────────────────────────────────────────────────────────
st.title("✈️ AeroZim Travel Hub")
st.caption("Your complete guide to Zimbabwe's airports, hotels, and flight routes")
st.markdown("---")

# ── KPIs ───────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🛫 Airports",      len(filtered_airports))
k2.metric("🏨 Hotels",        len(filtered_hotels))
k3.metric("✈️ Routes",        len(filtered_routes))
k4.metric("💰 Avg Hotel Rate", f"${filtered_hotels['price_per_night_usd'].mean():.0f}/night")
k5.metric("🌍 Cities Covered", filtered_airports["city"].nunique())

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Airport Map", "🏨 Hotels", "✈️ Flight Routes", "📊 Analytics"])


# ──────────────────────────────────────────────────────────────────────────────
# TAB 1: AIRPORT MAP
# ──────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">🗺️ Zimbabwe Airport Map</div>', unsafe_allow_html=True)

    col_map, col_info = st.columns([2, 1])

    with col_map:
        m = folium.Map(
            location=[-19.0, 29.5],
            zoom_start=6,
            tiles="CartoDB dark_matter"
        )

        for _, row in filtered_airports.iterrows():
            color = TYPE_COLORS.get(row["type"], "#ffffff")
            popup_html = f"""
            <div style="font-family:Arial;min-width:200px;background:#0c1a29;color:#dde8f0;padding:12px;border-radius:8px">
                <h4 style="color:#4da6d9;margin:0 0 8px 0">{row['name']}</h4>
                <p><b>IATA:</b> {row['iata'] if pd.notna(row['iata']) else 'N/A'} &nbsp;|&nbsp; <b>ICAO:</b> {row['icao']}</p>
                <p><b>City:</b> {row['city']}</p>
                <p><b>Type:</b> {row['type']}</p>
                <p><b>Elevation:</b> {row['elevation_ft']:,} ft</p>
                <p><b>Runways:</b> {row['runways']}</p>
                <p><b>Status:</b> <span style="color:#22c55e">{row['status']}</span></p>
            </div>
            """
            icon = folium.DivIcon(
                html=f"""<div style="
                    background:{color};
                    border-radius:50%;
                    width:14px;height:14px;
                    border:2px solid white;
                    box-shadow:0 0 6px {color}
                "></div>""",
                icon_size=(14, 14),
                icon_anchor=(7, 7)
            )
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=f"✈️ {row['name']} ({row['city']})",
                icon=icon
            ).add_to(m)

        # Hotel markers
        for _, row in filtered_hotels.iterrows():
            airport = airports_df[airports_df["airport_id"] == row["airport_id"]]
            if not airport.empty:
                folium.CircleMarker(
                    location=[row["latitude"], row["longitude"]],
                    radius=5,
                    color="#f59e0b",
                    fill=True,
                    fill_color="#f59e0b",
                    fill_opacity=0.7,
                    tooltip=f"🏨 {row['name']} — ${row['price_per_night_usd']}/night ({row['stars']}★)",
                    popup=folium.Popup(f"""
                    <div style="font-family:Arial;background:#0c1a29;color:#dde8f0;padding:10px;border-radius:8px">
                        <h4 style="color:#f59e0b;margin:0 0 6px 0">{row['name']}</h4>
                        <p><b>City:</b> {row['city']}</p>
                        <p><b>Stars:</b> {'★' * int(row['stars'])}</p>
                        <p><b>Price:</b> ${row['price_per_night_usd']}/night</p>
                        <p><b>Rooms:</b> {row['rooms']}</p>
                        <p><b>Distance to Airport:</b> {row['distance_km']} km</p>
                        <p><b>Amenities:</b> {row['amenities']}</p>
                    </div>
                    """, max_width=260)
                ).add_to(m)

        # Legend
        legend_html = """
        <div style="position:fixed;bottom:30px;left:30px;z-index:1000;background:rgba(12,26,41,0.9);
             padding:12px 16px;border-radius:10px;border:1px solid #1a4a6e;color:#dde8f0;font-family:Arial;font-size:12px">
            <b style="color:#4da6d9">Legend</b><br><br>
            <span style="color:#1e90ff">●</span> International Airport<br>
            <span style="color:#22c55e">●</span> Domestic Airport<br>
            <span style="color:#f59e0b">●</span> Regional / Hotel<br>
            <span style="color:#a78bfa">●</span> Private / GA<br>
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))

        st_folium(m, width=None, height=520, returned_objects=[])

    with col_info:
        st.markdown("### 🛫 Airports")
        for _, row in filtered_airports.iterrows():
            iata = row["iata"] if pd.notna(row["iata"]) and row["iata"] != "" else "—"
            color = TYPE_COLORS.get(row["type"], "#fff")
            st.markdown(f"""
            <div class="airport-card">
                <h4>{row['name']}</h4>
                <p>📍 {row['city']} &nbsp;|&nbsp; IATA: <b>{iata}</b></p>
                <p>🏷️ <span style="color:{color}">{row['type']}</span> &nbsp;|&nbsp; ✅ {row['status']}</p>
                <p>📏 Elevation: {row['elevation_ft']:,} ft &nbsp;|&nbsp; 🛤️ {row['runways']} runway(s)</p>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 2: HOTELS
# ──────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">🏨 Hotels Near Zimbabwe Airports</div>', unsafe_allow_html=True)

    selected_city = st.selectbox(
        "Filter by City",
        options=["All Cities"] + sorted(filtered_hotels["city"].unique().tolist())
    )

    if selected_city != "All Cities":
        display_hotels = filtered_hotels[filtered_hotels["city"] == selected_city]
    else:
        display_hotels = filtered_hotels

    display_hotels = display_hotels.sort_values("stars", ascending=False)

    col_h1, col_h2 = st.columns([2, 1])

    with col_h1:
        for _, row in display_hotels.iterrows():
            stars_display = STAR_ICONS.get(int(row["stars"]), "")
            amenity_list = row["amenities"].split(",")[:5]
            amenity_badges = " ".join([f'<span style="background:#1a4a6e;padding:2px 7px;border-radius:10px;font-size:11px;margin:2px">{a.strip()}</span>' for a in amenity_list])
            st.markdown(f"""
            <div class="hotel-card">
                <h5>{row['name']} &nbsp; {stars_display}</h5>
                <p>📍 {row['city']} &nbsp;|&nbsp; 🏨 {row['rooms']} rooms</p>
                <p>💰 <b style="color:#22c55e">${row['price_per_night_usd']}/night</b> &nbsp;|&nbsp; ✈️ {row['distance_km']} km to airport</p>
                <p style="margin-top:6px">{amenity_badges}</p>
            </div>
            """, unsafe_allow_html=True)

    with col_h2:
        set_plot_style()
        st.markdown("### 💰 Price by City")
        city_prices = display_hotels.groupby("city")["price_per_night_usd"].mean().sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(5, max(3, len(city_prices) * 0.6)))
        colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(city_prices)))
        ax.barh(city_prices.index, city_prices.values, color=colors, edgecolor="#0c1a29", linewidth=0.8)
        for i, v in enumerate(city_prices.values):
            ax.text(v + 1, i, f"${v:.0f}", va="center", color="#dde8f0", fontsize=9)
        ax.set_xlabel("Avg Price ($/night)")
        ax.set_title("Avg Hotel Rate by City", color="#dde8f0", fontsize=12)
        ax.grid(axis="x")
        st.pyplot(fig)
        plt.close()

        st.markdown("### ⭐ Star Distribution")
        star_dist = filtered_hotels["stars"].value_counts().sort_index()
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        ax2.bar([f"{s}★" for s in star_dist.index], star_dist.values,
                color=["#4da6d9","#22c55e","#f59e0b","#f97316","#ef4444"][:len(star_dist)],
                edgecolor="#0c1a29", linewidth=0.8)
        ax2.set_title("Hotels by Star Rating", color="#dde8f0", fontsize=12)
        ax2.set_ylabel("Count")
        ax2.grid(axis="y")
        st.pyplot(fig2)
        plt.close()


# ──────────────────────────────────────────────────────────────────────────────
# TAB 3: FLIGHT ROUTES
# ──────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">✈️ Zimbabwe Flight Routes</div>', unsafe_allow_html=True)

    airlines = ["All Airlines"] + sorted(filtered_routes["airline"].unique().tolist())
    selected_airline = st.selectbox("Filter by Airline", airlines)

    if selected_airline != "All Airlines":
        display_routes = filtered_routes[filtered_routes["airline"] == selected_airline]
    else:
        display_routes = filtered_routes

    col_r1, col_r2 = st.columns([3, 1])

    with col_r1:
        st.markdown(f"**{len(display_routes)} routes found**")
        for _, row in display_routes.iterrows():
            risk_class = f"risk-{row['delay_risk'].lower()}"
            risk_icon  = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(row["delay_risk"], "⚪")
            st.markdown(f"""
            <div class="route-row">
                <b style="color:#4da6d9">{row['airline']}</b> &nbsp;|&nbsp;
                🛫 <b>{row['from_city']}</b> → <b>{row['to_city']}</b>
                &nbsp;&nbsp;
                🕐 {row['departure']} → {row['arrival']}
                &nbsp;&nbsp;
                📅 {row['frequency']}
                &nbsp;&nbsp;
                💰 <b style="color:#22c55e">${row['price_usd']}</b>
                &nbsp;&nbsp;
                {risk_icon} Delay Risk: <span class="{risk_class}">{row['delay_risk']}</span>
                &nbsp;&nbsp;
                ✈️ {row['aircraft']}
            </div>
            """, unsafe_allow_html=True)

    with col_r2:
        set_plot_style()
        st.markdown("### 📊 Routes by Airline")
        airline_counts = routes_df["airline"].value_counts()
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.barh(airline_counts.index, airline_counts.values,
                color="#4da6d9", edgecolor="#0c1a29", linewidth=0.8)
        ax.set_xlabel("Routes")
        ax.set_title("Routes per Airline", color="#dde8f0", fontsize=11)
        ax.grid(axis="x")
        st.pyplot(fig)
        plt.close()

        st.markdown("### ⚠️ Delay Risk")
        risk_counts = routes_df["delay_risk"].value_counts()
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        risk_c = [RISK_COLORS.get(r, "#fff") for r in risk_counts.index]
        ax2.pie(risk_counts.values, labels=risk_counts.index, autopct="%1.0f%%",
                colors=risk_c, startangle=90,
                wedgeprops={"edgecolor": "#0c1a29", "linewidth": 1.5})
        ax2.set_title("Delay Risk Distribution", color="#dde8f0", fontsize=11)
        st.pyplot(fig2)
        plt.close()


# ──────────────────────────────────────────────────────────────────────────────
# TAB 4: ANALYTICS
# ──────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">📊 Travel Analytics Dashboard</div>', unsafe_allow_html=True)

    set_plot_style()
    col_a1, col_a2 = st.columns(2)

    with col_a1:
        # Airport type breakdown
        type_counts = airports_df["type"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        colors_t = [TYPE_COLORS.get(t, "#fff") for t in type_counts.index]
        wedges, texts, autotexts = ax.pie(
            type_counts.values, labels=type_counts.index,
            autopct="%1.0f%%", colors=colors_t, startangle=90,
            wedgeprops={"edgecolor": "#0c1a29", "linewidth": 2}
        )
        for t in texts:     t.set_color("#dde8f0"); t.set_fontsize(10)
        for t in autotexts: t.set_color("#0c1a29"); t.set_fontweight("bold")
        ax.set_title("Airport Types", color="#dde8f0", fontsize=13, pad=10)
        st.pyplot(fig)
        plt.close()

    with col_a2:
        # Hotel prices by city scatter
        fig, ax = plt.subplots(figsize=(6, 4))
        cities = hotels_df["city"].unique()
        c_colors = plt.cm.tab10(np.linspace(0, 1, len(cities)))
        for city, color in zip(cities, c_colors):
            subset = hotels_df[hotels_df["city"] == city]
            ax.scatter(subset["stars"], subset["price_per_night_usd"],
                       label=city, color=color, s=80, alpha=0.8,
                       edgecolors="#0c1a29", linewidth=0.5)
        ax.set_xlabel("Stars")
        ax.set_ylabel("Price ($/night)")
        ax.set_title("Hotel Stars vs Price by City", color="#dde8f0", fontsize=13, pad=10)
        ax.legend(fontsize=8, loc="upper left")
        ax.grid()
        st.pyplot(fig)
        plt.close()

    col_a3, col_a4 = st.columns(2)

    with col_a3:
        # Route prices by airline
        route_prices = routes_df.groupby("airline")["price_usd"].mean().sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.barh(route_prices.index, route_prices.values,
                       color="#4da6d9", edgecolor="#0c1a29", linewidth=0.8)
        for bar, val in zip(bars, route_prices.values):
            ax.text(val + 2, bar.get_y() + bar.get_height()/2,
                    f"${val:.0f}", va="center", color="#dde8f0", fontsize=10)
        ax.set_xlabel("Avg Ticket Price ($)")
        ax.set_title("Avg Route Price by Airline", color="#dde8f0", fontsize=13, pad=10)
        ax.grid(axis="x")
        st.pyplot(fig)
        plt.close()

    with col_a4:
        # Hotels per city bar chart
        hotels_per_city = hotels_df.groupby("city").size().sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(6, 4))
        colors_h = plt.cm.Greens(np.linspace(0.4, 0.9, len(hotels_per_city)))
        ax.barh(hotels_per_city.index, hotels_per_city.values,
                color=colors_h, edgecolor="#0c1a29", linewidth=0.8)
        for i, v in enumerate(hotels_per_city.values):
            ax.text(v + 0.05, i, str(v), va="center", color="#dde8f0", fontsize=10)
        ax.set_xlabel("Number of Hotels")
        ax.set_title("Hotels per City", color="#dde8f0", fontsize=13, pad=10)
        ax.grid(axis="x")
        st.pyplot(fig)
        plt.close()

    # Summary table
    st.markdown('<div class="section-header">📋 Destination Summary</div>', unsafe_allow_html=True)
    summary = airports_df.merge(
        hotels_df.groupby("city").agg(
            hotels=("hotel_id", "count"),
            avg_price=("price_per_night_usd", "mean"),
            min_price=("price_per_night_usd", "min"),
        ).reset_index(),
        on="city", how="left"
    )[["city", "name", "type", "iata", "hotels", "avg_price", "min_price"]]
    summary.columns = ["City", "Airport", "Type", "IATA", "Hotels", "Avg Rate ($/night)", "From ($/night)"]
    summary["Avg Rate ($/night)"] = summary["Avg Rate ($/night)"].apply(lambda x: f"${x:.0f}" if pd.notna(x) else "N/A")
    summary["From ($/night)"]     = summary["From ($/night)"].apply(lambda x: f"${x:.0f}" if pd.notna(x) else "N/A")
    summary["Hotels"]             = summary["Hotels"].fillna(0).astype(int)
    st.dataframe(summary, use_container_width=True, hide_index=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("✈️ AeroZim Travel Hub | Built with Python, Folium, Pandas, Matplotlib & Streamlit | Data: Zimbabwe Civil Aviation Authority")
