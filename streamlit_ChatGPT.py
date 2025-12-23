import streamlit as st
import pandas as pd
import sqlite3
import requests
import plotly.express as px
import pickle
import numpy as np 
with open("sarima_model.pkl", "rb") as f:
    sarima = pickle.load(f)
# Page config MUST come first
st.set_page_config(
    page_title="Paris Cyclists",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CSS ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #1a1a1a;
}

.main .block-container {
    padding-top: 2rem;
    background-color: #1a1a1a;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: #f4d03f !important;
}

/* Text */
.stMarkdown p, label {
    color: #e0e0e0 !important;
}

/* === FORCE GOLD METRICS (Streamlit-proof) === */
div[data-testid="metric-container"] * {
    color: #f4d03f !important;
}

div[data-testid="metric-container"] label {
    color: #f4d03f !important;
    font-weight: 700 !important;
}

div[data-testid="metric-container"] div {
    color: #f4d03f !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
}

/* Optional: subtle glow */
div[data-testid="metric-container"] div {
    text-shadow: 0 0 8px rgba(244, 208, 63, 0.35);
}


/* Date input */
[data-testid="stDateInput"] input {
    background-color: #2d2d2d !important;
    color: #f4d03f !important;
    border: 1px solid #f4d03f !important;
}

/* Plotly */
[data-testid="stPlotlyChart"] {
    background-color: #1a1a1a !important;
}
/* Only the specific number_input we wrapped in #n-pred-container */
#n-pred-container [data-testid="stNumberInput"] > div {
    max-width: 6rem;              /* total widget width (label area) */
}

/* Actual input field */
#n-pred-container [data-testid="stNumberInput"] input {
    max-width: 4rem;              /* just enough for 3 digits */
    background-color: #2d2d2d;    /* dark grey */
    color: #f4d03f;               /* gold numbers */
    border: 1px solid #f4d03f;    /* gold border */
    text-align: center;
    font-weight: 600;
}

/* +/- buttons area */
#n-pred-container [data-testid="stNumberInput"] button {
    background-color: #2d2d2d;
    color: #f4d03f;
    border: 1px solid #f4d03f;
}

/* Remove white default background around control */
#n-pred-container [data-testid="stNumberInput"] > div > div {
    background-color: #2d2d2d;
}

/* Label above control */
#n-pred-container label {
    color: #e0e0e0 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.title("🚲 Cyclists in Paris 🗼🥐")

# ---------- Data ----------
@st.cache_data
def load_bike_data():
    conn = sqlite3.connect("bike_data.db")
    df = pd.read_sql("SELECT date, count FROM counters ORDER BY date", conn)
    conn.close()
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")

df = load_bike_data()

# ---------- GIFs ----------
col1, col2 = st.columns(2)

with col1:
    r = requests.get("https://api.thecatapi.com/v1/images/search?mime_types=gif")
    if r.status_code == 200:
        st.image(r.json()[0]["url"], width=300)
    st.caption("Random Cat GIF")

with col2:
    r = requests.get("https://api.thedogapi.com/v1/images/search?mime_types=gif")
    if r.status_code == 200:
        st.image(r.json()[0]["url"], width=300)
    st.caption("Random Dog GIF")

# ---------- Date Filter ----------
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", df.index.min())
with col2:
    end_date = st.date_input("End Date", df.index.max())

filtered_df = df.loc[start_date:end_date]

# ---------- Plot ----------
fig = px.line(
    filtered_df.reset_index(),
    x="date",
    y="count",
    title="Cyclist Count Over Time"
)

fig.update_layout(
    plot_bgcolor="#1a1a1a",
    paper_bgcolor="#1a1a1a",
    font=dict(color="#f4d03f"),
    title_font_color="#f4d03f",
    xaxis=dict(
        title=dict(
            text="Date",
            font=dict(color="#f4d03f", size=16)
        ),
        tickfont=dict(color="#f4d03f", size=12),
        gridcolor="#2d2d2d",
        zerolinecolor="#2d2d2d",
        linecolor="#f4d03f"
    ),

    yaxis=dict(
        title=dict(
            text="Cyclist Count",
            font=dict(color="#f4d03f", size=16)
        ),
        tickfont=dict(color="#f4d03f", size=12),
        gridcolor="#2d2d2d",
        zerolinecolor="#2d2d2d",
        linecolor="#f4d03f"
    )
)



fig.update_traces(line=dict(color="#f4d03f", width=4))

st.plotly_chart(fig, use_container_width=True)

# ---------- Metrics ----------
# col1, col2, col3 = st.columns(3)
# col1.metric("Total Days", f"{len(df):,}")
# col2.metric("Max Daily Count", f"{df['count'].max():,.0f}")
# col3.metric("Avg Daily Count", f"{df['count'].mean():,.0f}")

def gold_metric(label, value):
    return f"""
    <div style="
        background-color:#2d2d2d;
        border:1px solid #f4d03f;
        border-radius:10px;
        padding:20px;
        text-align:center;
    ">
        <div style="
            color:#f4d03f;
            font-size:1.1rem;
            font-weight:600;
            margin-bottom:8px;
        ">
            {label}
        </div>
        <div style="
            color:#f4d03f;
            font-size:2.5rem;
            font-weight:800;
            text-shadow:0 0 10px rgba(244,208,63,0.4);
        ">
            {value}
        </div>
    </div>
    """

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(gold_metric("Total Days", f"{len(df):,}"), unsafe_allow_html=True)

with col2:
    st.markdown(gold_metric("Max Daily Count", f"{df['count'].max():,.0f}"), unsafe_allow_html=True)

with col3:
    st.markdown(gold_metric("Avg Daily Count", f"{df['count'].mean():,.0f}"), unsafe_allow_html=True)

st.markdown("## 🔮 SARIMA Predictions")
col1, col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(
        "<div id='n-pred-container'>",
        unsafe_allow_html=True,
    )
    N_prediction = st.number_input(
    "Number of days to forecast", 
    min_value=1, max_value=365, value=31, step=1
    )
pred_sarm = sarima.predict(N_prediction)
pred_df = pd.DataFrame({"date": pred_sarm.index,
                        "count": np.exp(pred_sarm.values)})
fig_sarima = px.line(
    df.reset_index(),
    x="date",
    y="count",
    title="Cyclist Count Over Time",
)
fig_sarima.update_traces(
    name="Observed data",
    line=dict(color="#f4d03f", width=3),
    selector=0)

fig_sarima.add_scatter(
    x=pred_df["date"],
    y=pred_df["count"],
    mode="lines",
    name=f"SARIMA forecast ({N_prediction} days)",
    line=dict(color="#72ED20", width=3)  # lighter gold
)
fig_sarima.update_layout(
    showlegend=True,
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f4d03f", size=12)
    ),
    plot_bgcolor="#1a1a1a",
    paper_bgcolor="#1a1a1a",
    font=dict(color="#f4d03f"),
    title_font_color="#f4d03f",
    xaxis=dict(
        title=dict(
            text="Date",
            font=dict(color="#f4d03f", size=16)
        ),
        tickfont=dict(color="#f4d03f", size=12),
        gridcolor="#2d2d2d",
        zerolinecolor="#2d2d2d",
        linecolor="#f4d03f"
    ),

    yaxis=dict(
        title=dict(
            text="Cyclist Count",
            font=dict(color="#f4d03f", size=16)
        ),
        tickfont=dict(color="#f4d03f", size=12),
        gridcolor="#2d2d2d",
        zerolinecolor="#2d2d2d",
        linecolor="#f4d03f"
    )
)




st.plotly_chart(fig_sarima, use_container_width=True, key="sarima_chart")