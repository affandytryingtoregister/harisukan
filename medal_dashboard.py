import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# -------------- SETTINGS --------------
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQC0K2a2x8G_5CgJALtSE4V9xLcnUz0QSIZLsrm8n0mW8-fz-CRrW0lKyp-LJbjaa3N72TBaoR5rEPr/pub?output=csv"  # 🔁 Replace with your real link
REFRESH_INTERVAL = 30  # seconds
# --------------------------------------

st.set_page_config(page_title="Sports Week Medal Tally", layout="wide")
st.title("🏅 Sports Week Live Medal Tally")

st.caption(f"Auto-refreshes every {REFRESH_INTERVAL} seconds to get latest medal data.")
st.experimental_set_query_params(refresh=int(time.time()))

# Load CSV from Google Sheets
try:
    df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
    df.columns = df.columns.str.strip()
    df.fillna('', inplace=True)

    df['Gold'] = pd.to_numeric(df['Gold'], errors='coerce').fillna(0).astype(int)
    df['Silver'] = pd.to_numeric(df['Silver'], errors='coerce').fillna(0).astype(int)
    df['Bronze'] = pd.to_numeric(df['Bronze'], errors='coerce').fillna(0).astype(int)
    df['Total'] = df['Gold'] + df['Silver'] + df['Bronze']

    df_sorted = df.sort_values(by=['Gold', 'Silver', 'Bronze'], ascending=False).reset_index(drop=True)
    df_sorted.index += 1

    # Plot
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

    # Table
    st.subheader("📊 Medal Ranking Table")
    st.dataframe(
        df_sorted[["Team", "Gold", "Silver", "Bronze", "Total"]].reset_index().rename(columns={"index": "Rank"}),
        use_container_width=True
    )

    time.sleep(REFRESH_INTERVAL)
    st.rerun()

except Exception as e:
    st.error(f"⚠️ Failed to load medal data from Google Sheets: {e}")
    st.info("Make sure the sheet is published to the web as CSV and follows the correct column format.")
