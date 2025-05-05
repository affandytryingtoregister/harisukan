import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# -------------- SETTINGS --------------
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQC0K2a2x8G_5CgJALtSE4V9xLcnUz0QSIZLsrm8n0mW8-fz-CRrW0lKyp-LJbjaa3N72TBaoR5rEPr/pub?output=csv"  # 🔁 Replace with your sheet
REFRESH_INTERVAL = 30  # seconds
# Background image (blue-green fluid abstract)
BACKGROUND_IMAGE_URL = "https://static.vecteezy.com/system/resources/previews/006/812/555/non_2x/blue-green-abstract-fluid-shapes-background-vector.jpg"
# --------------------------------------

st.set_page_config(page_title="Sports Week Medal Tally", layout="wide")
st.title("🏅 Sports Week Live Medal Tally")

# 🔹 Inject background and translucent content box
page_bg_img = f'''
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("https://www.vecteezy.com/vector-art/681255-blue-green-abstract-fluid-shapes-background");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stHeader"] {{
    background: rgba(255, 255, 255, 0.5);
}}
[data-testid="stSidebar"] {{
    background: rgba(255, 255, 255, 0.5);
}}

.main > div {{
    background-color: rgba(255, 255, 255, 0.85);
    padding: 2rem;
    border-radius: 10px;
    margin-top: 1rem;
}}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Info
st.caption(f"Auto-refreshes every {REFRESH_INTERVAL} seconds to get latest medal data.")
st.query_params.update(refresh=int(time.time()))

# Load data
try:
    df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
    df.columns = df.columns.str.strip()
    df.fillna('', inplace=True)

    # Ensure numbers are integers
    df['Gold'] = pd.to_numeric(df['Gold'], errors='coerce').fillna(0).astype(int)
    df['Silver'] = pd.to_numeric(df['Silver'], errors='coerce').fillna(0).astype(int)
    df['Bronze'] = pd.to_numeric(df['Bronze'], errors='coerce').fillna(0).astype(int)
    df['Total'] = df['Gold'] + df['Silver'] + df['Bronze']

    # Sort
    df_sorted = df.sort_values(by=['Gold', 'Silver', 'Bronze'], ascending=False).reset_index(drop=True)
    df_sorted.index += 1

    # Chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Team'], y=df['Gold'], name='Gold', marker_color='gold',
        hovertext=df['Gold Events'], hoverinfo='text+y'
    ))
    fig.add_trace(go.Bar(
        x=df['Team'], y=df['Silver'], name='Silver', marker_color='silver',
        hovertext=df['Silver Events'], hoverinfo='text+y'
    ))
    fig.add_trace(go.Bar(
        x=df['Team'], y=df['Bronze'], name='Bronze', marker_color='#cd7f32',
        hovertext=df['Bronze Events'], hoverinfo='text+y'
    ))
    fig.update_layout(
        barmode='stack',
        title='Live Medal Tally (Hover to View Events)',
        xaxis_title='Team',
        yaxis_title='Medal Count',
        legend_title='Medal Type',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # Ranking table
    st.subheader("📊 Medal Ranking Table")
    st.dataframe(
        df_sorted[["Team", "Gold", "Silver", "Bronze", "Total"]].reset_index().rename(columns={"index": "Rank"}),
        use_container_width=True
    )

    # Auto-refresh
    time.sleep(REFRESH_INTERVAL)
    st.rerun()

except Exception as e:
    st.error(f"⚠️ Failed to load medal data from Google Sheets: {e}")
    st.info("Make sure the sheet is published as CSV and accessible by anyone with the link.")
