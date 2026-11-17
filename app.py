
import streamlit as st

st.set_page_config(
    page_title="Real Estate Commission Calculator",
    page_icon="🏡",
    layout="centered"
)

st.title("🏡 Real Estate Commission Calculator")
st.write("Calculate commission and agent earnings.")

st.divider()

property_price = st.number_input(
    "Property Sale Price ($)",
    min_value=0.0,
    value=500000.0,
    step=10000.0
)

commission_rate = st.number_input(
    "Commission Percentage (%)",
    min_value=0.0,
    value=3.0,
    step=0.25
)

agent_percentage = st.number_input(
    "Agent Share (%)",
    min_value=0.0,
    max_value=100.0,
    value=80.0,
    step=5.0
)

commission = property_price * commission_rate / 100

agent_commission = commission * agent_percentage / 100

brokerage_commission = commission - agent_commission

st.divider()

st.subheader("Commission Report")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Commission", f"${commission:,.2f}")

with col2:
    st.metric("Agent Earnings", f"${agent_commission:,.2f}")

st.metric("Brokerage Earnings", f"${brokerage_commission:,.2f}")

st.caption("Commission calculations are estimates.")

