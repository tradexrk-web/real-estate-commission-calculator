
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

import streamlit as st

def generate_pdf_report(
    property_price,
    commission_rate,
    agent_percentage,
    referral_percentage,
    commission,
    referral_fee,
    remaining_commission,
    agent_commission,
    brokerage_commission
):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(
        Paragraph("REAL ESTATE COMMISSION REPORT", styles["Title"])
    )

    story.append(Spacer(1, 20))

    report_data = [
        ["Description", "Amount / Percentage"],
        ["Property Sale Price", f"${property_price:,.2f}"],
        ["Commission Rate", f"{commission_rate:.2f}%"],
        ["Agent Share", f"{agent_percentage:.2f}%"],
        ["Referral Fee Rate", f"{referral_percentage:.2f}%"],
        ["Total Commission", f"${commission:,.2f}"],
        ["Referral Fee", f"${referral_fee:,.2f}"],
        ["Commission After Referral", f"${remaining_commission:,.2f}"],
        ["Agent Earnings", f"${agent_commission:,.2f}"],
        ["Brokerage Earnings", f"${brokerage_commission:,.2f}"]
    ]

    table = Table(
        report_data,
        colWidths=[3.2 * inch, 2.5 * inch]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.navy),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke)
    ]))

    story.append(table)

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "This report is generated for informational purposes.",
            styles["Italic"]
        )
    )

    document.build(story)

    return buffer.getvalue()

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


referral_percentage = st.number_input(
    "Referral Fee (%)",
    min_value=0.0,
    max_value=100.0,
    value=25.0
)

commission = property_price * commission_rate / 100

referral_fee = commission * referral_percentage / 100

remaining_commission = commission - referral_fee

agent_commission = remaining_commission * agent_percentage / 100

brokerage_commission = remaining_commission - agent_commission

st.divider()

st.subheader("Commission Report")

st.metric("Referral Fee", f"${referral_fee:,.2f}")

st.metric("Commission After Referral", f"${remaining_commission:,.2f}")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Commission", f"${commission:,.2f}")

with col2:
    st.metric("Agent Earnings", f"${agent_commission:,.2f}")

st.metric("Brokerage Earnings", f"${brokerage_commission:,.2f}")

pdf_report = generate_pdf_report(
    property_price,
    commission_rate,
    agent_percentage,
    referral_percentage,
    commission,
    referral_fee,
    remaining_commission,
    agent_commission,
    brokerage_commission
)

st.download_button(
    label="📄 Download PDF Report",
    data=pdf_report,
    file_name="commission_report.pdf",
    mime="application/pdf",
    use_container_width=True
)


st.caption("Commission calculations are estimates.")

