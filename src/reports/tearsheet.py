import os
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)

from reportlab.graphics.shapes import Drawing

os.makedirs("reports/tearsheets", exist_ok=True)
os.makedirs("temp", exist_ok=True)

master = pd.read_csv(
    "data/processed/master_dataset.csv"
)

cashflow = pd.read_excel(
    "output/cashflow_intelligence.xlsx"
)

try:
    pros_cons = pd.read_csv(
        "output/pros_cons_generated.csv"
    )

except:
    pros_cons = pd.DataFrame()

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal_style = styles["BodyText"]


def create_tearsheet(company):

    df = master[
        master["company_name"] == company
    ].copy()

    if df.empty:
        return

    latest = df.iloc[-1]

    pdf = SimpleDocTemplate(
        f"reports/tearsheets/{company}_tearsheet.pdf",
        pagesize=(8.27 * inch, 11.69 * inch)
    )

    story = []

    # ---------------- Header ----------------

    story.append(
        Paragraph(
            f"<font color='navy'><b>{company}</b></font>",
            title_style
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # ---------------- KPI Table ----------------

    kpi_table = [

        [
            "Revenue",
            f"{latest['sales']:,.0f}"
        ],

        [
            "Net Profit",
            f"{latest['net_profit']:,.0f}"
        ],

        [
            "ROE",
            f"{latest['return_on_equity_pct']:.2f}%"
        ],

        [
            "P/E",
            f"{latest['pe_ratio']:.2f}"
        ],

        [
            "Market Cap",
            f"{latest['market_cap_crore']:,.0f}"
        ],

        [
            "FCF",
            f"{latest['free_cash_flow_cr']:,.0f}"
        ]

    ]

    table = Table(
        kpi_table,
        colWidths=[2.5 * inch, 2.5 * inch]
    )

    table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)

        ])

    )

    story.append(table)

    story.append(
        Spacer(1, 20)
    )

    # ---------------- Revenue Chart ----------------

    revenue_chart = create_bar_chart(
        df,
        "sales",
        "Revenue Trend",
        f"{company}_revenue.png"
    )

    story.append(
        Paragraph(
            "<b>Revenue Trend</b>",
            heading_style
        )
    )

    story.append(
        Image(
            revenue_chart,
            width=5.8 * inch,
            height=3 * inch
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # ---------------- Net Profit Chart ----------------

    profit_chart = create_bar_chart(
        df,
        "net_profit",
        "Net Profit Trend",
        f"{company}_profit.png"
    )

    story.append(
        Paragraph(
            "<b>Net Profit Trend</b>",
            heading_style
        )
    )

    story.append(
        Image(
            profit_chart,
            width=5.8 * inch,
            height=3 * inch
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # ---------------- ROE vs ROCE ----------------

    roe_chart = create_line_chart(
        df,
        f"{company}_roe.png"
    )

    story.append(
        Paragraph(
            "<b>ROE vs ROCE</b>",
            heading_style
        )
    )

    story.append(
        Image(
            roe_chart,
            width=5.8 * inch,
            height=3 * inch
        )
    )

    story.append(
        Spacer(1, 20)
    )
    story.append(PageBreak())

    story.append(
        Paragraph(
            "<b>Balance Sheet Composition</b>",
            heading_style
        )
    )

    balance = df[
        [
            "year",
            "equity_capital",
            "borrowings",
            "other_liabilities"
        ]
    ].copy()

    balance_table = [["Year", "Equity", "Borrowings", "Other Liabilities"]]

    for _, row in balance.iterrows():

        balance_table.append([
            int(row["year"]),
            f"{row['equity_capital']:,.0f}",
            f"{row['borrowings']:,.0f}",
            f"{row['other_liabilities']:,.0f}"
        ])

    table = Table(balance_table)

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))

    story.append(table)

    story.append(Spacer(1, 20))
    story.append(
        Paragraph(
            "<b>Latest Cash Flow</b>",
            heading_style
        )
    )

    cash = [
        ["Operating", latest["operating_activity"]],
        ["Investing", latest["investing_activity"]],
        ["Financing", latest["financing_activity"]],
        ["Net Cash Flow", latest["net_cash_flow"]]
    ]

    cash_table = Table(cash)

    cash_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, -1), colors.beige),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))

    story.append(cash_table)

    story.append(Spacer(1, 20))
    story.append(
        Paragraph("<b>Pros</b>", heading_style)
    )

    if not pros_cons.empty:

        pros = pros_cons[
            (pros_cons["company_id"] == company) &
            (pros_cons["type"] == "pro")
        ]

        for _, row in pros.head(5).iterrows():

            story.append(
                Paragraph(
                    f"• {row['text']}",
                    normal_style
                )
            )

    story.append(Spacer(1, 15))
    story.append(
        Paragraph("<b>Cons</b>", heading_style)
    )

    if not pros_cons.empty:

        cons = pros_cons[
            (pros_cons["company_id"] == company) &
            (pros_cons["type"] == "con")
        ]

        for _, row in cons.head(5).iterrows():

            story.append(
                Paragraph(
                    f"• {row['text']}",
                    normal_style
                )
            )

    story.append(Spacer(1, 20))
    story.append(
        Paragraph(
            f"<b>Capital Allocation:</b> {latest['capital_allocation_label']}",
            heading_style
        )
    )

    pdf.build(story)


def create_bar_chart(df, column, title, filename):

    plt.figure(figsize=(5, 3))

    plt.bar(
        df["year"].astype(str),
        df[column],
        color="steelblue"
    )

    plt.title(title)

    plt.xticks(rotation=45)

    plt.tight_layout()

    path = f"temp/{filename}"

    plt.savefig(path)

    plt.close()

    return path


def create_line_chart(df, filename):

    plt.figure(figsize=(6, 3))

    plt.plot(
        df["year"],
        df["return_on_equity_pct"],
        marker="o",
        linewidth=2,
        label="ROE"
    )

    if "return_on_capital_employed_pct" in df.columns:

        plt.plot(
            df["year"],
            df["return_on_capital_employed_pct"],
            marker="s",
            linewidth=2,
            label="ROCE"
        )

    plt.title("ROE vs ROCE")

    plt.xlabel("Year")

    plt.ylabel("%")

    plt.legend()

    plt.grid(alpha=0.3)

    plt.tight_layout()

    path = f"temp/{filename}"

    plt.savefig(path)

    plt.close()

    return path


if __name__ == "__main__":

    company = "TCS"

    create_tearsheet(company)

    print(f"Tearsheet created successfully for {company}")
