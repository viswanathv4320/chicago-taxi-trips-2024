from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import json
from plotly.utils import PlotlyJSONEncoder

app = Flask(__name__)

df = pd.read_csv("chicago_taxi_2024_cleaned.csv")

@app.route("/")
def index():
    # Header stats
    stats = {
        "total_trips": f"{len(df) / 1_000_000:.1f}M",
        "total_revenue": f"${df['Trip Total'].sum() / 1_000_000:.0f}M",
        "avg_fare": f"${df['Fare'].mean():.2f}",
        "avg_tip_pct": f"{df['Tip Pct'].mean():.1f}%"
    }

    # Section 1 — Revenue over time
    df["month_num"] = df["Trip Start Month"].str.split("-").str[1].astype(int)
    monthly = df.groupby("month_num")["Trip Total"].sum().reset_index()
    monthly.columns = ["month", "revenue"]
    monthly["revenue"] = monthly["revenue"] / 1_000_000
    revenue_data = {
        "x": [int(x) for x in monthly["month"].tolist()],
        "y": [round(float(y), 2) for y in monthly["revenue"].tolist()]
    }
    revenue_chart = json.dumps(revenue_data)

    # Section 2 — Heatmap
    heatmap_data = df.groupby(["Day of Week", "Trip Start Hour"]).size().reset_index()
    heatmap_data.columns = ["day", "hour", "trips"]
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = heatmap_data.pivot(index="day", columns="hour", values="trips")
    pivot = pivot.reindex(day_order)
    heatmap_chart = json.dumps({
        "days": day_order,
        "hours": [int(h) for h in pivot.columns.tolist()],
        "z": [[int(v) for v in row] for row in pivot.values.tolist()]
    })

    # Section 3 — Company scorecard
    company = df.groupby("Company").size().reset_index(name="trips")
    company = company.sort_values("trips", ascending=False).head(10)
    company_data = {
        "labels": company["Company"].tolist(),
        "values": [int(x) for x in company["trips"].tolist()]
    }
    company_chart = json.dumps(company_data)

    # Section 4 — Payment mix
    payment = df["Payment Type"].value_counts().reset_index()
    payment = payment[payment["count"] > 10000]
    payment_data = {
        "labels": payment["Payment Type"].tolist(),
        "values": [int(x) for x in payment["count"].tolist()]
    }
    payment_chart = json.dumps(payment_data)

    return render_template("index.html",
                           stats=stats,
                           revenue_chart=revenue_chart,
                           heatmap_chart=heatmap_chart,
                           company_chart=company_chart,
                           payment_chart=payment_chart)

@app.route("/debug")
def debug():
    # Chart 1
    df["month_num"] = df["Trip Start Month"].str.split("-").str[1].astype(int)
    monthly = df.groupby("month_num")["Trip Total"].sum().reset_index()
    monthly.columns = ["month", "revenue"]
    monthly["revenue"] = monthly["revenue"] / 1_000_000
    print("=== MONTHLY ===")
    print(monthly)

    # Chart 2
    heatmap_data = df.groupby(["Day of Week", "Trip Start Hour"]).size().reset_index()
    heatmap_data.columns = ["day", "hour", "trips"]
    print("=== HEATMAP sample ===")
    print(heatmap_data.head(10))

    # Chart 3
    company = df.groupby("Company").size().reset_index(name="trips")
    company = company.sort_values("trips", ascending=False).head(10)
    print("=== COMPANY ===")
    print(company)

    # Chart 4
    payment = df["Payment Type"].value_counts().reset_index()
    print("=== PAYMENT ===")
    print(payment)
    print(payment.columns.tolist())

    return "Check your terminal"

if __name__ == "__main__":
    app.run(debug=True)