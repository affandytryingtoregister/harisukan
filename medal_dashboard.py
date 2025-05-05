import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Sports Week Medal Tally", layout="wide")
st.title("🏅 Sports Week Live Medal Tally")

uploaded_file = st.file_uploader("Upload Medal Tally Excel", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()  # Clean up column names
    df.fillna('', inplace=True)

    # Medal values
    df['Total'] = df['Gold'] + df['Silver'] + df['Bronze']

    # Sort teams by medal priority
    df_sorted = df.sort_values(by=['Gold', 'Silver', 'Bronze'], ascending=False).reset_index(drop=True)
    df_sorted.index += 1  # Rank starts at 1

    teams = df['Team']
    gold = df['Gold']
    silver = df['Silver']
    bronze = df['Bronze']

    # Event hover data
    gold_events = df['Gold Events']
    silver_events = df['Silver Events']
    bronze_events = df['Bronze Events']

    # Bar Chart with Hover
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=teams,
        y=gold,
        name='Gold',
        marker_color='gold',
        hovertext=gold_events,
        hoverinfo='text+y'
    ))

    fig.add_trace(go.Bar(
        x=teams,
        y=silver,
        name='Silver',
        marker_color='silver',
        hovertext=silver_events,
        hoverinfo='text+y'
    ))

    fig.add_trace(go.Bar(
        x=teams,
        y=bronze,
        name='Bronze',
        marker_color='#cd7f32',  # Bronze
        hovertext=bronze_events,
        hoverinfo='text+y'
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

    # Show Ranking Table
    st.subheader("📊 Medal Ranking Table")
    st.dataframe(
        df_sorted[["Team", "Gold", "Silver", "Bronze", "Total"]].reset_index().rename(columns={"index": "Rank"}),
        use_container_width=True
    )

else:
    st.info("Please upload an Excel file with columns: Team, Gold, Gold Events, Silver, Silver Events, Bronze, Bronze Events.")
