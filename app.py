import streamlit as st
import pandas as pd
import feedparser

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("🧠 RiskOptix AI-X | Interactive Supply Chain Cognition Dashboard")

# --- Sidebar Controls ---
st.sidebar.title("⚙️ Simulation Controls")
scenario = st.sidebar.selectbox("Select Risk Scenario", ["Normal", "Flood", "Cyber Attack", "Port Strike"])
threshold_high = st.sidebar.slider("High Risk Threshold", 0.0, 1.0, 0.7)
threshold_med = st.sidebar.slider("Medium Risk Threshold", 0.0, threshold_high, 0.4)

uploaded_file = st.sidebar.file_uploader("📤 Upload New GNN Risk CSV", type=["csv"])

# --- Load Data ---
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("gnn_risk_predictions.csv")

st.header(f"📊 Node Risk Scores — Scenario: {scenario}")
st.dataframe(df)

# --- Risk Interpretation ---
def interpret_risk(score):
    if score > threshold_high:
        return "🔴 High"
    elif score > threshold_med:
        return "🟠 Medium"
    else:
        return "🟢 Low"

# --- Apply Interpretation ---
df["Risk Level"] = df["Risk"].apply(interpret_risk)
highest_risk_node = df.loc[df["Risk"].idxmax()]

# --- Mitigation Suggestion ---
st.subheader("🧠 AI Suggested Mitigation Strategy")
if highest_risk_node["Risk"] > threshold_high:
    st.success(f"🔁 Reroute Required for {highest_risk_node['Node']}")
    st.info("💰 Estimated Cost: $2000 | 🕒 Delay: 2 days")
elif highest_risk_node["Risk"] > threshold_med:
    st.info(f"🧱 Buffer Inventory Suggested at {highest_risk_node['Node']}")
    st.info("💰 Estimated Cost: $800 | 🕒 Delay: 3 days")
else:
    st.warning("⏳ Monitor Situation — No Action Required")

# --- Risk Visualization ---
st.subheader("📈 Risk Level by Node")
st.bar_chart(df.set_index("Node")["Risk"])

# --- Simulation Buttons ---
st.subheader("🧪 Mitigation Simulation")
action = st.radio("Choose an action to simulate:", ["None", "Reroute", "Increase Buffer", "Do Nothing"])

if action == "Reroute":
    st.write("✅ Rerouting reduces risk by 30% on top 2 nodes")
elif action == "Increase Buffer":
    st.write("✅ Buffering reduces delay risk, no cost change")
elif action == "Do Nothing":
    st.write("⚠️ No mitigation applied. Risk may rise.")
else:
    st.write("ℹ️ Select an action to see simulation impact.")

# --- Live News Feed ---
st.subheader("📰 Live News Feed")
def get_news_feed(query, max_items=5):
    rss_url = f"https://news.google.com/rss/search?q={query}+supply+chain"
    feed = feedparser.parse(rss_url)
    articles = feed.entries[:max_items]
    return [(entry.title, entry.link) for entry in articles]

news_query = scenario.lower().replace(" ", "+")
articles = get_news_feed(news_query)

if articles:
    for title, link in articles:
        st.markdown(f"🔹 [{title}]({link})", unsafe_allow_html=True)
else:
    st.write("No recent news found for this scenario.")

