# ✈️ AeroZim Travel Hub

An interactive Zimbabwe travel companion app built with Python and Streamlit. Combines airport information, hotel listings, flight routes, and analytics in a single dashboard with an interactive Folium map.

## 🖥️ Live Demo
> Deploy on [Streamlit Cloud](https://streamlit.io/cloud) — connect your GitHub repo and it's live in minutes.

## 🚀 Features

### 🗺️ Airport Map
- Interactive Folium dark-mode map of all Zimbabwe airports
- Colour-coded markers by airport type (International, Domestic, Regional, Private)
- Hotel markers overlaid on the same map
- Clickable popups with full airport details (IATA/ICAO codes, elevation, runways, status)

### 🏨 Hotels
- 27+ hotels near Zimbabwean airports with full details
- Filter by city, price per night, and star rating
- Visual charts: average hotel rate by city, star distribution
- Amenity badges for quick scanning

### ✈️ Flight Routes
- 18 routes including domestic and international connections
- Filter by airline (Air Zimbabwe, Fastjet, Emirates, etc.)
- Delay risk indicators (Low / Medium / High) per route
- Price, departure/arrival times, frequency, and aircraft type

### 📊 Analytics Dashboard
- Airport type breakdown pie chart
- Hotel stars vs price scatter by city
- Average route price by airline
- Hotels per city horizontal bar chart
- Full destination summary table

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Pandas | Data manipulation |
| NumPy | Numerical computations |
| Matplotlib | Chart rendering |
| Folium | Interactive Leaflet.js map |
| streamlit-folium | Streamlit ↔ Folium bridge |
| Streamlit | Web app framework |

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/aerozim-travel-hub.git
cd aerozim-travel-hub

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`

## 📁 Project Structure

```
aerozim-travel-hub/
│
├── app.py              # Main Streamlit application (4 tabs)
├── airports.csv        # Zimbabwe airports dataset (12 airports)
├── hotels.csv          # Hotels near airports (27 hotels)
├── routes.csv          # Flight routes (18 routes, domestic + international)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 📂 Datasets

**airports.csv** — 12 airports including HRE, BUQ, VFA with coordinates, elevation, IATA/ICAO codes

**hotels.csv** — 27 hotels from budget to luxury (Meikles 5★ to regional guesthouses) with geo-coordinates, pricing, and amenities

**routes.csv** — 18 routes covering Air Zimbabwe, Fastjet Zimbabwe, South African Airways, Kenya Airways, Ethiopian Airlines, and Emirates

## 🌍 Airports Covered

| City | Airport | Type |
|------|---------|------|
| Harare | Robert Gabriel Mugabe International | International |
| Bulawayo | Joshua Mqabuko Nkomo International | International |
| Victoria Falls | Victoria Falls International | International |
| Kariba | Kariba Airport | Domestic |
| Hwange | Hwange National Park Airport | Domestic |
| Masvingo | Masvingo Airport | Domestic |
| Mutare | Mutare Airport | Domestic |
| Gweru | Gweru-Thornhill | Domestic |
| Chiredzi | Buffalo Range | Domestic |

## 👨‍💻 Author

Built as part of a Data Analytics & ML portfolio for an Informatics internship application in Zimbabwe's aviation sector.

---
*Built with ❤️ using Python & Streamlit*
