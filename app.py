from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__)

# Load pre-aggregated data — fast to load
stats_df   = pd.read_csv("data/data_stats.csv")
monthly_df = pd.read_csv("data/data_monthly.csv")
heatmap_df = pd.read_csv("data/data_heatmap.csv")
company_df = pd.read_csv("data/data_company.csv")
payment_df = pd.read_csv("data/data_payment.csv")

@app.route("/")
def index():
    # Header stats
    row = stats_df.iloc[0]
    stats = {
        "total_trips": f"{row['total_trips'] / 1_000_000:.1f}M",
        "total_revenue": f"${row['total_revenue'] / 1_000_000:.0f}M",
        "avg_fare": f"${row['avg_fare']:.2f}",
        "avg_tip_pct": f"{row['avg_tip_pct']:.1f}%"
    }

    # Section 1 — Revenue
    revenue_chart = json.dumps({
        "x": [int(x) for x in monthly_df["month_num"].tolist()],
        "y": [round(float(y), 2) for y in monthly_df["Trip Total"].tolist()]
    })

    # Section 2 — Heatmap
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = heatmap_df.pivot(index="day", columns="hour", values="trips")
    pivot = pivot.reindex(day_order)
    heatmap_chart = json.dumps({
        "days": day_order,
        "hours": [int(h) for h in pivot.columns.tolist()],
        "z": [[int(v) for v in row] for row in pivot.values.tolist()]
    })

    # Section 3 — Company
    company_chart = json.dumps({
        "labels": company_df["Company"].tolist(),
        "values": [int(x) for x in company_df["trips"].tolist()]
    })

    # Section 4 — Payment
    payment_chart = json.dumps({
        "labels": payment_df["Payment Type"].tolist(),
        "values": [int(x) for x in payment_df["count"].tolist()]
    })

    return render_template("index.html",
                           stats=stats,
                           revenue_chart=revenue_chart,
                           heatmap_chart=heatmap_chart,
                           company_chart=company_chart,
                           payment_chart=payment_chart)

if __name__ == "__main__":
    app.run(debug=True)